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
BOT_TOKEN = "8180212858:AAG36irfWEVJ9XG5oRaau0pyoqeUpL9bgVU"          # Токен от @BotFather
ADMIN_USERNAME = "THEKEFIRSTAN"           # Куда пересылать анкеты
# ============================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Этапы анкеты
(
    UZ, AGE, COUNTRY, KNOW_HISTORY,
    HISTORY_TEXT, RP_EXP, SOURCE, LORE
) = range(8)

QUESTIONS = [
    "1️⃣ *ЮЗ в Telegram* (твой @юзернейм или имя):",
    "2️⃣ *Возраст*:",
    "3️⃣ *Какую страну выбираешь?*",
    "4️⃣ *Знаешь ли ты историю выбранной страны?*",
    "5️⃣ *Расскажи кратко об истории выбранной страны:*",
    "6️⃣ *Есть ли опыт в текстовом РП?*",
    "7️⃣ *Откуда узнал о нас?*",
    "8️⃣ *Ознакомлен с лором Аурелии?*",
]

KEYS_HISTORY = [["Да", "Частично"], ["Ещё не читал", "Лора нет, беру на себя ответственность"]]
KEYS_RP = [["Да", "Нет", "Совсем немного"]]
KEYS_LORE = [["Да", "Нет"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "✨ *АНКЕТА | AURELIA RP* ✨\n\n"
        "Привет! Сейчас мы зададим тебе несколько вопросов для вступления в наше РП.\n"
        "Отвечай честно и развёрнуто. Удачи! 🗺️\n\n"
        "Начнём с первого вопроса 👇",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.message.reply_text(QUESTIONS[0], parse_mode="Markdown")
    return UZ


async def get_uz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["uz"] = update.message.text
    await update.message.reply_text(QUESTIONS[1], parse_mode="Markdown")
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text(QUESTIONS[2], parse_mode="Markdown")
    return COUNTRY


async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country"] = update.message.text
    await update.message.reply_text(
        QUESTIONS[3],
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(KEYS_HISTORY, resize_keyboard=True, one_time_keyboard=True),
    )
    return KNOW_HISTORY


async def get_know_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["know_history"] = update.message.text
    await update.message.reply_text(
        QUESTIONS[4],
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return HISTORY_TEXT


async def get_history_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history_text"] = update.message.text
    await update.message.reply_text(
        QUESTIONS[5],
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(KEYS_RP, resize_keyboard=True, one_time_keyboard=True),
    )
    return RP_EXP


async def get_rp_exp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["rp_exp"] = update.message.text
    await update.message.reply_text(
        QUESTIONS[6],
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return SOURCE


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
