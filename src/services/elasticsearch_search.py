import asyncio
import os
import json
from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date  # pip install python-dateutil

async def fetch_data_from_elasticsearch():
    """Elasticsearch에서 데이터를 비동기적으로 가져와 JSON 파일로 저장"""
    
    load_dotenv()
    ELASTICSEARCH_H = os.getenv("ELASTICSEARCH_HOST")
    es_client = AsyncElasticsearch([ELASTICSEARCH_H])

    # ✅ 그룹별 인덱스 정의
    GROUP_1_2_INDICES = ["darkweb_site_1", "darkweb_site_2"]
    GROUP_3_INDICES   = ["darkweb_site_3"]

    async def wait_for_elasticsearch():
        """Elasticsearch가 준비될 때까지 대기"""
        while True:
            try:
                if await es_client.ping():
                    print("✅ Elasticsearch 연결 성공!")
                    return
            except Exception:
                print("⏳ Elasticsearch 연결 대기 중...")
                await asyncio.sleep(5)

    async def fetch_data(index_name, query):
        """특정 인덱스에서 데이터를 가져오는 함수"""
        try:
            response = await es_client.search(index=index_name, body=query)
            hits = response.get('hits', {}).get('hits', [])
            return [hit["_source"] for hit in hits]
        except Exception as e:
            print(f"⚠️ {index_name}에서 데이터를 가져오는 중 오류 발생: {e}")
            return []

    await wait_for_elasticsearch()

    # ✅ 모든 문서를 검색하는 쿼리
    query = {"query": {"match_all": {}}}

    # ✅ 그룹 1_2 데이터 수집 (darkweb_site_1, darkweb_site_2)
    group_1_2_data = []
    for index in GROUP_1_2_INDICES:
        data = await fetch_data(index, query)
        group_1_2_data.extend(data)

    # ✅ 그룹 3 데이터 수집 (darkweb_site_3)
    group_3_data = []
    for index in GROUP_3_INDICES:
        data = await fetch_data(index, query)
        group_3_data.extend(data)

    await es_client.close()

    print(f"✅ 그룹 1_2 데이터 수집 완료: {len(group_1_2_data)}개")
    print(f"✅ 그룹 3 데이터 수집 완료: {len(group_3_data)}개")

    # ✅ 날짜 비교를 위해 현재 시간 및 기준 시간 설정
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    one_week_ago = now - timedelta(days=7)

    def get_datetime(record):
        """insert_time 값을 datetime 객체로 변환"""
        ts = record.get("insert_time")
        if not ts:
            return None
        try:
            dt = parse_date(ts)
            if dt.tzinfo is not None:
                dt = dt.astimezone().replace(tzinfo=None)  # 타임존 제거
            return dt
        except Exception:
            return None

    # ✅ 오늘(최근 1일) 데이터 필터링
    group_1_2_today = [rec for rec in group_1_2_data if (dt := get_datetime(rec)) and dt >= today_start]
    group_3_today = [rec for rec in group_3_data if (dt := get_datetime(rec)) and dt >= today_start]

    # ✅ 최근 1주일 데이터 필터링
    group_1_2_last_week = [rec for rec in group_1_2_data if (dt := get_datetime(rec)) and one_week_ago <= dt <= now]
    group_3_last_week = [rec for rec in group_3_data if (dt := get_datetime(rec)) and one_week_ago <= dt <= now]

    def save_to_json(filename, data):
        """데이터를 JSON 파일로 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ✅ 각 그룹 및 기간별 데이터를 저장
    save_to_json("src/services/today_data_1_2.json", group_1_2_today)
    save_to_json("src/services/last_week_data_1_2.json", group_1_2_last_week)
    save_to_json("src/services/today_data_3.json", group_3_today)
    save_to_json("src/services/last_week_data_3.json", group_3_last_week)

    print("✅ JSON 파일들이 성공적으로 저장되었습니다.")

# ✅ 데이터를 동기적으로 실행하는 함수
'''def get_elasticsearch_data():
    asyncio.run(fetch_data_from_elasticsearch())

if __name__ == "__main__":
    get_elasticsearch_data()'''