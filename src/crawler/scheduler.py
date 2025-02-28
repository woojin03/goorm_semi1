import asyncio
from crawler.darkweb_1 import crawl_darkweb1
from crawler.darkweb_2 import crawl_darkweb2
from crawler.darkweb_3 import fetch_messages  # ✅ 텔레그램 크롤러 포함
from database.database_mongo import save_messages

async def scheduled_task():
    """ 다크웹 및 텔레그램 크롤링을 주기적으로 실행하고 DB에 저장 """
    while True:
        print("🔍 다크웹 및 텔레그램 크롤링 시작...")
        all_messages = []  # ✅ 모든 크롤러 데이터를 저장할 리스트

        # ✅ 다크웹 크롤러 1 실행
        data_1 = await crawl_darkweb1()
        for item in data_1:
            item["source"] = "darkweb_1"  # ✅ 출처 추가
        all_messages.extend(data_1)

        # ✅ 다크웹 크롤러 2 실행
        data_2 = await crawl_darkweb2()
        for item in data_2:
            item["source"] = "darkweb_2"  # ✅ 출처 추가
        all_messages.extend(data_2)

        # ✅ 텔레그램 크롤러 실행
        telegram_data = await fetch_messages()
        for item in telegram_data:
            item["source"] = "telegram"  # ✅ 출처 추가
        all_messages.extend(telegram_data)

        if all_messages:
            await save_messages(all_messages)  # ✅ DB 저장
            print(f"✅ {len(all_messages)}개의 데이터 저장 완료!")

        print("⏳ 다음 크롤링까지 대기 중...")
        await asyncio.sleep(300)  # ✅ 15분마다 실행 (900초) -> 추후 조정 가능
