import asyncio
import time
from elasticsearch import AsyncElasticsearch

# ✅ 수정된 Elasticsearch 연결 설정 (도커 네트워크 호스트명 사용)
ELASTICSEARCH_HOST = "http://elasticsearch:9200"
es_client = AsyncElasticsearch([ELASTICSEARCH_HOST])

# ✅ 6개의 다크웹 크롤링 데이터 인덱스 목록
darkweb_indices = [
    "darkweb_site_1",
    "darkweb_site_2",
    "darkweb_site_3",
    "darkweb_site_4",
    "darkweb_site_5",
    "darkweb_site_6"
]

async def wait_for_elasticsearch():
    """Elasticsearch가 실행될 때까지 대기"""
    while True:
        try:
            if await es_client.ping():
                print("✅ Elasticsearch가 실행되었습니다!")
                return
        except:
            print("⏳ Elasticsearch가 아직 준비되지 않았습니다. 재시도 중...")
            time.sleep(5)  # 5초 대기 후 재시도

async def create_index(index_name):
    """Elasticsearch 인덱스 생성 (이미 존재하면 스킵)"""
    exists = await es_client.indices.exists(index=index_name)
    if not exists:
        await es_client.indices.create(index=index_name)
        print(f"✅ Elasticsearch 인덱스 생성 완료: {index_name}")
    else:
        print(f"⚠️ Elasticsearch 인덱스 이미 존재: {index_name}")

async def main():
    await wait_for_elasticsearch()  # ✅ Elasticsearch가 실행될 때까지 대기
    for index in darkweb_indices:
        await create_index(index)
    await es_client.close()

if __name__ == "__main__":
    asyncio.run(main())
