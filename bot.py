import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Настройки бота
BOT_TOKEN = "7803991408:AAEeo9EjSTTU_J41YSyPrhEWWDjuMtOdnEg"  # ⚠️ Замените перед запуском!
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Игровая логика
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🎰 Слоты", callback_data="slots")],
        [InlineKeyboardButton("🎯 Рулетка", callback_data="roulette")]
    ]
    update.message.reply_text(
        "🎩 Добро пожаловать в казино!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "slots":
        query.edit_message_text(text="🎰 Вы выбрали слоты!")

if __name__ == '__main__':
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    print("Бот запущен!")
