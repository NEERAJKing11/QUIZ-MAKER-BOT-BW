from config import bot
import handlers
from keep_alive import keep_alive  # 👈 यह लाइन जोड़ें

if __name__ == "__main__":
    print("🤖 Bot Starting...")
    
    # 👈 यह लाइन जोड़ें (वेब सर्वर स्टार्ट करने के लिए)
    keep_alive()  
    
    print("✅ Online and Connected to MongoDB!")
    bot.infinity_polling()
