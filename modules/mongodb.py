from pymongo import MongoClient
from datetime import datetime

class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["voice_assistant_db"]
        self.conversations = self.db["conversations"]
    
    def save_conversation(self, user_msg, ai_response, user_id="default"):

        try:
            #DATAS TO SAVE
            conversation_data = {
                "user_id": user_id,
                "user_message": user_msg,
                "assistant_response": ai_response,
                "timestamp": datetime.now(),
            }
            
            #SAVE TO DB
            result = self.conversations.insert_one(conversation_data)
            return result.inserted_id
        except Exception as e:
            return e
    
    def get_context(self, user_id="default", limit=5):
        try:
            conversations = self.conversations.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit)
            
            return [
                {"user": c["user_message"], "assistant": c["assistant_response"]}
                for c in conversations
            ]
        except Exception as e:
            return e
    
    def close_connection(self):
        self.client.close()