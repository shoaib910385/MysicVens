import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from SHUKLAMUSIC import app, YouTube
from SHUKLAMUSIC.utils.stream.stream import stream
from SHUKLAMUSIC.utils.decorators.language import LanguageStart

# Tracks ongoing game sessions: {chat_id: {"answer": str, "active": bool}}
guess_sessions = {}

# Song list for guessing (name + url)
GUESS_SONGS = [
    {"title": "Saiyaara", "url": "https://www.youtube.com/watch?v=dvYMyqO2PZg"},
    {"title": "Qatal", "url": "https://www.youtube.com/watch?v=pbxgHqPizRg"},
    {"title": "Baby Doll", "url": "https://www.youtube.com/watch?v=ZKzuh0AQSBI"},
    {"title": "Pink Lips", "url": "https://www.youtube.com/watch?v=KJhL7U95Ug8"},
    {"title": "Tu Jaane Na", "url": "https://www.youtube.com/watch?v=WoBFeCRfV20"},
    {"title": "Offo", "url": "https://www.youtube.com/watch?v=ghzMGkZC4nY"},
    {"title": "Attention", "url": "https://www.youtube.com/watch?v=nfs8NYg7yQM"},
    {"title": "Pal Pal Dil Ke Paas", "url": "https://www.youtube.com/watch?v=az4R5G5v1bA"},
    {"title": "Zaroorat", "url": "https://www.youtube.com/watch?v=GzU8KqOY8YA"},
]

@app.on_message(filters.command("guesssong") & filters.group & ~BANNED_USERS)
@LanguageStart
async def guess_song_game(client, message: Message, _):
    chat_id = message.chat.id

    if guess_sessions.get(chat_id, {}).get("active"):
        return await message.reply_text("❗ A guessing game is already in progress!")

    # Pick a random song
    song = random.choice(GUESS_SONGS)
    guess_sessions[chat_id] = {
        "answer": song["title"].lower(),
        "active": True,
        "winner": None
    }

    # Fetch stream data
    try:
        details, _id = await YouTube.track(song["url"])
    except Exception as e:
        guess_sessions.pop(chat_id, None)
        return await message.reply_text("❌ Couldn't fetch the song, try again.")

    # Announce game start
    await message.reply_text("🎵 Guess The Song!\nI've started playing 10 seconds of a song in VC. First to guess wins!\n\nType the name of the song in chat!")

    # Start stream
    try:
        await stream(
            _,
            None,
            message.from_user.id,
            details,
            chat_id,
            message.from_user.first_name,
            chat_id,
            streamtype="youtube",
        )
    except Exception:
        guess_sessions.pop(chat_id, None)
        return await message.reply_text("❌ Failed to stream the song.")

    # Wait 10 seconds (play preview)
    await asyncio.sleep(10)

    # Stop music after 10s
    from SHUKLAMUSIC.core.call import SHUKLA
    await SHUKLA.leave_group_call(chat_id)

    # Wait 20 more seconds for guesses
    await asyncio.sleep(20)

    # Game End
    if guess_sessions[chat_id]["winner"]:
        winner = guess_sessions[chat_id]["winner"]
        await app.send_message(chat_id, f"🏆 {winner} guessed it right!\n✅ Answer: `{song['title']}`")
    else:
        await app.send_message(chat_id, f"⏱ Time's up!\n❌ No one guessed it.\nCorrect Answer: `{song['title']}`")

    guess_sessions.pop(chat_id, None)


@app.on_message(filters.text & filters.group & ~BANNED_USERS)
async def check_guess(client, message: Message):
    chat_id = message.chat.id
    session = guess_sessions.get(chat_id)

    if not session or not session.get("active"):
        return

    guess = message.text.lower().strip()
    correct = session["answer"]

    if correct in guess:
        session["active"] = False
        session["winner"] = message.from_user.mention
