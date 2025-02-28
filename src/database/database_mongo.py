from motor.motor_asyncio import AsyncIOMotorClient
from elasticsearch import AsyncElasticsearch
import os
from dotenv import load_dotenv
from datetime import datetime

# ✅ 환경 변수 로드
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:1234@localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "darkweb_data")
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")

# ✅ MongoDB & Elasticsearch 클라이언트 초기화
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
es_client = AsyncElasticsearch([ELASTICSEARCH_HOST])

# ✅ 크롤러별 MongoDB 컬렉션 매핑
DARKWEB_COLLECTIONS = {
    "darkweb_1": "darkweb_site_1",
    "darkweb_2": "darkweb_site_2",
    "darkweb_3": "darkweb_site_3",
    "telegram": "darkweb_site_3"
}
KEYWORD_COLLECTION = "discord_user"  # 키워드 저장
ALERT_COLLECTION = "user_alerts"  # ✅ 유저별 알림 기록 저장

# ✅ 크롤러별 중복 확인 필드 매핑
# ✅ 크롤러별 중복 확인 필드 매핑 (데이터 구조에 맞게 수정)
KEY_FIELDS = {
    "darkweb_site_1": ["title", "description", "website"],  # ✅ 일반 다크웹 크롤링 데이터
    "darkweb_site_2": ["title", "description", "website"],  # ✅ 일반 다크웹 크롤링 데이터
    "darkweb_site_3": ["sender_id", "message_text", "timestamp"]  # ✅ 텔레그램 크롤링 데이터
}


async def dup_search(data: dict, collection: str) -> int:
    """✅ MongoDB & Elasticsearch 중복 검색"""
    key_fields = KEY_FIELDS.get(collection, ["title", "description", "website"])  # ✅ 검색 필드 확인

    # ✅ 모든 값이 `None`, 빈 문자열, 리스트 또는 딕셔너리인 경우 제외
    query_conditions = []
    for field in key_fields:
        value = data.get(field)
        if value and isinstance(value, (str, int, float)):  # ✅ 숫자 및 문자열 데이터만 처리
            value = str(value).strip()  # ✅ 문자열 변환 후 공백 제거
            if value and value.lower() != "none":  # ✅ 'none' 문자열 제외
                query_conditions.append({"match": {field: value}})

    if not query_conditions:  # ✅ 검색할 필드가 없으면 Elasticsearch 검색하지 않음
        print(f"⚠️ 검색할 값이 없어 중복 검사를 수행하지 않음: {data}")
        return 0  

    query_elastic = {
        "query": {
            "bool": {
                "must": query_conditions
            }
        }
    }

    try:
        existing_message_elastic = await es_client.search(index=collection, body=query_elastic)
        return 1 if existing_message_elastic["hits"]["total"]["value"] > 0 else 0
    except Exception as e:
        print(f"⚠️ Elasticsearch 검색 오류 (인덱스: {collection}): {e}")
        return 0


async def save_messages(messages):
    """ ✅ MongoDB & Elasticsearch에 메시지 저장 """
    
    grouped_messages = {}
    for message in messages:
        source = message.get("source", "unknown")
        collection_name = DARKWEB_COLLECTIONS.get(source)
        if not collection_name:
            print(f"⚠️ 알 수 없는 데이터 출처: {source}")
            continue
        grouped_messages.setdefault(collection_name, []).append(message)

    for collection_name, docs in grouped_messages.items():
        collection = db[collection_name]
        for message in docs:
            # ✅ 중복 데이터 확인 (MongoDB + Elasticsearch)
            if await dup_search(message, collection_name) == 1:
                print(f"⚠️ 중복 데이터로 저장되지 않음: {message.get('title', message.get('message_text', 'No Title'))}")
                continue

            # ✅ 기본적으로 `alert_sent=False` 설정
            message["alert_sent"] = False
            insert_result = await collection.insert_one(message)
            doc_id = str(insert_result.inserted_id)

            # ✅ Elasticsearch 저장
            message_data = message.copy()
            message_data.pop("_id", None)
            if isinstance(message_data.get("timestamp"), datetime):
                message_data["timestamp"] = message_data["timestamp"].isoformat()
            await es_client.index(index=collection_name, id=doc_id, document=message_data)
            print(f"✅ [{collection_name}] 저장 완료")

async def get_all_keywords():
    """ ✅ discord_user 컬렉션에서 모든 사용자의 키워드 목록 가져오기 """
    user_keywords = {}
    async for doc in db[KEYWORD_COLLECTION].find():
        user_id = doc["user_id"]
        keyword = doc["keyword"]
        if user_id not in user_keywords:
            user_keywords[user_id] = []
        user_keywords[user_id].append(keyword)
    return user_keywords
