import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# ============================
# НАСТРОЙКИ — ВСТАВЬ СВОИ
# ============================
BOT_TOKEN = "ВСТАВЬ_ТОКЕН_СЮДА"

# ШАГ 1: Запусти бота и напиши ему /getid
# ШАГ 2: Скопируй число которое он пришлёт и вставь сюда:
ADMIN_CHAT_ID = 7787565361  # ← ЗАМЕНИТЬ НА СВОЙ ID
# ============================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

(UZ, AGE, COUNTRY, KNOW_HISTORY, HISTORY_TEXT, RP_EXP, SOURCE, LORE) = range(8)

KEYS_HISTORY = [
    ["Да", "Частично"],
    ["Ещё не читал", "Лора нет, беру ответственность"],
]
KEYS_RP   = [["Да", "Нет", "Совсем немного"]]
KEYS_LORE = [["Да", "Нет"]]


# /getid — узнать свой chat_id
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(
        f"🆔 Твой chat_id: `{uid}`\n\n"
        f"Вставь это число в переменную `ADMIN_CHAT_ID` в коде бота.",
        parse_mode="Markdown",
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "✨ *АНКЕТА | AURELIA RP* ✨\n\n"
        "Привет! Сейчас мы зададим тебе несколько вопросов для вступления в наше РП.\n"
        "Отвечай честно и развёрнуто. Удачи! 🗺️",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.message.reply_text("1️⃣ *ЮЗ в Telegram* (твой @юзернейм или имя):", parse_mode="Markdown")
    return UZ


async def get_uz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["uz"] = update.message.text
    await update.message.reply_text("2️⃣ *Возраст:*", parse_mode="Markdown")
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("3️⃣ *Какую страну выбираешь?*", parse_mode="Markdown")
    return COUNTRY


async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country"] = update.message.text
    await update.message.reply_text(
        "4️⃣ *Знаешь ли ты историю выбранной страны?*",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(KEYS_HISTORY, resize_keyboard=True, one_time_keyboard=True),
    )
    return KNOW_HISTORY


async def get_know_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["know_history"] = update.message.text
    await update.message.reply_text(
        "5️⃣ *Расскажи кратко об истории выбранной страны:*",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return HISTORY_TEXT


async def get_history_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history_text"] = update.message.text
    await update.message.reply_text(
        "6️⃣ *Есть ли опыт в текстовом РП?*",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(KEYS_RP, resize_keyboard=True, one_time_keyboard=True),
    )
    return RP_EXP


async def get_rp_exp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["rp_exp"] = update.message.text
    await update.message.reply_text(
        "7️⃣ *Откуда узнал о нас?*",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return SOURCE


async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["source"] = update.message.text
    await update.message.reply_text(
        "8️⃣ *Ознакомлен с лором Аурелии?*",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(KEYS_LORE, resize_keyboard=True, one_time_keyboard=True),
    )
    return LORE


async def get_lore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lore"] = update.message.text
    data = context.user_data
    user = update.effective_user

    username_str = f"@{user.username}" if user.username else user.full_name

    anketa = (
        f"📋 *НОВАЯ АНКЕТА | AURELIA RP*\n"
        f"👤 Telegram: {username_str} | ID: `{user.id}`\n"
        f"{'─' * 30}\n"
        f"*1. ЮЗ:* {data.get('uz')}\n"
        f"*2. Возраст:* {data.get('age')}\n"
        f"*3. Страна:* {data.get('country')}\n"
        f"*4. Знание истории:* {data.get('know_history')}\n"
        f"*5. История страны:*\n{data.get('history_text')}\n"
        f"*6. Опыт в РП:* {data.get('rp_exp')}\n"
        f"*7. Откуда узнал:* {data.get('source')}\n"
        f"*8. Лор Аурелии:* {data.get('lore')}"
    )

    # Отправка администратору по числовому chat_id
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=anketa,
            parse_mode="Markdown",
        )
        logger.info(f"Анкета от {user.id} отправлена администратору.")
    except Exception as e:
        logger.error(f"Ошибка отправки анкеты: {e}")

    await update.message.reply_text(
        "✅ *Анкета отправлена!*\n\n"
        "Спасибо за заявку в *AURELIA RP*! 🌍\n"
        "Модераторы рассмотрят её и свяжутся с тобой. Ожидай! ⏳",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Анкета отменена. Напиши /start чтобы начать заново.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("getid", get_id))

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            UZ:           [MessageHandler(filters.TEXT & ~filters.COMMAND, get_uz)],
            AGE:          [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            COUNTRY:      [MessageHandler(filters.TEXT & ~filters.COMMAND, get_country)],
            KNOW_HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_know_history)],
            HISTORY_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_history_text)],
            RP_EXP:       [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rp_exp)],
            SOURCE:       [MessageHandler(filters.TEXT & ~filters.COMMAND, get_source)],
            LORE:         [MessageHandler(filters.TEXT & ~filters.COMMAND, get_lore)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    logger.info("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()

async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["source"] = update.message.text
    await update.message.reply_text(
        QUESTIONS[7],
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(KEYS_LORE, resize_keyboard=True, one_time_keyboard=True),
    )
    return LORE


async def get_lore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lore"] = update.message.text
    data = context.user_data
    user = update.effective_user

    # Формируем анкету
    anketa = (
        f"📋 *НОВАЯ АНКЕТА | AURELIA RP*\n"
        f"👤 От: @{user.username or user.full_name} (ID: `{user.id}`)\n\n"
        f"*1. ЮЗ в Telegram:* {data.get('uz')}\n"
        f"*2. Возраст:* {data.get('age')}\n"
        f"*3. Страна:* {data.get('country')}\n"
        f"*4. Знание истории:* {data.get('know_history')}\n"
        f"*5. История страны:*\n{data.get('history_text')}\n"
        f"*6. Опыт в РП:* {data.get('rp_exp')}\n"
        f"*7. Откуда узнал:* {data.get('source')}\n"
        f"*8. Ознакомлен с лором Аурелии:* {data.get('lore')}"
    )

    # Отправляем анкету администратору
    try:
        await context.bot.send_message(
            chat_id=f"@{ADMIN_USERNAME}",
            text=anketa,
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Ошибка отправки анкеты: {e}")

    # Отвечаем пользователю
    await update.message.reply_text(
        "✅ *Анкета отправлена!*\n\n"
        "Спасибо за заявку в *AURELIA RP*! 🌍\n"
        "Модераторы рассмотрят её и свяжутся с тобой. Ожидай! ⏳",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Анкета отменена. Напиши /start, чтобы начать заново.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            UZ:           [MessageHandler(filters.TEXT & ~filters.COMMAND, get_uz)],
            AGE:          [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            COUNTRY:      [MessageHandler(filters.TEXT & ~filters.COMMAND, get_country)],
            KNOW_HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_know_history)],
            HISTORY_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_history_text)],
            RP_EXP:       [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rp_exp)],
            SOURCE:       [MessageHandler(filters.TEXT & ~filters.COMMAND, get_source)],
            LORE:         [MessageHandler(filters.TEXT & ~filters.COMMAND, get_lore)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    logger.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
