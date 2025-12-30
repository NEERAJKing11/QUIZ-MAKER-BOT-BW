from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive! 🤖"

def run():
    # Render और अन्य क्लाउड पोर्ट 8080 या 0.0.0.0 एक्सपेक्ट करते हैं
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
