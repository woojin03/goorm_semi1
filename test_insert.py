import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from elasticsearch import AsyncElasticsearch
from datetime import datetime, timezone, timedelta

# ✅ 한국 시간(KST, UTC+9) 설정
KST = timezone(timedelta(hours=9))

# ✅ MongoDB 연결 설정
MONGO_URI = "mongodb://admin:1234@localhost:27017/darkweb?authSource=admin"
mongo_client = AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client.darkweb  # ✅ `darkweb` 데이터베이스 선택

# ✅ Elasticsearch 연결 설정
ELASTICSEARCH_HOST = "http://localhost:9200"
es_client = AsyncElasticsearch([ELASTICSEARCH_HOST])

# ✅ 테스트 데이터셋 (한국 시간 적용)
test_data = {
    "title": "Test Leak Report",
    "content": "This is a test entry for a dark web data breach.",
    "source": "http://darkweb.example.com",
    "timestamp": datetime.now(KST).isoformat()  # ✅ 한국 시간을 ISO 8601 형식 문자열로 변환
}

async def insert_mongo(data):
    """✅ MongoDB 데이터 삽입"""
    try:
        collection = mongo_db.darkweb_site_1  # ✅ `darkweb_site_1` 컬렉션 선택
        result = await collection.insert_one(data)
        inserted_id = str(result.inserted_id)  # ✅ `_id`를 문자열로 변환
        print(f"✅ MongoDB 데이터 삽입 완료: {inserted_id}")
        return inserted_id
    except Exception as e:
        print(f"❌ MongoDB 삽입 실패: {e}")
        return None

async def insert_elasticsearch(data, doc_id):
    """✅ Elasticsearch 데이터 삽입"""
    try:
        index_name = "darkweb_site_1"  # ✅ `darkweb_site_1` 인덱스 사용
        es_data = data.copy()  # ✅ 원본 데이터 복사

        # ✅ `_id` 필드를 제거하고, `id`로 전달
        if "_id" in es_data:
            del es_data["_id"]  # ✅ MongoDB의 `_id` 필드 제거

        await es_client.index(index=index_name, id=doc_id, document=es_data)
        print(f"✅ Elasticsearch 데이터 삽입 완료: {doc_id}")
    except Exception as e:
        print(f"❌ Elasticsearch 삽입 실패: {e}")

async def main():
    """✅ MongoDB & Elasticsearch 데이터 삽입 테스트"""
    doc_id = await insert_mongo(test_data)  # ✅ MongoDB에 먼저 삽입
    if doc_id:
        await insert_elasticsearch(test_data, doc_id)  # ✅ Elasticsearch에 같은 데이터 삽입

    # ✅ 클라이언트 종료
    await es_client.close()
    mongo_client.close()

# ✅ 비동기 실행
if __name__ == "__main__":
    asyncio.run(main())
