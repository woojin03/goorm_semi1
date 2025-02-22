import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# ✅ Discord Bot 설정 (긴급 알람 & 보고서 전송 채널 통합)
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # 디스코드 봇 토큰
DISCORD_ALERT_CHANNEL = int(os.getenv("DISCORD_ALERT_CHANNEL", 1234567890))  # 알람 & 보고서 전송 채널

# ✅ MongoDB 설정
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:1234@mongodb:27017/admin")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "darkweb_data")

# ✅ Elasticsearch 설정
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "darkweb_records")

# ✅ 크롤러 설정
CRAWLER_INTERVAL = int(os.getenv("CRAWLER_INTERVAL", 30))  # 기본 30분 간격 실행
TOR_PROXY = os.getenv("TOR_PROXY", "socks5h://localhost:9050")  # Tor 프록시 설정

# ✅ 보고서 설정
REPORT_TIME = os.getenv("REPORT_TIME", "00:00")  # 매일 00:00 보고서 생성
REPORT_PATH = os.getenv("REPORT_PATH", "reports/daily_report.html")  # 보고서 저장 경로

# ✅ 기타 설정
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"  # 디버그 모드 여부
