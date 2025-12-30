import telebot

# 1. अपना टेलीग्राम बॉट टोकन यहाँ डालें
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# 2. अपना MongoDB URL यहाँ डालें
# यह कुछ ऐसा दिखता है: "mongodb+srv://user:password@cluster..."
MONGO_URI = 'YOUR_MONGODB_CONNECTION_STRING_HERE'

bot = telebot.TeleBot(API_TOKEN)
