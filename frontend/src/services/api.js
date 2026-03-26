import axios from "axios";

const API_URL = "http://localhost:8000/chat";

export async function sendMessage(session_id, message) {
  const response = await axios.post(API_URL, {
    session_id,
    message,
  });
  return response.data.response;
}
