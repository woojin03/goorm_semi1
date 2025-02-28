import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from config import API_ID, API_HASH, CHANNEL_USERNAME
from crawler.parser import clean_message
import pytz
from datetime import datetime, timezone

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

async def fetch_messages():
    """텔레그램 크롤러 - 데이터를 수집하여 리스트로 반환"""
    kst = pytz.timezone("Asia/Seoul")
    messages_list = []  # ✅ 리스트로 저장

    # ✅ 클라이언트 연결 확인
    if not await connect_client():
        print("⚠️ 클라이언트 연결 실패")
        return []

    for channel in CHANNEL_USERNAME:
        print(f"🔍 크롤링 중: {channel}")

        try:
            entity = await client.get_entity(channel)
            messages = await client(GetHistoryRequest(
                peer=entity, limit=50, offset_date=None, offset_id=0,
                max_id=0, min_id=0, add_offset=0, hash=0
            ))

            for message in messages.messages:
                if message.message:
                    sender = message.sender_id
                    raw_text = message.message
                    cleaned_text = clean_message(raw_text)
                    timestamp = message.date.astimezone(kst).strftime("%Y-%m-%d %H:%M:%S")

                    # ✅ 데이터를 리스트에 추가
                    messages_list.append({
                        "sender_id": sender,
                        "message_text": cleaned_text,
                        "timestamp": timestamp,
                        "insert_time": datetime.now(timezone.utc).isoformat()
                    })

        except Exception as e:
            print(f"⚠️ 채널 `{channel}` 크롤링 중 오류 발생: {e}")

    return messages_list  # ✅ 리스트 반환
