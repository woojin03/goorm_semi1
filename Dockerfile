# ✅ 1. 최신 Python 버전 사용
FROM python:3.12

# ✅ 2. 작업 디렉토리 설정
WORKDIR /app

# ✅ 3. 환경 변수 설정 (버그 방지: Python이 bytecode 생성 X, stdout 버퍼링 X)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# ✅ 4. 의존성 캐싱 최적화 (requirements.txt 변경이 없으면 재설치 생략)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 5. 프로젝트 전체 복사
COPY . .

# ✅ 6. 기본 실행 명령어 (현재 개발 단계에서는 실행 안 하므로 주석 가능)
# CMD ["python", "src/bot/bot.py"]
