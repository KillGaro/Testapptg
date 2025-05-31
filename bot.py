import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Настройка логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# База данных (упрощенная)
users_db = {}

# Главное меню
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id not in users_db:
        users_db[user.id] = {"balance": 1000, "level": 1}
    
    keyboard = [
        [InlineKeyboardButton("🎰 Слоты (ставка: 100$)", callback_data="slots")],
        [InlineKeyboardButton("⚽ Виртуальный матч (ставка: 200$)", callback_data="sport")],
        [InlineKeyboardButton("🎯 Рулетка (ставка: 150$)", callback_data="roulette")],
        [InlineKeyboardButton("💰 Баланс", callback_data="balance")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        f"🎩 *Добро пожаловать в Lucky Jack Casino*, {user.first_name}!\n"
        f"Твой баланс: *{users_db[user.id]['balance']} $LUCKY* 🪙\n\n"
        "Выбери игру:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Игра в слоты
def slots(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    
    if users_db[user_id]["balance"] < 100:
        query.answer("❌ Недостаточно средств! Минимум: 100$", show_alert=True)
        return
    
    # Анимация барабанов
    symbols = ["🍒", "🍋", "🍊", "7️⃣", "💰"]
    msg = query.edit_message_text(text="🎰 Крутим барабаны...\n\n[ 🌀 | 🌀 | 🌀 ]")
    
    import time, random
    for _ in range(3):
        time.sleep(0.5)
        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)
        msg.edit_text(f"🎰 Крутим барабаны...\n\n[ {slot1} | {slot2} | {slot3} ]")
    
    # Проверка выигрыша
    if slot1 == slot2 == slot3:
        win = 500
        text = f"🎉 *ДЖЕКПОТ!* +{win}$"
    elif slot1 == slot2 or slot2 == slot3:
        win = 200
        text = f"🔥 *Вы выиграли!* +{win}$"
    else:
        win = -100
        text = "😢 *Проигрыш* -100$"
    
    users_db[user_id]["balance"] += win
    
    keyboard = [[InlineKeyboardButton("🔙 В меню", callback_data="menu")]]
    msg.edit_text(
        f"{text}\n\n"
        f"Твой баланс: *{users_db[user_id]['balance']} $LUCKY* 🪙",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Обработка кнопок
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    
    if data == "slots":
        slots(update, context)
    elif data == "menu":
        start(update, context)

def main() -> None:
    updater = Updater("ВАШ_TELEGRAM_BOT_TOKEN")
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
