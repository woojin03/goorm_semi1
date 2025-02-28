import asyncio
from database.database_mongo import get_all_keywords, db
from bot.bot import send_discord_alert
from elasticsearch import AsyncElasticsearch
from datetime import datetime, timezone
from config import ELASTICSEARCH_HOST

# ✅ Elasticsearch 클라이언트 설정
es = AsyncElasticsearch([ELASTICSEARCH_HOST])

# ✅ 유저별 알림 기록 저장 (MongoDB)
alert_collection = db["user_alerts"]

# ✅ 검색할 Elasticsearch 인덱스 목록
ELASTIC_INDICES = ["darkweb_site_1", "darkweb_site_2", "darkweb_site_3"]

# ✅ 크롤러별 필드 매핑 (검색 대상 필드)
SEARCH_FIELDS = {
    "darkweb_site_1": ["title", "description"],
    "darkweb_site_2": ["title", "description", "website"],
    "darkweb_site_3": ["message_text"]
}

async def search_keywords_in_elastic():
    """✅ Elasticsearch에서 키워드를 검색하고 유저별로 알림을 전송"""
    user_keywords = await get_all_keywords()

    for user_id, keywords in user_keywords.items():
        for keyword in keywords:
            # ✅ 검색 쿼리 생성 (키워드 포함 여부 확인)
            query = {
                "query": {
                    "bool": {
                        "should": [
                            {"match": {field: keyword}} for field in ["message_text", "title", "description"]
                        ],
                        "minimum_should_match": 1
                    }
                }
            }

            try:
                for index in ELASTIC_INDICES:
                    response = await es.search(index=index, body=query)

                    for hit in response["hits"]["hits"]:
                        data = hit["_source"]
                        timestamp = data.get("timestamp", "")
                        doc_id = hit["_id"]

                        print(f"🔍 [Elasticsearch] 키워드 '{keyword}'가 인덱스 '{index}'에서 발견됨")

                        # ✅ 유저별 알림 중복 방지 (MongoDB `user_alerts` 활용)
                        existing_alert = await alert_collection.find_one(
                            {"user_id": user_id, "message_id": doc_id}
                        )

                        if existing_alert:
                            print(f"⚠️ 유저 {user_id} 에게 이미 전송된 메시지 (ID: {doc_id})")
                            continue  # 이미 알림을 받은 경우 건너뜀

                        # ✅ 디스코드 알림 전송
                        await send_discord_alert(user_id, keyword, data, timestamp)

                        # ✅ 유저별 알림 기록을 MongoDB에 저장
                        await alert_collection.insert_one({
                            "user_id": user_id,
                            "message_id": doc_id,
                            "timestamp": datetime.now(timezone.utc)
                        })
                        print(f"✅ 유저 {user_id} 에게 알림 전송 완료 (ID: {doc_id})")

            except Exception as e:
                print(f"⚠️ Elasticsearch 검색 오류 (인덱스: {index}): {e}")

async def monitor_keywords():
    """✅ 주기적으로 키워드 검색 실행 (Elasticsearch만 사용)"""
    print("🔍 Elasticsearch 키워드 검색을 즉시 실행...")
    await search_keywords_in_elastic()  # ✅ 첫 실행 시 즉시 검색 실행

    while True:
        print("⏳ Elasticsearch에서 주기적으로 키워드 검색 실행 중...")
        await search_keywords_in_elastic()
        await asyncio.sleep(180)  # ✅ 3분마다 실행
