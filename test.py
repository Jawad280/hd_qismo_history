import os
from dotenv import load_dotenv
import requests
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test.py')

qiscus_app_id = os.environ.get("QISCUS_APP_ID")
qiscus_secret_key = os.environ.get("QISCUS_SECRET_KEY")
system_id = os.environ.get('QISCUS_SYSTEM_ID')
agent_id = os.environ.get('QISCUS_AGENT_ID')

def get_chat_history(room_id:str, page):
    url = f"https://api.qiscus.com/api/v2.1/rest/load_comments?room_id={room_id}&limit=100&page={page}"
    headers = {
        "QISCUS-SDK-APP-ID": qiscus_app_id,
        "QISCUS-SDK-SECRET": qiscus_secret_key
    }

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()
        comments = data.get('results').get('comments')

        return comments
    except requests.exceptions.RequestException as e:
        logger.info(f"Failed to retrieve conversation history for room ID: {room_id} - {str(e)}")
        return None
    
def get_full_chat_history(room_id: str):
    chat_history = []
    index = 1
    is_end = False

    while not is_end:
        curr_hist = get_chat_history(room_id=room_id, page=index)
        if curr_hist:
            chat_history += curr_hist
            index += 1
        else:
            is_end = True

    chat_history.sort(key=lambda comment: comment.get('timestamp'))
    return chat_history

def is_valid_comment(comment):
    if not comment:
        return False
    return comment.get('user').get('user_id') != system_id and (comment.get('type') == 'text' or comment.get('type') == 'file_attachment')

def format_comment(comment):
    if is_valid_comment(comment):
        if comment.get('payload').get('url'):
            # Image
            message = {
                'text': '',
                'type': comment.get('type'),
                'image_url': comment.get('payload').get('url'),
                'role': 'user' if comment.get('user').get('extras').get('is_customer') else 'assistant',
                'timestamp': comment.get('timestamp')
            }
        else:
            message = {
                'text': comment.get('message'),
                'type': comment.get('type'),
                'image_url': comment.get(''),
                'role': 'user' if comment.get('user').get('user_id') != agent_id else 'assistant',
                'timestamp': comment.get('timestamp')
            }

        return message

    else:
        return None

def format_chat_history(comments: list):
    res = []

    for comment in comments:
        message = format_comment(comment=comment)
        if message:
            res.append(message)
    
    return res

res = get_full_chat_history(room_id="269541399")
# res = format_chat_history(res)

print(res[:10])