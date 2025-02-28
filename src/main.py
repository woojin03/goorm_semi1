import sys
import os
import asyncio
import aiohttp

# ✅ Python 모듈 경로 설정 (src 폴더 인식)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ 필요한 값만 import
from config import API_ID, API_HASH, CHANNEL_USERNAME, PHONE_NUMBER, DISCORD_TOKEN, MONGO_URI, MONGO_DB_NAME, ELASTICSEARCH_HOST, CRAWLER_INTERVAL
from bot.bot import bot  # 디스코드 봇
from crawler.scheduler import scheduled_task  # 텔레그램 크롤러
from bot.alert import monitor_keywords  # 키워드 감지 기능
from bot.send_report import send_report  # 일일 보고서 디스코드 전송
from services.report import run_elasticsearch_search, update_html_with_data  # 보고서 업데이트 기능

async def daily_report():
    """📢 자동 다크웹 리포트 생성 & 전송"""
    print("📢 [자동 보고서] 다크웹 리포트 생성 & 디스코드 전송 시작")

    # ✅ 1. Elasticsearch에서 최신 데이터 가져오기
    run_elasticsearch_search()

    # ✅ 2. HTML 리포트(news.html) 업데이트
    update_html_with_data()

    # ✅ 3. 디스코드에 보고서 전송
    await send_report(bot)

    print("✅ [자동 보고서] 다크웹 리포트 전송 완료")

async def schedule_daily_report():
    """📅 하루에 한 번 보고서 자동 생성 & 전송"""
    while True:
        await daily_report()  # ✅ 일일 보고서 실행
        await asyncio.sleep(86400)  # ✅ 24시간 (86400초) 대기 후 다시 실행

async def main():
    """🎯 크롤러, 디스코드 봇, 키워드 감지, 일일 보고서 실행"""
    task1 = asyncio.create_task(bot.start(DISCORD_TOKEN))  # ✅ 디스코드 봇 실행
    task2 = asyncio.create_task(scheduled_task())  # ✅ 텔레그램 크롤러 실행
    task3 = asyncio.create_task(monitor_keywords())  # ✅ 키워드 감지 기능 실행
    task4 = asyncio.create_task(schedule_daily_report())  # ✅ 일일 보고서 자동 실행

    await asyncio.gather(task1, task2, task3, task4)  # 🚀 모든 기능 동시 실행

if __name__ == "__main__":
    try:
        asyncio.run(main())  # ✅ `main.py` 실행
    except KeyboardInterrupt:
        print("🛑 프로그램 종료 중...")