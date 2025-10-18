import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from ASTA_MUSIC import app
from ASTA_MUSIC.utils import BOT_USERNAME

@app.on_message(filters.command(["start"]) & filters.private)
async def start_private(client, message: Message):
    baby = await message.reply_text("**__ᴅɪηɢ ᴅᴏηɢ🥀__**")

    # ⚡ Fast smooth animation
    for dots in [".", "..", "..."]:
        try:
            await baby.edit_text(f"**__ᴅɪηɢ ᴅᴏηɢ{dots}🥀__**")
        except:
            pass
        await asyncio.sleep(0.15)

    await baby.edit_text("**__sᴛᴧʀᴛɪηɢ❤️‍🔥__**")
    await asyncio.sleep(0.4)
    await baby.edit_text("**__ʙσᴛ sᴛᴧʀᴛєᴅ💤__**")
    await asyncio.sleep(0.4)

    BUTTONS = [
        [
            InlineKeyboardButton("☞ 𝐆ʀσυρ ☜", url="https://t.me/oldskoolgc"),
            InlineKeyboardButton("☞ 𝐒υρρσʀᴛ ☜", url="https://t.me/ixasta1"),
        ],
        [
            InlineKeyboardButton("☞ 𝐀ᴅᴅ 𝐌ᴇ 𝐁ᴀʙʏ ☜", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
    ]

    caption = (
        "💫 **ʜєʏ ʙᴀʙʏ!**\n\n"
        "ɪ'ϻ **ʟᴀɪʙᴀ ᴍυsɪᴄ ʙσᴛ 🎵**\n"
        "ʀєᴀᴅʏ τσ ρʟᴀʏ sσηɢs ɪη γσυʀ ʜєᴀʀᴛ 💖\n\n"
        "ʙσᴛ ϻᴀᴅє ʙʏ ⋏ 𝛅 𝛕 ⋏ ☞"
    )

    await baby.edit_text(caption, reply_markup=InlineKeyboardMarkup(BUTTONS))


@app.on_message(filters.command(["start"]) & filters.group)
async def start_group(client, message: Message):
    await message.reply_text(
        f"**ʜєʏ {message.from_user.mention} 🌸**\n\n"
        f"ɪ'ϻ **ʟᴀɪʙᴀ ᴍυsɪᴄ ʙσᴛ 🎧**\n"
        f"ʀєᴀᴅʏ τσ ρʟᴀʏ ϻυsɪᴄ ɪη τʜɪs ɢʀσυρ 💫\n\n"
        f"ʙσᴛ ϻᴀᴅє ʙʏ ⋏ 𝛅 𝛕 ⋏ ☞",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("☞ 𝐆ʀσυρ ☜", url="https://t.me/oldskoolgc"),
                    InlineKeyboardButton("☞ 𝐒υρρσʀᴛ ☜", url="https://t.me/ixasta1"),
                ],
                [
                    InlineKeyboardButton("☞ 𝐀ᴅᴅ 𝐌ᴇ 𝐁ᴀʙʏ ☜", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                ],
            ]
        ),
    )
