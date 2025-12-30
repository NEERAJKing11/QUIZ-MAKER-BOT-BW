from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from config import bot
import database  # अब हम database वाली फाइल यूज़ करेंगे

# --- START & RESTART ---
@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id in database.user_state:
        del database.user_state[user_id]
    
    bot.reply_to(message, "🤖 **Life-Time Quiz Bot में स्वागत है!**\n\nनया क्विज़ बनाने के लिए /createquiz दबाएं।")

# --- CREATE QUIZ ---
@bot.message_handler(commands=['createquiz'])
def start_creation(message):
    user_id = message.chat.id
    database.user_state[user_id] = {"step": 1}
    bot.send_message(user_id, "📝 **Quiz का नाम (Title) भेजें:**")

# --- TEXT HANDLER ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.chat.id
    text = message.text

    if user_id not in database.user_state:
        return

    step = database.user_state[user_id].get("step")

    if step == 1:
        database.user_state[user_id]["title"] = text
        database.user_state[user_id]["step"] = 2
        bot.send_message(user_id, "✅ Title सेट!\n\n📄 **Description भेजें:**")

    elif step == 2:
        database.user_state[user_id]["desc"] = text
        database.user_state[user_id]["step"] = 3
        bot.send_message(user_id, "✅ Description सेट!\n\n❓ **Question भेजें:**")

    elif step == 3:
        # यहाँ हम डेटाबेस में सेव करेंगे (Permanent Save)
        title = database.user_state[user_id]["title"]
        desc = database.user_state[user_id]["desc"]
        question = text
        
        quiz_id = database.save_new_quiz(user_id, title, desc, question)
        
        del database.user_state[user_id]
        send_quiz_panel(user_id, quiz_id)

# --- PANEL FUNCTION ---
def send_quiz_panel(chat_id, quiz_id):
    quiz = database.get_quiz_by_id(quiz_id)
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

# --- CALLBACKS ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('start_'))
def handle_start_quiz(call):
    quiz_id = call.data.split('_', 1)[1]
    quiz = database.get_quiz_by_id(quiz_id)
    
    if quiz:
        bot.answer_callback_query(call.id, "✅ Quiz Starting...")
        bot.send_message(call.message.chat.id, f"**Question:** {quiz['question']}", parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "❌ Quiz नहीं मिला!")

# --- INLINE QUERY (GROUP) ---
@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
    try:
        quiz_id = inline_query.query
        quiz = database.get_quiz_by_id(quiz_id)
        
        if quiz:
            r = InlineQueryResultArticle(
                id='1', title=quiz['title'], description=quiz['desc'],
                input_message_content=InputTextMessageContent(f"Quiz: {quiz['title']}\nClick Start below to play!")
            )
            bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)
