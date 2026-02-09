import redis
import json
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_memory(session_id: str) -> List[Dict[str, str]]:
    data = r.get(session_id)
    if data:
        return json.loads(data)
    return []

def add_to_memory(session_id: str, user_msg: str, bot_msg: str) -> None:
    history = get_memory(session_id)
    history.append({"user": user_msg, "bot": bot_msg})
    r.set(session_id, json.dumps(history), ex=3600*24)  
