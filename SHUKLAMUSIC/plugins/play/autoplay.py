import random
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from SHUKLAMUSIC import app, YouTube, SHUKLA
from SHUKLAMUSIC.utils.stream.stream import stream
from SHUKLAMUSIC.utils.decorators.language import LanguageStart

# Tracks autoplay state per chat
autoplay_sessions = {}

# Hindi/popular songs list
TRENDING_SONGS = [
    "https://www.youtube.com/watch?v=dvYMyqO2PZg",  # Saiyaara
    "https://www.youtube.com/watch?v=pbxgHqPizRg",  # Qatal
    "https://www.youtube.com/watch?v=ZKzuh0AQSBI",  # Baby Doll
    "https://www.youtube.com/watch?v=KJhL7U95Ug8",  # Pink Lips
    "https://www.youtube.com/watch?v=WoBFeCRfV20",  # Tu Jaane Na
    "https://www.youtube.com/watch?v=ghzMGkZC4nY",  # Offo
    "https://www.youtube.com/watch?v=j5uXpKoP_xk",  # Die with a Smile
    "https://www.youtube.com/watch?v=nfs8NYg7yQM",  # Attention
    "https://www.youtube.com/watch?v=az4R5G5v1bA",  # Pal Pal Dil Ke Paas
    "https://www.youtube.com/watch?v=GzU8KqOY8YA",  # Zaroorat
]


# ▶️ Start autoplay
@app.on_message(filters.command("autoplay") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_autoplay(client, message: Message, _):
    chat_id = message.chat.id
    user = message.from_user

    # Pick 5 random songs
    selected = random.sample(TRENDING_SONGS, 5)
    autoplay_sessions[chat_id] = {
        "songs": selected,
        "index": 0,
        "user_id": user.id,
        "user_name": user.first_name,
        "start_msg": None,
    }

    start_msg = await message.reply_text("▶️ Started Autoplay. Playing 5 trending songs...")
    autoplay_sessions[chat_id]["start_msg"] = start_msg

    await play_next_autoplay(chat_id, _)


# ⏭ Play next song automatically
async def play_next_autoplay(chat_id, _):
    session = autoplay_sessions.get(chat_id)
    if not session:
        return

    if session["index"] >= len(session["songs"]):
        # End autoplay
        if session.get("start_msg"):
            try:
                await session["start_msg"].reply("✅ Autoplay finished after 5 songs.")
            except:
                pass
        autoplay_sessions.pop(chat_id, None)
        return

    url = session["songs"][session["index"]]
    session["index"] += 1

    try:
        details, _id = await YouTube.track(url)
    except Exception:
        return await play_next_autoplay(chat_id, _)  # skip and move to next

    try:
        await stream(
            _,
            None,  # no separate stream start message
            session["user_id"],
            details,
            chat_id,
            session["user_name"],
            chat_id,
            streamtype="youtube",
        )
    except Exception:
        return await play_next_autoplay(chat_id, _)  # skip and move to next


# 🔚 When stream ends, move to next
@SHUKLA.on_stream_end
async def stream_end_handler(_, client, stream_data, chat_id):
    if chat_id in autoplay_sessions:
        await play_next_autoplay(chat_id, _)


# ⛔️ Stop autoplay
@app.on_message(filters.command("stopautoplay") & filters.group & ~BANNED_USERS)
@LanguageStart
async def stop_autoplay_handler(client, message: Message, _):
    chat_id = message.chat.id

    if chat_id in autoplay_sessions:
        autoplay_sessions.pop(chat_id)
        await message.reply_text("⛔️ Autoplay has been stopped manually.")
    else:
        await message.reply_text("❌ There is no active autoplay running.")
