import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN  = "8829239086:AAHnNy2IK6mL--7-P6oXqevTODEsAC6EBxI"
CHANNEL_ID = "@such_chuhuiv"

logging.basicConfig(level=logging.INFO)

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Пришли заявку — текст или фото — и она попадёт в канал."
    )

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    try:
        if msg.photo:
            await ctx.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=msg.photo[-1].file_id,
                caption=msg.caption or ""
            )
        elif msg.video:
            await ctx.bot.send_video(
                chat_id=CHANNEL_ID,
                video=msg.video.file_id,
                caption=msg.caption or ""
            )
        elif msg.text:
            await ctx.bot.send_message(
                chat_id=CHANNEL_ID,
                text=msg.text
            )
        else:
            await msg.reply_text("Поддерживаются только текст, фото и видео.")
            return
        await msg.reply_text("Заявка отправлена ✓")
    except Exception as e:
        logging.error("Ошибка: %s", e)
        await msg.reply_text("Не удалось отправить. Бот добавлен в канал как админ?")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND | filters.PHOTO | filters.VIDEO,
        handle_message
    ))
    app.run_polling()

if __name__ == "__main__":
    main()
