import os
import sys
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from parser import clean_message  # ✅ 텔레그램 메시지 전처리 함수
import pytz
from datetime import datetime
from myconfig import API_ID, API_HASH, CHANNEL_USERNAME  

# ✅ 글로벌 클라이언트 세션 생성
client = TelegramClient("session_name", API_ID, API_HASH)

async def connect_client():
    """텔레그램 클라이언트 연결"""
    if not client.is_connected():
        await client.connect()
        print("✅ 텔레그램 클라이언트 다시 연결됨")

    if not await client.is_user_authorized():
        print("⚠️ 텔레그램 클라이언트가 인증되지 않았습니다. 로그인이 필요합니다.")
        return False
    return True

async def crawl_telegram_messages():
    """다중 텔레그램 채널에서 메시지 크롤링 (sender, cleaned_text, timestamp 반환)"""
    kst = pytz.timezone("Asia/Seoul")
    extracted_data = []  # 📌 크롤링한 데이터를 저장할 리스트
    seen_texts = set()

    if not await connect_client():
        print("⚠️ 클라이언트 연결 실패")
        return extracted_data

    for channel in CHANNEL_USERNAME:  # ✅ 여러 채널을 순회
        print(f"🔍 크롤링 중: {channel}")

        try:
            entity = await client.get_entity(channel)
            print(f"✅ 채널 `{channel}` 엔터티 가져오기 성공")

            messages = await client(GetHistoryRequest(
                peer=entity,
                limit=50,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))

            print(f"📩 가져온 메시지 수: {len(messages.messages)}")

            for message in messages.messages:
                if message.message:  # ✅ 실제 메시지가 있는 경우만 처리
                    sender = message.sender_id
                    raw_text = message.message
                    cleaned_text = clean_message(raw_text)  # ✅ 전처리된 메시지

                     # 이미 수집한 메시지 내용이면 스킵
                    if cleaned_text in seen_texts:
                        continue
                    seen_texts.add(cleaned_text)

                    timestamp = message.date.astimezone(kst).strftime("%Y-%m-%d %H:%M:%S")

                    # ✅ sender, cleaned_text, timestamp만 저장
                    extracted_data.append({
                        "sender": sender,
                        "cleaned_text": cleaned_text,
                        "timestamp": timestamp
                    })

            print(f"✅ 크롤링 완료, 총 {len(extracted_data)}개의 메시지 추출됨.")

        except Exception as e:
            print(f"⚠️ 채널 `{channel}` 크롤링 중 오류 발생: {e}")

    return extracted_data  # ✅ 리스트 형태로 반환

async def main():
    """크롤링 실행"""
    data = await fetch_messages()
    print("📌 크롤링된 데이터:", data)

if __name__ == "__main__":
    asyncio.run(crawl_telegram_messages())  # ✅ 직접 실행할 경우만 실행되도록 설정
