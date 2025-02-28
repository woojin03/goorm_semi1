import json
import subprocess
import re
import os
from datetime import datetime

def run_elasticsearch_search():
    """elasticsearch_search.py 파일을 실행하여 최신 JSON 데이터를 생성"""
    try:
        SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "elasticsearch_search.py")
        subprocess.run(['python', SCRIPT_PATH], check=True)
        print("✅ Elasticsearch 데이터 json파일 저장 완료.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Elasticsearch 검색 스크립트 실행 중 오류 발생: {e}")

def update_html_with_data():
    """생성된 JSON 데이터(오늘, 지난주)를 읽어 HTML 파일(news.html)에 반영"""

    JSON_DIR = os.path.dirname(__file__)  # 현재 report.py가 있는 디렉토리
    today_data_path_1_2 = os.path.join(JSON_DIR, "today_data_1_2.json")
    today_data_path_3 = os.path.join(JSON_DIR, "today_data_3.json")
    last_week_data_path_1_2 = os.path.join(JSON_DIR, "last_week_data_1_2.json")
    last_week_data_path_3 = os.path.join(JSON_DIR, "last_week_data_3.json")
    html_path = os.path.join(JSON_DIR, "news.html")

    # JSON 파일 로드
    try:
        with open(today_data_path_1_2, 'r', encoding='utf-8') as f:
            today_data_1_2 = json.load(f)
        with open(today_data_path_3, 'r', encoding='utf-8') as f:
            today_data_3 = json.load(f)
        with open(last_week_data_path_1_2, 'r', encoding='utf-8') as f:
            last_week_data_1_2 = json.load(f)
        with open(last_week_data_path_3, 'r', encoding='utf-8') as f:
            last_week_data_3 = json.load(f)
    except FileNotFoundError as e:
        print(f"⚠️ JSON 파일을 찾을 수 없습니다: {e}")
        return

    # HTML 파일 읽기
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"⚠️ news.html 파일이 없습니다: {html_path}")
        return

    # 날짜 업데이트
    today_str = datetime.now().strftime("%B %d, %Y")
    html_content = re.sub(r'<p class="date" id="report-date">.*?</p>',
                          f'<p class="date" id="report-date">{today_str}</p>',
                          html_content, flags=re.DOTALL)

    # leak-count 업데이트
    leak_count = len(today_data_1_2) + len(today_data_3)
    html_content = re.sub(r'<span id="leak-count">.*?</span>',
                          f'<span id="leak-count">{leak_count}</span>',
                          html_content, flags=re.DOTALL)

    # HTML 파일 저장
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("✅ HTML 파일 업데이트 완료.")

'''if __name__ == "__main__":
    run_elasticsearch_search()
    update_html_with_data()'''
