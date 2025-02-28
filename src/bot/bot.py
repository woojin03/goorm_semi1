# bot.py
import discord
from discord.ext import commands, tasks
from database.database_mongo import db
import os
from dotenv import load_dotenv


# 환경 변수 로드
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # 메시지를 보낼 채널 ID 환경변수로 설정

# MongoDB 컬렉션을 `discord_user`로 변경
keywords_collection = db["discord_user"]

intents = discord.Intents.default()
intents.message_content = True  # 메시지 읽기 활성화
intents.presences = True  # Presence Intent 활성화
intents.members = True  # Server Members Intent 활성화
intents.dm_messages = True  # DM 메시지 전송 가능하게 설정
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 디스코드 봇 `{bot.user.name}` 실행됨!")

        # 주기적으로 메시지를 보내는 작업 시작
    if not send_periodic_message.is_running():
        send_periodic_message.start()

@tasks.loop(hours=1)  # 1시간마다 실행
async def send_periodic_message():
    """1시간마다 채널에 키워드 사용법 안내 메시지 전송"""
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        help_message = (
            "** 디스코드 키워드 알림 봇 사용법 **\n\n"
            "✅ 키워드 추가: `!키워드추가 <키워드>`\n"
            "✅ 키워드 목록 확인: `!키워드목록`\n"
            "✅ 키워드 삭제: `!키워드삭제 <키워드>`\n\n"
            " 등록한 키워드가 포함된 메시지가 감지되면 자동으로 DM으로 알림이 전송됩니다!"
        )
        await channel.send(help_message)
        print(f"✅ {channel.name} 채널에 안내 메시지 전송 완료!")
    else:
        print("⚠️ 채널을 찾을 수 없습니다. 채널 ID를 확인하세요.")


@bot.command(name="키워드추가")
async def add_keyword(ctx, *, keyword):
    """사용자가 키워드를 등록하는 기능 (중복 방지)"""
    user_id = int(ctx.author.id)  # `int` 타입으로 변환
    existing_keyword = await keywords_collection.find_one({"user_id": user_id, "keyword": keyword})

    if existing_keyword:
        await ctx.send(f"⚠️ 키워드 `{keyword}`는 이미 등록되어 있습니다!")
    else:
        await keywords_collection.insert_one({"user_id": user_id, "keyword": keyword})
        await ctx.send(f"✅ 키워드 `{keyword}` 추가 완료!")


@bot.command(name="키워드목록")
async def list_keywords(ctx):
    """사용자가 등록한 키워드를 출력"""
    user_id = int(ctx.author.id)  # `int` 타입으로 변환
    keywords = [doc["keyword"] async for doc in keywords_collection.find({"user_id": user_id})]

    if keywords:
        await ctx.send(f" 등록된 키워드: {', '.join(keywords)}")
    else:
        await ctx.send("⚠️ 등록된 키워드가 없습니다!")

@bot.command(name="키워드삭제")
async def remove_keyword(ctx, *, keyword):
    """사용자가 등록한 키워드를 삭제"""
    user_id = int(ctx.author.id)  # `int` 타입으로 변환
    result = await keywords_collection.delete_one({"user_id": user_id, "keyword": keyword})

    if result.deleted_count > 0:
        await ctx.send(f"️ 키워드 `{keyword}` 삭제 완료!")
    else:
        await ctx.send(f"⚠️ 키워드 `{keyword}`를 찾을 수 없습니다!")


async def send_discord_alert(user_id, keyword, data, timestamp):
    """ 키워드 포함된 메시지를 디스코드 유저에게 DM으로 전송 (유저 검색 예외 처리 강화) """
    try:
        user = bot.get_user(user_id)
        if user is None:
            try:
                user = await bot.fetch_user(user_id)  # ✅ 안전하게 유저 가져오기
            except discord.NotFound:
                print(f"⚠️ 디스코드 유저 `{user_id}`를 찾을 수 없습니다. (유효하지 않은 ID)")
                return
            except discord.Forbidden:
                print(f"⚠️ `{user_id}` 유저가 봇의 DM을 차단했거나 접근 권한이 없음.")
                return
            except discord.HTTPException as e:
                print(f"⚠️ 유저 `{user_id}` 정보를 가져오는 중 오류 발생: {e}")
                return

        if user:
            # ✅ 메시지 내용 처리
            title = data.get("title", "")
            description = data.get("description", "")
            message_text = data.get("message_text", "")

            if not message_text:
                message_text = f"**제목:** {title}\n**설명:** {description}"

            discord_message = (
                f"🔍 키워드 `{keyword}` 가 포함된 메시지 감지됨!\n\n"
                f"📅 시간: {timestamp}\n"
                f"📜 내용: {message_text}"
            )

            await user.send(discord_message)
            print(f"✅ 디스코드 알림 전송 완료: {keyword} → {user_id}")

        else:
            print(f"⚠️ 디스코드 유저 `{user_id}`를 찾을 수 없음.")

    except discord.Forbidden:
        print(f"⚠️ `{user_id}` 유저가 DM을 차단했거나, 봇이 DM을 보낼 권한이 없음.")
    except discord.HTTPException as e:
        print(f"⚠️ 디스코드 메시지 전송 중 오류 발생: {e}")
    except Exception as e:
        print(f"⚠️ 디스코드 알림 전송 오류: {e}")
