import re

def clean_message(text):
    """ 텔레그램 메시지를 정리하는 파서 """
    text = re.sub(r"[🔴⚠️🚨🆘❗️🔎📩✅⏳]", "", text)  # ✅ 불필요한 이모지 제거
    text = re.sub(r"\s{2,}", "\n", text)  # 2개 이상의 연속된 공백을 줄바꿈(\n)으로 변경
    text = re.sub(r"\n{2,}", "\n", text)  # 2줄 이상의 연속된 줄바꿈을 1줄로 축소
    text = text.strip()  # 앞뒤 공백 제거
    return text


# 불필요한 문자제거를 위한 파서