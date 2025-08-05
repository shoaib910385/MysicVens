import random
import asyncio
from urllib.parse import urlparse, parse_qs
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from SHUKLAMUSIC import app, YouTube
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.utils.stream.stream import stream
from SHUKLAMUSIC.utils.decorators.language import LanguageStart

# Stores guessing sessions
guess_sessions = {}

# Songs list
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

# Function to extract video ID
def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query).get('v', [None])[0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    return None

@app.on_message(filters.command("guesssong") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_guess_song(client, message: Message, _):
    chat_id = message.chat.id

    if chat_id in guess_sessions:
        return await message.reply_text("⚠️ A guessing game is already in progress!")

    # Pick a random song
    song = random.choice(GUESS_SONGS)
    answer = song["title"].strip().lower()
    video_id = extract_video_id(song["url"])
    if not video_id:
        return await message.reply_text("❌ Invalid YouTube link format.")

    try:
        details, _id = await YouTube.track(video_id)
    except Exception as e:
        return await message.reply_text("❌ Couldn't fetch the song. Try again.")

    # Store session
    guess_sessions[chat_id] = {
        "answer": answer,
        "guessed": False,
        "winner": None,
    }

    await message.reply_text(
        "🎧 Guess The Song Challenge!\nA song is now playing in VC.\nUse `/guess your answer` to win!\nYou have 30 seconds..."
    )

    # Start the stream
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

    await asyncio.sleep(10)
    try:
        await SHUKLA.leave_group_call(chat_id)
    except:
        pass

    await asyncio.sleep(20)
    session = guess_sessions.get(chat_id)
    if session and not session["guessed"]:
        await app.send_message(
            chat_id,
            f"⏱ Time's up! No one guessed it.\n✅ Correct answer: `{song['title']}`"
        )
        guess_sessions.pop(chat_id, None)

@app.on_message(filters.command("guess") & filters.group & ~BANNED_USERS)
async def handle_guess(client, message: Message):
    chat_id = message.chat.id
    session = guess_sessions.get(chat_id)

    if not session or session["guessed"]:
        return

    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return await message.reply("❗Usage: `/guess your answer`", quote=True)

    guess = parts[1].strip().lower()
    answer = session["answer"]

    if answer in guess:
        session["guessed"] = True
        session["winner"] = message.from_user.mention
        await message.reply(
            f"🎉 {session['winner']} guessed it right!\n✅ Answer: `{answer.title()}`"
        )
        guess_sessions.pop(chat_id, None)
