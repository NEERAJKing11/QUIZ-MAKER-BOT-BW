import telebot

# 1. अपना टेलीग्राम बॉट टोकन यहाँ डालें
API_TOKEN = '8442551616:AAFc3SHbjpCvfbTu-Ss-Rx4lTgKt2J8Paqw'

# 2. अपना MongoDB URL यहाँ डालें
# यह कुछ ऐसा दिखता है: "mongodb+srv://user:password@cluster..."
MONGO_URI = 'mongodb+srv://sardakumari905_db_user:p6yUp70gQGLwYTDN@cluster0.0r1bebe.mongodb.net/?appName=Cluster0'

bot = telebot.TeleBot(API_TOKEN)
