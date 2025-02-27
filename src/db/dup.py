# dup_search.py
import asyncio
from elasticsearch import AsyncElasticsearch

# Elasticsearch 클라이언트 설정 (환경에 맞게 수정)
es = AsyncElasticsearch(hosts=["http://localhost:9200"])

async def dup_search(data: dict, index: str) -> int:
    """
    Elasticsearch 8.x 버전에서 victim_explan 또는 content 값을 검색하여 중복 여부를 판단합니다.
    매개변수:
      - data (dict): 검색 대상 데이터 (victim_explan 또는 content 필드를 포함해야 함)
      - index (str): 검색할 Elasticsearch 인덱스 이름
    반환:
      - 검색 결과가 하나라도 존재하면 1, 그렇지 않으면 0
    """
    # 검색 대상 필드 선택: victim_explan 또는 content
    if "victim_explan" in data:
        field = "victim_explan"
        value = data["victim_explan"]
    elif "content" in data:
        field = "content"
        value = data["content"]
    else:
        # 검색할 필드가 없으면 중복 여부 체크를 하지 않고 0 반환
        return 0

    # Elasticsearch match 쿼리 생성
    query = {
        "match": {
            field: value
        }
    }

    try:
        # 검색 수행 (ES 8.x에서는 query 매개변수를 사용)
        result = await es.search(index=index, query=query)
        # hits.total가 dict 형식 (예: {"value": N, "relation": "eq"})인 경우와 int인 경우 모두 처리
        total = result["hits"]["total"]
        count = total.get("value", 0) if isinstance(total, dict) else total

        return 1 if count > 0 else 0
    except Exception as e:
        print(f"dup_search 오류: {e}")
        return 0

# 간단한 테스트 예제
if __name__ == "__main__":
    async def main():
        # victim_explan 필드를 가진 테스트 데이터
        test_data = {
            "victim_title": "테스트 타이틀",
            "victim_site": "example.com",
            "victim_explan": "테스트 설명"
        }
        result = await dup_search(test_data, index="darkweb_site_1")
        print("dup_search 결과:", result)

    asyncio.run(main())
