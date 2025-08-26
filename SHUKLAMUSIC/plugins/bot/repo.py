from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SHUKLAMUSIC import app
from config import BOT_USERNAME
from SHUKLAMUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
Jᴀᴀ ʜᴀɪ ᴘᴀᴅʜᴀɪ ᴋʀ Jᴀᴀᴋᴇ ᴀᴀʏᴀ ʙᴀᴅᴀ ʀᴇᴘᴏ ᴅᴇᴋʜɴᴇ ᴡᴀʟᴀ !
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("♡ α∂∂ иσω ♡", url=f"https://t.me/tidalxmusicbot?startgroup=true")
        ],
        [
          InlineKeyboardButton("˹ϻʏ ʜᴏϻє˼", url="https://t.me/drx_supportchat"),
          InlineKeyboardButton("˹ ϻʏ ϻᴧsᴛєʀ ˼ 👑", url="https://t.me/hehe_stalker"),
          ],
               [
                InlineKeyboardButton("˹ηєᴛᴡᴏʀᴋ˼", url=f"https://t.me/thedrxnet"),
],
[
InlineKeyboardButton("ᴄʜᴇᴄᴋ", url=f"https://t.me/tidalxmusicbot"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://files.catbox.moe/wifnjm.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
