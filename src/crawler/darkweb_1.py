import aiohttp
import asyncio
from bs4 import BeautifulSoup
import aiohttp_socks  # SOCKS5 프록시 지원 패키지
from datetime import datetime, timezone

# 1. 크롤링할 .onion 사이트 URL
url = "http://rnsm777cdsjrsdlbs4v5qoeppu3px6sb2igmh53jzrx7ipcrbjz5b2ad.onion/"

# 2. HTTP 요청 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 3. SOCKS5 프록시 설정 (Tor 네트워크 사용)
proxy_url = "socks5://127.0.0.1:9050"

async def crawl_darkweb1():
    """
    🕵️‍♂️ 비동기 방식으로 다크웹 크롤링 후 데이터 반환
    - 페이지 요청 후 HTML 파싱하여 데이터 추출
    - 데이터를 리스트로 반환 (출력 없음)
    - 크롤링이 끝나면 완료 메시지 출력
    """
    connector = aiohttp_socks.ProxyConnector.from_url(proxy_url)

    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers, timeout=30) as response:
                response.raise_for_status()
                html = await response.text()
    except aiohttp.ClientError:
        print("❌ 크롤링 실패: 페이지 요청 오류")  # 🚨 실패 시 메시지 출력
        return []  # 실패 시 빈 리스트 반환

    # 🔹 HTML 파싱
    soup = BeautifulSoup(html, "html.parser")
    leak_data_1 = []

    # 🔹 ol 태그 내의 li 태그에서 데이터 추출
    for ol in soup.find_all("ol"):
        for li in ol.find_all("li"):
            title = li.find("h4").get_text(strip=True) if li.find("h4") else "제목 없음"
            description = li.find("p").get_text(strip=True) if li.find("p") else "유출 정보 없음"
            insert_time = datetime.now(timezone.utc).isoformat()

            # 데이터 저장 (출력 없이 리스트에 저장)
            leak_data_1.append({"title": title, "description": description, "insert_time": insert_time})

    print(f"🔍 {len(leak_data_1)}개의 데이터가 크롤링되었습니다.")
    return leak_data_1  # ✅ 리스트 형태로 반환 (출력 없음)
