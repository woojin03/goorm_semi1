import os
import sys
import asyncio
import schedule
import time

# ✅ `scheduler.py` 실행 환경에서 `crawl/telegram/`을 찾을 수 있도록 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # `scheduler.py` 경로
TELEGRAM_DIR = os.path.join(BASE_DIR, "crawl", "telegram")  # `config.py`가 있는 폴더
sys.path.append(TELEGRAM_DIR)  # ✅ Python이 `config.py`를 찾을 수 있도록 설정
print(sys.path)

# ✅ 크롤러 모듈 가져오기
from crawl.darkweb.RansomEXX_crawl import crawl_darkweb as crawl_darkweb_1  # ✅ 첫 번째 크롤러
from crawl.darkweb.test_darkweb_1 import crawl_darkweb as crawl_darkweb_2  # ✅ 두 번째 크롤러
from crawl.telegram.test_telegram_crawler import crawl_telegram_messages as crawl_telegram  # ✅ 세 번째 크롤러
from db.db_m import db_m
from db.dup import dup_search

# ✅ 크롤링된 데이터를 저장할 리스트
all_crawled_data = []  # 데이터를 저장할 리스트

async def scheduled_task():
    """🕒 15분마다 실행되는 크롤링 + 데이터 저장"""

    print("\n⏳ 첫 번째 크롤링 작업 시작...")
    data1 = await crawl_darkweb_1()
    print(f"✅ 첫 번째 크롤링 작업 완료! (수집된 데이터 개수: {len(data1)})")

    print("\n⏳ 두 번째 크롤링 작업 시작...")
    data2 = await crawl_darkweb_2()
    print(f"✅ 두 번째 크롤링 작업 완료! (수집된 데이터 개수: {len(data2)})")

    print("\n⏳ 텔레그램 크롤링 작업 시작...")
    data3 = await crawl_telegram()
    print(f"✅ 텔레그램 크롤링 작업 완료! (수집된 데이터 개수: {len(data3)})")

    # ✅ 크롤링한 데이터를 DB에 저장
    print("\n💾 데이터베이스 저장 시작...")
    await db_m(data1, data2, data3)
    print("✅ 데이터베이스 저장 완료!")


async def run_scheduler():
    """⏰ 15분마다 실행하는 스케줄러"""
    print("🕒 스케줄러가 실행 중입니다... (15분 간격으로 3개의 크롤러 실행)")
    schedule.every(1).minutes.do(lambda: asyncio.create_task(scheduled_task()))  # ✅ 15분마다 실행
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)  # CPU 과부하 방지를 위해 1초 대기

# 프로그램 실행
if __name__ == "__main__":
    asyncio.run(run_scheduler())  # ✅ 비동기 스케줄러 실행
