import requests

PROXIES = {
    "http": "socks5h://localhost:9050",
    "https": "socks5h://localhost:9050"
}

try:
    response = requests.get("http://check.torproject.org", proxies=PROXIES, timeout=10)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"❌ Tor 프록시 연결 실패: {e}")
