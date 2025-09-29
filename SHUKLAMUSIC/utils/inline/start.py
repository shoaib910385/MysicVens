from pyrogram.types import InlineKeyboardButton

import config
from SHUKLAMUSIC import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton("˹ᴘσʟιᴄʏ˼", url=f"https://telegra.ph/PRIVACY-POLICY-09-29-68"),
    
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],

        [
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper"),
        ],
        [
            InlineKeyboardButton("˹ ϻʏ ϻᴧsᴛєʀ ˼ 👑", url=f"https://t.me/Imvalrik"),
        ],
    ]
    return buttons
    
    
