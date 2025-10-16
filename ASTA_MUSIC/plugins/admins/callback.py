import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ASTA_MUSIC import YouTube, app
from ASTA_MUSIC.core.call import ASTA
from ASTA_MUSIC.misc import SUDOERS, db
from ASTA_MUSIC.utils.database import (
    get_active_chats,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_music_playing,
    is_nonadmin_chat,
    music_off,
    music_on,
    set_loop,
)
from ASTA_MUSIC.utils.decorators.language import languageCB
from ASTA_MUSIC.utils.formatters import seconds_to_min
from ASTA_MUSIC.utils.inline import (
    close_markup,
    stream_markup,
    stream_markup_timer,
)
from ASTA_MUSIC.utils.stream.autoclear import auto_clean
from ASTA_MUSIC.utils.thumbnails import get_thumb
from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
    confirmer,
    votemode,
)
from strings import get_string

checker = {}
upvoters = {}


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
    mention = CallbackQuery.from_user.mention

    # --- Upvote section ---
    if command == "UpVote":
        if chat_id not in votemode:
            votemode[chat_id] = {}
        if chat_id not in upvoters:
            upvoters[chat_id] = {}

        voters = upvoters[chat_id].get(CallbackQuery.message.id)
        if not voters:
            upvoters[chat_id][CallbackQuery.message.id] = []

        vote = votemode[chat_id].get(CallbackQuery.message.id)
        if not vote:
            votemode[chat_id][CallbackQuery.message.id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            upvoters[chat_id][CallbackQuery.message.id].remove(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            upvoters[chat_id][CallbackQuery.message.id].append(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] += 1

        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.id])

        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]
            except:
                return await CallbackQuery.edit_message_text("ғᴀɪʟᴇᴅ.")
            try:
                if current["vidid"] != exists["vidid"] or current["file"] != exists["file"]:
                    return await CallbackQuery.edit_message_text(_["admin_35"])
            except:
                return await CallbackQuery.edit_message_text(_["admin_36"])
            await CallbackQuery.edit_message_text(_["admin_37"].format(upvote))
        else:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"👍 {get_upvotes}",
                            callback_data=f"ADMIN UpVote|{chat_id}_{counter}",
                        )
                    ]
                ]
            )
            await CallbackQuery.answer(_["admin_40"], show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)

    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                admins = adminlist.get(CallbackQuery.message.chat.id)
                if not admins or CallbackQuery.from_user.id not in admins:
                    return await CallbackQuery.answer(_["admin_14"], show_alert=True)

    # --- Controls ---
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await music_off(chat_id)
        await ASTA.pause_stream(chat_id)
        return await CallbackQuery.message.reply_text(_["admin_2"].format(mention))

    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await music_on(chat_id)
        await ASTA.resume_stream(chat_id)
        return await CallbackQuery.message.reply_text(_["admin_4"].format(mention))

    elif command in ["Stop", "End"]:
        await ASTA.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        return await CallbackQuery.message.reply_text(_["admin_5"].format(mention))

    elif command in ["Skip", "Replay"]:
        check = db.get(chat_id)
        if not check:
            return await CallbackQuery.answer("Queue empty!", show_alert=True)
        txt = (
            f"➻ sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ 🎄\n│ \n└ʙʏ : {mention} 🥀"
            if command == "Skip"
            else f"➻ sᴛʀᴇᴀᴍ ʀᴇ-ᴘʟᴀʏᴇᴅ 🎄\n│ \n└ʙʏ : {mention} 🥀"
        )

        if command == "Skip":
            popped = None
            try:
                popped = check.pop(0)
                if popped:
                    await auto_clean(popped)
            except:
                pass
            if not check:
                await CallbackQuery.edit_message_text(txt)
                await CallbackQuery.message.reply_text(
                    _["admin_6"].format(mention, CallbackQuery.message.chat.title)
                )
                return await ASTA.stop_stream(chat_id)

        queued = check[0]["file"]
        title = check[0]["title"].title()
        user = check[0]["by"]
        duration = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0

        try:
            img = await get_thumb(videoid)
        except:
            img = STREAM_IMG_URL

        button = stream_markup(_, videoid, chat_id)
        run = await CallbackQuery.message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(
                f"https://t.me/{app.username}?start=info_{videoid}",
                title[:23],
                duration,
                user,
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"
        await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))


# --- Timer for Markup Updates ---
async def markup_timer():
    while not await asyncio.sleep(4):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                if not await is_music_playing(chat_id):
                    continue
                playing = db.get(chat_id)
                if not playing:
                    continue
                duration_seconds = int(playing[0]["seconds"])
                if duration_seconds == 0:
                    continue
                mystic = playing[0].get("mystic")
                markup = playing[0].get("markup")
                if not mystic or not markup:
                    continue
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")

                buttons = stream_markup_timer(
                    _,
                    playing[0]["vidid"],
                    chat_id,
                    seconds_to_min(playing[0]["played"]),
                    playing[0]["dur"],
                )
                await mystic.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
            except:
                continue


asyncio.create_task(markup_timer())
