import os
from dotenv import load_dotenv

# .env 파일 로드
#load_dotenv()

# .env 파일 경로를 명확하게 지정
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)  # .env 파일 로드


#텔레그램 API
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "").split(",")

# ✅ Discord Bot 설정 (긴급 알람 & 보고서 전송 채널 통합)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # 디스코드 봇 토큰
#DISCORD_ALERT_CHANNEL = int(os.getenv("DISCORD_ALERT_CHANNEL", 1234567890))  # 알람 & 보고서 전송 채널

# ✅ MongoDB 설정
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:1234@mongodb:27017/admin")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "darkweb_data")

# ✅ Elasticsearch 설정
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "darkweb_records")

# ✅ 크롤러 설정
# ✅ CRAWLER_INTERVAL을 초 단위로 설정 (변환 필요 없음)
#CRAWLER_INTERVAL = int(os.getenv("CRAWLER_INTERVAL", 1800))  # 기본값: 1800초 (30분)
# ✅ CRAWLER_INTERVAL 값을 안전하게 변환 (예외 처리 추가)
try:
    CRAWLER_INTERVAL = int(os.getenv("CRAWLER_INTERVAL", 1800))  # 기본값: 1800초 (30분)
except ValueError:
    print("⚠️ CRAWLER_INTERVAL 값이 올바르지 않습니다. 기본값(1800초) 사용")
    CRAWLER_INTERVAL = 1800  # 기본값 사용
TOR_PROXY = os.getenv("TOR_PROXY", "socks5h://localhost:9050")  # Tor 프록시 설정

# ✅ 보고서 설정
REPORT_TIME = os.getenv("REPORT_TIME", "00:00")  # 매일 00:00 보고서 생성
REPORT_PATH = os.getenv("REPORT_PATH", "reports/daily_report.html")  # 보고서 저장 경로

# ✅ 기타 설정
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"  # 디버그 모드 여부
