from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from config import bot
import storage

# --- 1. START & RESTART COMMAND ---
@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    user_id = message.chat.id
    
    # पुराना डेटा साफ़ करें (Restart Logic)
    if user_id in storage.user_data:
        del storage.user_data[user_id]
    
    bot.reply_to(message, 
                 "🤖 **Ultra Quiz Bot में आपका स्वागत है!**\n\n"
                 "नया क्विज़ बनाने के लिए /createquiz दबाएं।", 
                 parse_mode="Markdown")

# --- 2. CREATE QUIZ COMMAND ---
@bot.message_handler(commands=['createquiz'])
def start_creation(message):
    user_id = message.chat.id
    storage.user_data[user_id] = {"step": 1}
    bot.send_message(user_id, "📝 **Quiz का नाम (Title) क्या रखना है?**\n\nअपना टाइटल भेजें:")

# --- 3. TEXT HANDLER (STEP-BY-STEP) ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.chat.id
    text = message.text

    if user_id not in storage.user_data:
        return

    step = storage.user_data[user_id].get("step")

    # Step 1 -> 2
    if step == 1:
        storage.user_data[user_id]["title"] = text
        storage.user_data[user_id]["step"] = 2
        bot.send_message(user_id, "✅ टाइटल सेट!\n\n📄 **Description (विवरण) भेजें:**")

    # Step 2 -> 3
    elif step == 2:
        storage.user_data[user_id]["desc"] = text
        storage.user_data[user_id]["step"] = 3
        bot.send_message(user_id, "✅ डिस्क्रिप्शन सेट!\n\n❓ **Question (प्रश्न) भेजें:**")

    # Step 3 -> Final
    elif step == 3:
        storage.user_data[user_id]["question"] = text
        
        # क्विज़ सेव करें
        quiz_id = f"quiz_{user_id}"
        storage.quizzes[quiz_id] = {
            "title": storage.user_data[user_id]["title"],
            "desc": storage.user_data[user_id]["desc"],
            "question": storage.user_data[user_id]["question"]
        }
        
        # स्टेट क्लियर करें
        del storage.user_data[user_id]
        
        # फाइनल पैनल भेजें
        send_quiz_panel(user_id, quiz_id)

# --- 4. PANEL FUNCTION ---
def send_quiz_panel(chat_id, quiz_id):
    quiz = storage.quizzes.get(quiz_id)
    if not quiz: return

    bot_username = bot.get_me().username
    msg_text = (f"🔥 **{quiz['title']}**\n📖 {quiz['desc']}\n❓ {quiz['question']}")

    markup = InlineKeyboardMarkup(row_width=1)
    btn_start = InlineKeyboardButton("🚀 Start Quiz", callback_data=f"start_{quiz_id}")
    btn_group = InlineKeyboardButton("👥 Start in Group", switch_inline_query=quiz_id)
    
    share_url = f"https://t.me/share/url?url=https://t.me/{bot_username}?start={quiz_id}"
    btn_share = InlineKeyboardButton("🔗 Share Quiz", url=share_url)

    markup.add(btn_start, btn_group, btn_share)
    bot.send_message(chat_id, msg_text, reply_markup=markup, parse_mode="Markdown")

# --- 5. CALLBACKS & INLINE ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('start_'))
def handle_start_quiz(call):
    bot.answer_callback_query(call.id, "✅ Quiz Starting...")
    bot.send_message(call.message.chat.id, "Quiz is LIVE! (Questions will appear here)")

@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
    try:
        quiz_id = inline_query.query
        if quiz_id in storage.quizzes:
            quiz = storage.quizzes[quiz_id]
            r = InlineQueryResultArticle(
                id='1', title=quiz['title'], description=quiz['desc'],
                input_message_content=InputTextMessageContent(f"Quiz Time: {quiz['title']}\nClick Start below!")
            )
            bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)
