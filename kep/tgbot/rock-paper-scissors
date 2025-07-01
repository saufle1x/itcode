import json
import datetime
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Підключаємо код до бота через токен, API Біткоїна також ми його підключаємо
BOT_TOKEN = "your_token_here"  # бот 
ADMIN_ID = 123456789  # Telegram ID для адмін-прав
USER_DATA = "data.json"  # Файл для зберігання даних користувачів
BTC_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"  

# Готуємо текст + англійську мову додаємо
TEXTS = {
    "ua": {
        "start": "🇺🇦 Виберіть мову",
        "welcome": "👋 Вітаю, {name}! Це гра 'Камінь-ножиці-папір'.\n\n"
                   "Доступні команди:\n"
                   "/play - Почати гру\n"
                   "/lang - Змінити мову\n"
                   "/help - Допомога\n"
                   "/info - Правила гри\n"
                   "/about - Про бота\n"
                   "/bitcoin - Курс Bitcoin\n",
        "game_choice": "Твій вибір: {choice}\nМій вибір: {bot_choice}\n\nРезультат: {result}",
        "stats": "📊 Ваша статистика:\nПеремоги: {wins}\nПоразки: {losses}\nНічиї: {draws}",
        "exit": "❌Вийти❌",
        "refused": "Жалко 😢\nНаступного разу зіграємо! Просто введи команду /play",
        "help": "ℹ️ Допомога:\n"
                "- Використовуйте кнопки для гри\n"
                "- /play - почати нову гру\n"
                "- /lang - змінити мову\n"
                "- /info - правила гри\n"
                "- /bitcoin - курс Bitcoin\n"  
                "- /stats - ваша статистика",
        "info": "📝 Правила гри:\n"
                "- Камінь перемагає ножиці\n"
                "- Ножиці перемагають папір\n"
                "- Папір перемагає камінь\n"
                "- Однакові вибори - нічия!\n\n"
                "Якщо хочеш почати - натисни команду під назвою /play",
        "about": "🤖 Про цього бота:\nЦе класична гра 'Камінь-ножиці-папір' з розширеннями:"
                "\n- Збереження статистики\n- З двома міжнародними мовами (українська та англійська)\n- Курс Bitcoin\n- Власна статистика",
        "time": "🕒 Поточний час: {time}",
        "hello": "Привіт, {name}! Радий тебе бачити 😊",
        "mood": "У мене все чудово! Надіюсь, у тебе теж 😉",
        "btc_rate": "💰 Поточний курс Bitcoin: ${rate} USD",  
        "change_lang": "🌐 Оберіть нову мову:",
        "lang_updated": "Мову змінено на українську!",
        "admin_stats": "👑 Адмін статистика:\nКористувачів: {users}\nІгор зіграно: {games}",
        "unknown": "Не розумію команди 😕 Використай /help",
        "choices": ["Камінь", "Ножиці", "Папір"],
        "results": ["Ви перемогли! 🎉", "Ви програли 😢", "Нічия! 🤝"]
    },
    "en": {
        "start": "🇺🇸 Choose language",
        "welcome": "👋 Hello, {name}! This is 'Rock-Paper-Scissors' game.\n\n"
                   "Available commands:\n"
                   "/play - Start game\n"
                   "/lang - Change language\n"
                   "/help - Help\n"
                   "/info - Game rules\n"
                   "/about - About bot\n"
                   "/bitcoin - Bitcoin rate\n",  
        "game_choice": "Your choice: {choice}\nMy choice: {bot_choice}\n\nResult: {result}",
        "stats": "📊 Your stats:\nWins: {wins}\nLosses: {losses}\nDraws: {draws}",
        "exit": "❌Exit❌",
        "refused": "Too bad 😢\nLet's play next time! Just type /play",
        "help": "ℹ️ Help:\n"
                "- Use buttons to play\n"
                "- /play - start new game\n"
                "- /lang - change language\n"
                "- /info - game rules\n"
                "- /bitcoin - Bitcoin rate\n"  
                "- /stats - your statistics",
        "info": "📝 Game rules:\n"
                "- Rock beats scissors\n"
                "- Scissors beat paper\n"
                "- Paper beats rock\n"
                "- Same choices - draw!\n\n"
                "To start, press /play",
        "about": "🤖 About this bot:\nClassic 'Rock-Paper-Scissors' game with extra features:"
                "\n- Statistics saving\n- Multilingual\n- Bitcoin rate\n- Personal stats",
        "time": "🕒 Current time: {time}",
        "hello": "Hello, {name}! Nice to see you 😊",
        "mood": "I'm great! Hope you are too 😉",
        "btc_rate": "💰 Current Bitcoin rate: ${rate} USD",
        "change_lang": "🌐 Choose new language:",
        "lang_updated": "Language changed to English!",
        "admin_stats": "👑 Admin stats:\nUsers: {users}\nGames played: {games}",
        "unknown": "Don't understand command 😕 Use /help",
        "choices": ["Rock", "Scissors", "Paper"],
        "results": ["You won! 🎉", "You lost 😢", "Draw! 🤝"]
    }
}

# Завантаження даних користувачів
def load_user_data():
    try:
        with open(USER_DATA, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Збереження даних користувачів
def save_user_data():
    with open(USER_DATA, "w") as f:
        json.dump(user_data, f, indent=2)

# Зберігаємо інформацію про нього
def info_user_data(user_id, name):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            "name": name,
            "lang": "ua",  # Мова за замовчуванням
            "stats": {"wins": 0, "losses": 0, "draws": 0}  # Статистика
        }

# Отримуємо текст, включаючи мову 
def get_text(user_id, key, **kwargs):
    lang = user_data.get(str(user_id), {"lang": "ua"}).get("lang", "ua")
    text = TEXTS[lang][key]
    return text.format(**kwargs) if kwargs else text

# Клавіатура для вибору мови
def language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("English 🇺🇸", callback_data="lang_en"),
            InlineKeyboardButton("Українська 🇺🇦", callback_data="lang_ua")
        ]
    ])

# Клавіатура для гри
def game_keyboard(user_id, include_choices=True):
    lang = user_data.get(str(user_id), {"lang": "uk"}).get("lang", "uk")
    keyboard = []
    
    if include_choices:
        choices = TEXTS[lang]["choices"]
        keyboard.append([
            InlineKeyboardButton(choices[0], callback_data="choice_0"), #Rock/Камінь
            InlineKeyboardButton(choices[1], callback_data="choice_1"), #Scissors/Ножиці
            InlineKeyboardButton(choices[2], callback_data="choice_2")  #Paper/Папір
        ])
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, "exit"), callback_data="exit_game")])
    return InlineKeyboardMarkup(keyboard)

# Визначення переможця 
def winner(user_choice, bot_choice):
    # 0-камінь, 1-ножиці, 2-папір
    if user_choice == bot_choice:
        return 2  # Нічия
    elif (user_choice - bot_choice) % 3 == 1:
        return 0  # Користувач перемагає
    else:
        return 1  # Бот перемагає

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info_user_data(user.id, user.full_name)

    if update.message:
        await update.message.reply_text(
            get_text(user.id, "start"),
            reply_markup=language_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            get_text(user.id, "start"),
            reply_markup=language_keyboard()
        )

# Функція зміни мови
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang = query.data.split("_")[1]  # "lang_en" -> "en"
    
    user_data[str(user_id)]["lang"] = lang
    save_user_data()
    
    await query.edit_message_text(get_text(user_id, "welcome", name=query.from_user.full_name))
    await query.answer()

# Команда /play
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info_user_data(user.id, user.full_name)
    
    await update.message.reply_text(
        get_text(user.id, "welcome", name=user.full_name),
        reply_markup=game_keyboard(user.id)
    )

# Функція вибору гравця
async def game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    
    if data == "exit_game":
        await query.edit_message_text(
            get_text(user_id, "refused"),
            reply_markup=None  # Прибираємо клавіатуру після виходу
        )
        await start(update, context)
        return
    
    # Формуємо вибір гравця (0, 1, 2)
    user_choice = int(data.split("_")[1])
    bot_choice = random.randint(0, 2) # Випадковий вибір бота
    result_index = winner(user_choice, bot_choice)
    
    # Оновлюємо статистики
    stats = user_data[str(user_id)]["stats"]
    if result_index == 0:
        stats["wins"] += 1
    elif result_index == 1:
        stats["losses"] += 1
    else:
        stats["draws"] += 1
    save_user_data()
    
    lang = user_data[str(user_id)]["lang"]
    choices = TEXTS[lang]["choices"]
    results = TEXTS[lang]["results"]
    
    # Результат гри 
    await query.edit_message_text(
        get_text(user_id, "game_choice",
                 choice=choices[user_choice],
                 bot_choice=choices[bot_choice],
                 result=results[result_index]) + "\n\n" +
        get_text(user_id, "stats", **stats),
        reply_markup=game_keyboard(user_id)  # Показуємо кнопки знову після гри
    )
    
# Команда /lang
async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info_user_data(user.id, user.full_name)
    
    await update.message.reply_text(
        get_text(user.id, "change_lang"),
        reply_markup=language_keyboard()
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(get_text(user.id, "help"))

# Команда /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(get_text(user.id, "info"))

# Команда /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(get_text(user.id, "about"))

# Команда /bitcoin 
async def btc_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(BTC_API_URL)
        rate = response.json()["bitcoin"]["usd"]
        await update.message.reply_text(get_text(update.effective_user.id, "btc_rate", rate=rate))
    except Exception as e:
        await update.message.reply_text("⚠️ Не вдалося фіксувати курс Bitcoin")

# Команда /stats
async def user_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info_user_data(user.id, user.full_name)
    stats = user_data[str(user.id)]["stats"]
    await update.message.reply_text(get_text(user.id, "stats", **stats))

# Команда /adminstats (тільки для адміна)
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != ADMIN_ID:
        return
    
    total_games = sum(
        u["stats"]["wins"] + u["stats"]["losses"] + u["stats"]["draws"]
        for u in user_data.values()
    )
    
    await update.message.reply_text(
        get_text(user.id, "admin_stats", users=len(user_data), games=total_games)
    )

# Реакція на повідомлення
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.lower()
    info_user_data(user.id, user.full_name)
    
    responses = {
        "привіт": "hello",
        "хай": "hello",
        "здоров":"hello",
        "hello": "hello",
        "hey": "hello",
        "hi": "hello",
        "як справи?": "mood",
        "що робиш?": "mood",
        "how are you?": "mood",
        "котра година?": "time",
        "яка година?": "time",
        "what time is it?": "time"
    }
    
    for key, response_key in responses.items():
        if key in text:
            if response_key == "time":
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                await update.message.reply_text(get_text(user.id, "time", time=current_time))
            else:
                await update.message.reply_text(get_text(user.id, response_key, name=user.first_name))
            return
    
    await update.message.reply_text(get_text(user.id, "unknown"))

# Загальна функція (старт)
def main():
    global user_data
    user_data = load_user_data()  # Завантажуємо дані користувачів
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Налаштуємо команди
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play_game))
    app.add_handler(CommandHandler("lang", change_language))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("bitcoin", btc_rate))  
    app.add_handler(CommandHandler("stats", user_stats))
    app.add_handler(CommandHandler("adminstats", admin_stats))
    
    # Реакції на кнопки
    app.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(game_handler, pattern="^(choice_|exit)"))
    
    # Обробка повідомлень
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаємо бота
    app.run_polling()
    
if __name__ == "__main__":
    main()
