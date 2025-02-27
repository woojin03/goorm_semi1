import asyncio
from datetime import datetime, timezone, timedelta
from .dup import dup_search
from .insert_DB import insert_DB

# ✅ 한국 시간(KST, UTC+9) 설정
KST = timezone(timedelta(hours=9))


async def db_m1(data1):
    """첫 번째 크롤러 데이터 저장"""
    if data1:
        for item in data1:
            insert_data = {
                "victim_title": item.get("title", "제목 없음"),
                "victim_site": item.get("website", "사이트 없음"),
                "victim_explan": item.get("description", "설명 없음"),
                "insert_time": datetime.now(KST).isoformat()
            }

            # 중복 여부 체크 (비동기)
            if await dup_search(insert_data, "darkweb_site_1") == 1:
                break
            await insert_DB(insert_data, "darkweb_site_1")


async def db_m2(data2):
    """두 번째 크롤러 데이터 저장"""
    if data2:
        for item in data2:
            insert_data = {
                "victim_title": item.get("title", "제목 없음"),
                "victim_explan": item.get("description", "설명 없음"),
                "insert_time": datetime.now(KST).isoformat()
            }

            if await dup_search(insert_data, "darkweb_site_2") == 1:
                break
            await insert_DB(insert_data, "darkweb_site_2")


async def db_m3(data3):
    """세 번째 크롤러 데이터 저장 (텔레그램)"""
    if data3:
        for item in data3:
            insert_data = {
                "sender_id": item.get("sender", "발신자 없음"),
                "content": item.get("cleaned_text", "내용 없음"),
                "date": item.get("timestamp", "날짜 없음"),
                "insert_time": datetime.now(KST).isoformat()
            }

            if await dup_search(insert_data, "darkweb_site_3") == 1:
                break
            await insert_DB(insert_data, "darkweb_site_3")


async def db_m(data1, data2, data3):
    """세 개의 데이터베이스 저장 작업을 동시에 실행"""
    await asyncio.gather(
        db_m1(data1),
        db_m2(data2),
        db_m3(data3)
    )
