conversation_state = {}

def init_conversation(session_id: str):
    conversation_state[session_id] = {
        "step": "welcome",
        "data": {}
    }

def get_state(session_id: str):
    return conversation_state.get(session_id)

def update_state(session_id: str, step: str, key=None, value=None):
    if session_id not in conversation_state:
        init_conversation(session_id)

    conversation_state[session_id]["step"] = step

    if key:
        conversation_state[session_id]["data"][key] = value

def end_conversation(session_id: str):
    if session_id in conversation_state:
        del conversation_state[session_id]
