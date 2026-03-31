# backend/app/utils/conversation_manager.py

from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..logger import logger


class ConversationManager:
    """
    Maneja el estado y mensajes de conversaciones en memoria.
    Nota: Esto es un MVP. En producción hospitalaria debe persistirse en DB.
    """

    def __init__(self, ttl_minutes: int = 60):
        self.conversations: Dict[str, Dict[str, Any]] = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def _ensure_conversation(self, conv_id: str):
        if conv_id not in self.conversations:
            self.conversations[conv_id] = {
                "messages": [],
                "state": {},
                "created": datetime.utcnow(),
                "last_activity": datetime.utcnow()
            }
            logger.info(f"[ConversationManager] Nueva conversación creada | conv_id={conv_id}")

    def _cleanup_expired(self):
        now = datetime.utcnow()
        expired_ids = []

        for conv_id, data in self.conversations.items():
            last_activity = data.get("last_activity", data.get("created"))
            if now - last_activity > self.ttl:
                expired_ids.append(conv_id)

        for conv_id in expired_ids:
            del self.conversations[conv_id]
            logger.info(f"[ConversationManager] Conversación expirada eliminada | conv_id={conv_id}")

    def save_message(self, conv_id: str, role: str, content: str):
        if conv_id not in self.conversations:
            self.conversations[conv_id] = {"messages": [], "patient_info": {}}
        
        self.conversations[conv_id]["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_history(self, conv_id: str) -> List[Dict]:
        return self.conversations.get(conv_id, {}).get("messages", [])

    def get_patient_info(self, conv_id: str) -> dict:
        return self.conversations.get(conv_id, {}).get("patient_info", {})
        logger.info(f"[ConversationManager] Mensaje guardado | conv_id={conv_id} | role={role}")

    def update_state(self, conv_id: str, new_state: dict):
        self._cleanup_expired()
        self._ensure_conversation(conv_id)

        if not isinstance(new_state, dict):
            logger.warning(f"[ConversationManager] new_state no es dict | conv_id={conv_id}")
            return

        self.conversations[conv_id]["state"].update(new_state)
        self.conversations[conv_id]["last_activity"] = datetime.utcnow()

        logger.info(f"[ConversationManager] Estado actualizado | conv_id={conv_id} | step={new_state.get('step')}")

    def get_state(self, conv_id: str) -> dict:
        self._cleanup_expired()
        self._ensure_conversation(conv_id)
        return self.conversations[conv_id]["state"]

    def get_messages(self, conv_id: str) -> List[dict]:
        self._cleanup_expired()
        self._ensure_conversation(conv_id)
        return self.conversations[conv_id]["messages"]

    def reset_conversation(self, conv_id: str):
        if conv_id in self.conversations:
            del self.conversations[conv_id]
            logger.info(f"[ConversationManager] Conversación reiniciada | conv_id={conv_id}")
