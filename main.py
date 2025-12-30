from config import bot
import handlers  # यह लाइन बहुत जरुरी है, इससे handlers.py का कोड लोड होगा

print("🤖 Bot is Running Smoothly...")

if __name__ == "__main__":
    bot.infinity_polling()
