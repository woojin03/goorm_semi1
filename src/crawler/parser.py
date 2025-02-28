import re

def clean_message(text):
    """ 텔레그램 메시지를 정리하는 파서 (문장 쪼개지는 문제 해결) """
    text = re.sub(r"\s{2,}", " ", text)  # ✅ 연속된 공백을 하나의 공백으로 변경
    text = text.strip()  # ✅ 앞뒤 공백 제거
    return text
