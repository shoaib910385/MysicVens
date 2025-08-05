import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from SHUKLAMUSIC import app, YouTube
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.utils.stream.stream import stream
from SHUKLAMUSIC.utils.decorators.language import LanguageStart

# Stores current guessing game sessions per chat
guess_sessions = {}

# List of song titles and URLs
GUESS_SONGS = [
    {"Saiyaar": "Saiyaara", "url": "https://www.youtube.com/watch?v=dvYMyqO2PZg"},
    {"qatal": "Qatal", "url": "https://www.youtube.com/watch?v=pbxgHqPizRg"},
    {"baby doll": "Baby Doll", "url": "https://www.youtube.com/watch?v=ZKzuh0AQSBI"},
    {"pink lips": "Pink Lips", "url": "https://www.youtube.com/watch?v=KJhL7U95Ug8"},
    {"tu jaane na": "Tu Jaane Na", "url": "https://www.youtube.com/watch?v=WoBFeCRfV20"},
    {"offo": "Offo", "url": "https://www.youtube.com/watch?v=ghzMGkZC4nY"},
    {"attention": "Attention", "url": "https://www.youtube.com/watch?v=nfs8NYg7yQM"},
    {"pal pal dil ke paas": "Pal Pal Dil Ke Paas", "url": "https://www.youtube.com/watch?v=az4R5G5v1bA"},
    {"zaroorat": "Zaroorat", "url": "https://www.youtube.com/watch?v=GzU8KqOY8YA"},
]

@app.on_message(filters.command("guesssong") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_guess_song(client, message: Message, _):
    chat_id = message.chat.id

    if chat_id in guess_sessions:
        return await message.reply_text("⚠️ A guessing game is already running!")

    song = random.choice(GUESS_SONGS)
    title = song["title"].strip().lower()
    video_id = song["url"].split("v=")[-1]

    try:
        details, _id = await YouTube.track(video_id)
    except Exception as e:
        return await message.reply_text("❌ Couldn't fetch the song. Try again.")

    # Save session
    guess_sessions[chat_id] = {
        "answer": title,
        "guessed": False,
        "winner": None,
    }

    await message.reply_text(
        "🎵 A song is now playing in VC.\n\nGuess the song title using:\n`/guess your answer`\n\nYou have 30 seconds!"
    )

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

    # Let it play 10s, then stop VC
    await asyncio.sleep(10)
    try:
        await SHUKLA.leave_group_call(chat_id)
    except:
        pass

    # Wait 20s more for guesses
    await asyncio.sleep(20)

    session = guess_sessions.get(chat_id)
    if session and not session["guessed"]:
        await message.reply_text(
            f"⏱ Time's up! No one guessed it.\n✅ Correct answer: `{song['title']}`"
        )

    guess_sessions.pop(chat_id, None)


@app.on_message(filters.command("guess") & filters.group & ~BANNED_USERS)
async def check_guess(client, message: Message):
    chat_id = message.chat.id
    session = guess_sessions.get(chat_id)

    if not session or session["guessed"]:
        return

    user_guess = message.text.split(" ", 1)
    if len(user_guess) < 2:
        return await message.reply_text("❗Usage: `/guess your answer`", quote=True)

    guess = user_guess[1].strip().lower()
    correct = session["answer"]

    if correct in guess:
        session["guessed"] = True
        session["winner"] = message.from_user.mention
        await message.reply_text(
            f"🎉 {session['winner']} guessed it right!\n✅ Answer: `{correct.title()}`"
        )
        guess_sessions.pop(chat_id, None)
