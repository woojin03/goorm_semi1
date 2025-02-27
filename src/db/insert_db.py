# insert_DB.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from elasticsearch import AsyncElasticsearch

# MongoDB 설정: 인증 정보를 포함한 darkweb 데이터베이스 연결
MONGO_URI = "mongodb://admin:1234@localhost:27017/darkweb?authSource=admin"
mongo_client = AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client.darkweb  # darkweb 데이터베이스 선택

# Elasticsearch 설정
es = AsyncElasticsearch(hosts=["http://localhost:9200"])

async def insert_DB(data: dict, collection_or_index: str):
    """
    MongoDB와 Elasticsearch에 데이터를 삽입하는 함수입니다.
    MongoDB의 _id 값을 Elasticsearch의 문서 id로 사용합니다.

    매개변수:
      - data: 삽입할 데이터 (dict)
      - collection_or_index: MongoDB 컬렉션 및 Elasticsearch 인덱스 이름
    """
    # MongoDB에 데이터 삽입
    try:
        collection = mongo_db[collection_or_index]
        mongo_result = await collection.insert_one(data)
        # MongoDB에서 반환된 _id를 문자열로 변환하여 사용
        doc_id = str(mongo_result.inserted_id)
        print(f"✅ MongoDB 삽입 성공 (컬렉션: {collection_or_index}): {doc_id}")
    except Exception as e:
        print(f"❌ MongoDB 삽입 오류 (컬렉션: {collection_or_index}): {e}")
        return  # MongoDB 삽입에 실패하면 Elasticsearch 삽입은 진행하지 않음

    # Elasticsearch에 동일한 id 값으로 데이터 삽입
    try:
        # 원본 데이터 복사 후 MongoDB의 _id 필드가 있다면 제거
        es_data = data.copy()
        if "_id" in es_data:
            del es_data["_id"]
        await es.index(index=collection_or_index, id=doc_id, document=es_data)
        print(f"✅ Elasticsearch 삽입 성공 (인덱스: {collection_or_index}): {doc_id}")
    except Exception as e:
        print(f"❌ Elasticsearch 삽입 오류 (인덱스: {collection_or_index}): {e}")

# 간단한 테스트 예제
if __name__ == "__main__":
    async def main():
        sample_data = {
            "victim_title": "테스트 타이틀",
            "victim_site": "example.com",
            "victim_explan": "테스트 설명",
            "insert_time": "2025-02-27T12:00:00"
        }
        await insert_DB(sample_data, "darkweb_site_1")

    asyncio.run(main())
