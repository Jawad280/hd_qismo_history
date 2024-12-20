from db import db, DR_JIB_CONVERSATIONS_COLLECTION
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main.py')

def get_data():
    try:
        # Fetch All Chats
        ref = db.collection(DR_JIB_CONVERSATIONS_COLLECTION)
        docs = ref.get()

        # Extract & organize data by room_id
        data = {}
        for doc in docs:
            room_id = doc.id
            doc_data = doc.to_dict()

            if doc_data:
                data[room_id] = doc_data

        # Save to JSON file
        with open('chat_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logger.info("Data successfully saved to chat_data.json")

    except Exception as e:
        logger.exception(f"Something went wrong when retrieving conversation history : {e}")
        raise e    


get_data()