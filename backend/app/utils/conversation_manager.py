# backend/app/utils/conversation_manager.py
from typing import Dict
import json
from datetime import datetime

class ConversationManager:
    def __init__(self):
        self.conversations: Dict = {}

    def save_message(self, conv_id: str, role: str, content: str):
        if conv_id not in self.conversations:
            self.conversations[conv_id] = {"messages": [], "state": {}, "created": datetime.utcnow()}
        
        self.conversations[conv_id]["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

    def update_state(self, conv_id: str, new_state: dict):
        if conv_id in self.conversations:
            self.conversations[conv_id]["state"].update(new_state)

    def get_state(self, conv_id: str) -> dict:
        return self.conversations.get(conv_id, {}).get("state", {})
