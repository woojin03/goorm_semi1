import os
import discord
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from urllib.parse import quote

# ✅ 환경 변수 로드
load_dotenv()

# ✅ 환경 변수 가져오기
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_REPORT_ID = os.getenv("DISCORD_REPORT_CHANNEL_ID")

# ✅ 환경 변수 확인 (오류 방지)
if not TOKEN:
    raise ValueError("⚠️ 환경 변수 `DISCORD_TOKEN`이 설정되지 않았습니다!")
if not CHANNEL_REPORT_ID:
    raise ValueError("⚠️ 환경 변수 `DISCORD_REPORT_CHANNEL_ID`이 설정되지 않았습니다!")

CHANNEL_REPORT_ID = int(CHANNEL_REPORT_ID)  # int 변환

async def convert_html_to_pdf(html_path, output_pdf_path):
    """ HTML 파일을 PDF로 변환하는 비동기 함수 (Playwright 사용) """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            absolute_html_path = os.path.abspath(html_path)  # 절대 경로 설정
            encoded_html_path = quote(absolute_html_path)  # URL 인코딩
            await page.goto(f"file://{encoded_html_path}")
            await page.pdf(path=output_pdf_path, format="A4")
            print(f"✅ HTML → PDF 변환 완료: {output_pdf_path}")
            await browser.close()
            return True
    except Exception as e:
        print(f"❌ PDF 변환 실패: {e}")
        return False

async def send_report(bot):
    """ news.html을 PDF로 변환 후, 디스코드 채널에 전송 """
    html_path = "src/services/sample_news.html"
    pdf_path = "src/services/sample_report.pdf"

    if not os.path.exists(html_path):
        print("❌ `news.html` 파일이 존재하지 않음!")
        return

    await bot.wait_until_ready()  # ✅ 디스코드 봇이 완전히 실행될 때까지 대기

    try:
        success = await convert_html_to_pdf(html_path, pdf_path)
        if success:
            channel = bot.get_channel(CHANNEL_REPORT_ID)
            if channel:
                await channel.send("📄 **오늘의 다크웹 리포트 (PDF)**", file=discord.File(pdf_path, filename="sample_report.pdf"))
                print("✅ HTML PDF 파일이 디스코드 채널에 전송됨!")
            else:
                print("⚠️ 채널을 찾을 수 없습니다!")
        else:
            print("⚠️ PDF 변환에 실패하였습니다!")
    except Exception as e:
        print(f"❌ 파일 처리 중 오류 발생: {e}")



#pip install playwright
#playwright install