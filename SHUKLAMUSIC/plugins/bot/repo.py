from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SHUKLAMUSIC import app
from config import BOT_USERNAME
from SHUKLAMUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
❥ ωєℓ¢σмє тσ 𒌋❰𝗗𝗥𝗫❱™

❥ ʀᴇᴘᴏ ᴄʜᴀᴀʜɪʏʀ ᴛᴏ ʙᴏᴛ ᴋᴏ 

❥ 5 ɢᴄ ᴍᴀɪ ᴀᴅᴅ ᴋᴀʀ ᴋᴇ 

❥ ᴀᴅᴍɪɴ ʙᴀɴᴏ ᴀᴜʀ sᴄʀᴇᴇɴsʜᴏᴛ 
     
❥ @HEHE_STALKER ᴋᴏ ᴅᴏ ғɪʀ ʀᴇᴘᴏ ᴍɪʟ sᴀᴋᴛɪ ʜᴀɪ 

"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("♡ α∂∂ иσω ♡", url=f"https://t.me/tidalxmusicbot?startgroup=true")
        ],
        [
          InlineKeyboardButton("ѕυρρσɾƚ", url="https://t.me/drx_supportchat"),
          InlineKeyboardButton("愛|𝗦𝗧么𝗟𝗞𝚵𝗥™", url="https://t.me/hehe_stalker"),
          ],
               [
                InlineKeyboardButton("𒌋❰𝗗𝗥𝗫❱™", url=f"https://t.me/thedrxnet"),
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
