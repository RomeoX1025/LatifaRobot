import html

from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from LatifaRobot import (
    DEV_USERS,
    LOGGER,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from LatifaRobot.modules.disable import DisableAbleCommandHandler
from LatifaRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
    can_delete,
)
from LatifaRobot.modules.helper_funcs.extraction import extract_user_and_text
from LatifaRobot.modules.helper_funcs.string_handling import extract_time
from LatifaRobot.modules.log_channel import gloggable, loggable


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def punch(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("⚠️ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            raise
        message.reply_text("⚠️ I ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʏᴇᴀʜʜʜ I'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴅᴏ ᴛʜᴀᴛ.")
        return log_message
    if is_user_ban_protected(chat, user_id):
        message.reply_text("I ʀᴇᴀʟʟʏ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ ᴘᴜɴᴄʜ ᴛʜɪs ᴜsᴇʀ....")
        return log_message
    if res := chat.unban_member(user_id):
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] Kicked by {mention_html(user.id, html.escape(user.first_name))}",
            parse_mode=ParseMode.HTML,
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#ᴋɪᴄᴋᴇᴅ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}"
        return log
    else:
        message.reply_text("⚠️ ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴘᴜɴᴄʜ ᴛʜᴀᴛ ᴜsᴇʀ.")
    return log_message


@bot_admin
@can_restrict
def punchme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("I ᴡɪsʜ I ᴄᴏᴜʟᴅ... ʙᴜᴛ ʏᴏᴜ'ʀᴇ ᴀɴ ᴀᴅᴍɪɴ .")
        return
    if res := update.effective_chat.unban_member(user_id):
        update.effective_message.reply_text(
            "ᴘᴜɴᴄʜᴇs ʏᴏᴜ ᴏᴜᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ !!",
        )
    else:
        update.effective_message.reply_text("ʜᴜʜ? I ᴄᴀɴ'ᴛ :/")


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> Optional[str]:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    if message.reply_to_message and message.reply_to_message.sender_chat:
        if r := bot.unban_chat_sender_chat(
            chat_id=chat.id,
            sender_chat_id=message.reply_to_message.sender_chat.id,
        ):
            message.reply_text(
                f"ᴄʜᴀɴɴᴇʟ {html.escape(message.reply_to_message.sender_chat.title)} ᴡᴀs ᴜɴʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ғʀᴏᴍ {html.escape(chat.title)}",
                parse_mode="html",
            )

        else:
            message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴜɴʙᴀɴ ᴄʜᴀɴɴᴇʟ")
        return
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("⚠️ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            raise
        message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴜɴʙᴀɴ ᴍʏsᴇʟғ ɪғ ɪ ᴡᴀsɴ'ᴛ ʜᴇʀᴇ...?")
        return log_message
    if is_user_in_chat(chat, user_id):
        message.reply_text("⚠️ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")
        return log_message
    chat.unban_member(user_id)
    message.reply_text(
        f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ᴡᴀs ᴜɴʙᴀɴɴᴇᴅ ʙʏ {mention_html(user.id, user.first_name)}",
        parse_mode=ParseMode.HTML,
    )
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴜɴʙᴀɴɴᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}"
    return log


@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    if user.id not in DRAGONS or user.id not in TIGERS:
        return
    try:
        chat_id = int(args[0])
    except:
        message.reply_text("ɢɪᴠᴇ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ.")
        return
    chat = bot.getChat(chat_id)
    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text("I ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ.")
            return
        else:
            raise
    if is_user_in_chat(chat, user.id):
        message.reply_text("Aren't you already in the chat??")
        return
    chat.unban_member(user.id)
    message.reply_text(f"ʏᴇᴘ, ɪ ʜᴀᴠᴇ ᴜɴʙᴀɴɴᴇᴅ ᴛʜᴇ ᴜsᴇʀ.")
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴜɴʙᴀɴɴᴇᴅ\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    return log


@bot_admin
@can_restrict
@loggable
def banme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("⚠️ I ᴄᴀɴɴᴏᴛ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ.")
        return
    if res := update.effective_chat.ban_member(user_id):
        update.effective_message.reply_text("ʏᴇs, ʏᴏᴜ'ʀᴇ ʀɪɢʜᴛ! ɢᴛғᴏ..")
        return f"<b>{html.escape(chat.title)}:</b>\n#ʙᴀɴᴍᴇ\n<b>ᴜsᴇʀ:</b> {mention_html(user.id, user.first_name)}\n<b>ɪᴅ:</b> <code>{user_id}</code>"

    else:
        update.effective_message.reply_text("Huh? I can't :/")


@dev_plus
def abishnoi(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ᴛᴏ ᴇᴄʜᴏ ᴛᴏ!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), to_send)
        except TelegramError:
            LOGGER.warning("ᴄᴏᴜʟᴅɴ'ᴛ sᴇɴᴅ ᴛᴏ ɢʀᴏᴜᴘ %s", chat_id)
            update.effective_message.reply_text(
                "ᴄᴏᴜʟᴅɴ'ᴛ sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ. ᴘᴇʀʜᴀᴘs ɪ'ᴍ ɴᴏᴛ ᴘᴀʀᴛ ᴏғ ᴛʜᴀᴛ ɢʀᴏᴜᴘ?"
            )


__help__ = """
*ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs:*
• /kickme*:* `ᴋɪᴄᴋs ᴛʜᴇ ᴜsᴇʀ ᴡʜᴏ ɪssᴜᴇᴅ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ `
• /banme*:* `ʙᴀɴs ᴛʜᴇ ᴜsᴇʀ ᴡʜᴏ ɪssᴜᴇᴅ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ `
*ᴀᴅᴍɪɴs ᴏɴʟʏ:*
• /ban <userhandle>*:*` ʙᴀɴs ᴀ ᴜsᴇʀ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ `
)
• /sban <ᴜsᴇʀʜᴀɴᴅʟᴇ>*:* `sɪʟᴇɴᴛʟʏ ʙᴀɴ ᴀ ᴜsᴇʀ. ᴅᴇʟᴇᴛᴇs ᴄᴏᴍᴍᴀɴᴅ, ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴅᴏᴇsɴ'ᴛ ʀᴇᴘʟʏ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)`
• /tban <ᴜsᴇʀʜᴀɴᴅʟᴇ> x(m/h/d)*:* `ʙᴀɴs ᴀ ᴜsᴇʀ ғᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = ᴍɪɴᴜᴛᴇs, h = ʜᴏᴜʀs, d = ᴅᴀʏs.`
• /unban <userhandle>*:* `ᴜɴʙᴀɴs ᴀ ᴜsᴇʀ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ )`
• /kick <userhandle>*:* `ᴋɪᴄᴋs ᴀ ᴜsᴇʀ ᴏᴜᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ, (via ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)`
• /mute <userhandle>*:* `sɪʟᴇɴᴄᴇs ᴀ ᴜsᴇʀ. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ.`
• /tmute <userhandle> x(m/h/d)*:* `ᴍᴜᴛᴇs a ᴜsᴇʀᴛ for x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = ᴍɪɴᴜᴛᴇs, h = ʜᴏᴜʀs, d = ᴅᴀʏs `
.
• /unmute <userhandle>*:* `ᴜɴᴍᴜᴛᴇs ᴀ ~ user. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs a ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ `
.
• /zombies*:* `sᴇᴀʀᴄʜᴇs ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ `
• /zombies clean*:* `ʀᴇᴍᴏᴠᴇs ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ `
.
• /abishnoi <chatid> <ᴍsɢ>*:* `ᴍᴀᴋᴇ ᴍᴇ sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀᴛ `.
"""

__mod_name__ = "𝙱ᴀɴs"

BAN_HANDLER = CommandHandler(["ban", "sban"], ban, run_async=True)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban, run_async=True)
KICK_HANDLER = CommandHandler(["kick", "punch"], punch, run_async=True)
UNBAN_HANDLER = CommandHandler("unban", unban, run_async=True)
##ROAR_HANDLER = CommandHandler("roar", selfunban, run_async=True)
UNBAN_BUTTON_HANDLER = CallbackQueryHandler(unbanb_btn, pattern=r"unbanb_")
KICKME_HANDLER = DisableAbleCommandHandler(
    ["kickme", "punchme"], punchme, filters=Filters.chat_type.groups, run_async=True
)
ABISHNOI_HANDLER = CommandHandler(
    "abishnoi",
    abishnoi,
    pass_args=True,
    filters=CustomFilters.sudo_filter,
    run_async=True,
)
BANME_HANDLER = CommandHandler("banme", banme, run_async=True)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
# dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(UNBAN_BUTTON_HANDLER)
dispatcher.add_handler(ABISHNOI_HANDLER)
dispatcher.add_handler(BANME_HANDLER)

__handlers__ = [
    BAN_HANDLER,
    TEMPBAN_HANDLER,
    KICK_HANDLER,
    UNBAN_HANDLER,
    # ROAR_HANDLER,
    KICKME_HANDLER,
    UNBAN_BUTTON_HANDLER,
    ABISHNOI_HANDLER,
    BANME_HANDLER,
]
