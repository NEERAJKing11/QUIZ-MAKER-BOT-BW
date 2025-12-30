import pymongo
import certifi
from config import MONGO_URI

# डेटाबेस से कनेक्ट करना
try:
    client = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['QuizBotDB']  # डेटाबेस का नाम
    quizzes_col = db['quizzes'] # क्विज़ सेव करने की जगह
    print("✅ Database Connected Successfully!")
except Exception as e:
    print(f"❌ Database Error: {e}")

# --- Temporary User Data (Ram me rahega, quiz banate waqt) ---
user_state = {} 

# --- Functions to Save/Get Quiz (Permanent) ---

def save_new_quiz(user_id, title, desc, question):
    # एक यूनिक ID बनाते हैं
    quiz_id = f"quiz_{user_id}_{title.replace(' ', '')[:5]}"
    
    data = {
        "_id": quiz_id,
        "user_id": user_id,
        "title": title,
        "desc": desc,
        "question": question
    }
    quizzes_col.insert_one(data)
    return quiz_id

def get_quiz_by_id(quiz_id):
    return quizzes_col.find_one({"_id": quiz_id})
