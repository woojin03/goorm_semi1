import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector  # ✅ SOCKS5 프록시 직접 설정
from bs4 import BeautifulSoup
from datetime import datetime, timezone

# 1️⃣ 크롤링할 다크웹 URL
url = "http://7ukmkdtyxdkdivtjad57klqnd3kdsmq6tp45rrsxqnu76zzv3jvitlqd.onion/"

# 2️⃣ HTTP 요청 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 3️⃣ SOCKS5 프록시 설정 (Tor 네트워크 사용)
proxy_host = "127.0.0.1"
proxy_port = 9050

async def crawl_darkweb2():
    """ 다크웹 크롤링 함수 - 비동기 방식으로 크롤링한 데이터를 리스트로 반환 """
    try:
        # 🔹 SOCKS5 프록시 커넥터 수동 설정
        connector = ProxyConnector.from_url(f"socks5://{proxy_host}:{proxy_port}")

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers, timeout=30) as response:
                response.raise_for_status()  # HTTP 오류 체크
                html = await response.text()  # 비동기 방식으로 HTML 가져오기
                print("✅ 페이지 요청 성공!")

    except aiohttp.ClientError as e:
        print(f"❌ 페이지 요청 실패: {e}")
        return []  # 오류 발생 시 빈 리스트 반환

    # 🔹 HTML 파싱
    soup = BeautifulSoup(html, "html.parser")
    leak_data_2 = []

    # 🔹 각 카드 데이터 크롤링
    for card in soup.find_all("div", class_="border border-warning card-body shadow-lg"):
        title = card.find("h4", class_="border-danger card-title text-start text-white")
        title_text = title.get_text(strip=True) if title else "제목 없음"

        website_tag = card.find("h6", class_="card-subtitle mb-2 text-muted text-start")
        website_link = website_tag.find("a")["href"] if website_tag and website_tag.find("a") else "링크 없음"

        description = card.find("p", class_="card-text text-start text-white")
        description_text = description.get_text(strip=True) if description else "설명 없음"

        insert_time = datetime.now(timezone.utc).isoformat()

        # 🔹 데이터 저장 (리스트에 추가)
        leak_data_2.append({
            "title": title_text,
            "website": website_link,
            "description": description_text,
            "insert_time": insert_time
        })

    print(f"🔍 {len(leak_data_2)}개의 데이터가 크롤링되었습니다.")
    return leak_data_2  # ✅ 리스트 형태로 반환
