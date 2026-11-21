
import asyncio
import html
from telegram import Update
from telegram.ext import (
    Application,
    ChatMemberHandler,
    ContextTypes
)

TOKEN = "9190077598:AAHRf-RDrd3Fvs4kO1OQsOCILIngAGFcw44"

SOURCE_CHAT = "@nthmodcheat"
LOG_CHAT = "@nthsourcecheat"

ACTIVE = ("member", "administrator", "creator")


async def delete_later(bot, chat_id, message_id):
    await asyncio.sleep(300)
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
    except Exception as e:
        print("Mesaj silinemedi:", e)


async def member_log(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    event = update.chat_member

    if not event:
        return

    if event.chat.username:
        if event.chat.username.lower() != "nthmodcheat":
            return

    old = event.old_chat_member
    new = event.new_chat_member
    user = new.user

    old_status = old.status
    new_status = new.status

    if old_status not in ("left", "kicked") and new_status in ACTIVE:
        title = "🟢 YENİ ÜYE"
        action = "Katılma Tarihi"
    elif old_status in ACTIVE and new_status in ("left", "kicked"):
        title = "🚨 ÜYE AYRILDI"
        action = "Ayrılma Tarihi"
    else:
        return

    try:
        count = await context.bot.get_chat_member_count(
            SOURCE_CHAT
        )
    except Exception:
        count = "Bilinmiyor"

    first = html.escape(user.first_name or "-")
    last = html.escape(user.last_name or "-")
    username = (
        "@" + html.escape(user.username)
        if user.username else "@yok"
    )

    date = event.date.strftime("%d.%m.%Y %H:%M:%S")

    text = (
        f"<b>Fully Hack</b>\n"
        f"<b>{title}</b>\n\n"
        f"• Last Name: {last}\n"
        f"• First Name: {first}\n"
        f"• Telegram ID: <code>{user.id}</code>\n"
        f"• {action}: <b>{date}</b>\n"
        f"• Kullanıcı Adı: {username}\n"
        f"• Güncel Üye: <b>{count}</b>"
    )

    try:
        msg = await context.bot.send_message(
            chat_id=LOG_CHAT,
            text=text,
            parse_mode="HTML"
        )

        asyncio.create_task(
            delete_later(
                context.bot,
                msg.chat_id,
                msg.message_id
            )
        )

    except Exception as e:
        print("Log gönderme hatası:", e)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        ChatMemberHandler(
            member_log,
            ChatMemberHandler.CHAT_MEMBER
        )
    )

    print("Telegram Log Bot Aktif!")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
    
