import telebot

# 1. अपना टेलीग्राम बॉट टोकन यहाँ डालें
API_TOKEN = '7965361903:AAExpjboakayOxURWG47AnspkeptzqBFDo0'

# 2. अपना MongoDB URL यहाँ डालें
# यह कुछ ऐसा दिखता है: "mongodb+srv://user:password@cluster..."
MONGO_URI = 'mongodb+srv://sardakumari905_db_user:p6yUp70gQGLwYTDN@cluster0.0r1bebe.mongodb.net/?appName=Cluster0'

bot = telebot.TeleBot(API_TOKEN)
