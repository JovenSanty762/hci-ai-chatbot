import { useState } from "react";
import { sendMessage } from "../services/api";
import MessageBubble from "./MessageBubble";
import Header from "./Header";
import { v4 as uuidv4 } from "uuid";

export default function ChatWindow() {
  const [sessionId] = useState(uuidv4());
  const [messages, setMessages] = useState([
    { sender: "bot", text: "🏥 Bienvenido al asistente virtual del Hospital. ¿Qué especialidad deseas agendar?" }
  ]);
  const [input, setInput] = useState("");

  async function handleSend() {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    const botResponse = await sendMessage(sessionId, input);

    const botMsg = { sender: "bot", text: botResponse };
    setMessages((prev) => [...prev, botMsg]);

    setInput("");
  }

  return (
    <div style={{
      width: "400px",
      margin: "50px auto",
      borderRadius: "10px",
      boxShadow: "0px 0px 10px rgba(0,0,0,0.2)",
      overflow: "hidden",
      fontFamily: "Arial"
    }}>
      <Header />

      <div style={{
        height: "450px",
        padding: "15px",
        overflowY: "auto",
        backgroundColor: "#f7f7f7"
      }}>
        {messages.map((msg, index) => (
          <MessageBubble key={index} sender={msg.sender} text={msg.text} />
        ))}
      </div>

      <div style={{
        display: "flex",
        padding: "10px",
        borderTop: "1px solid #ccc",
        backgroundColor: "white"
      }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe aquí..."
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc"
          }}
        />
        <button
          onClick={handleSend}
          style={{
            marginLeft: "10px",
            padding: "10px 15px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#0066cc",
            color: "white",
            cursor: "pointer"
          }}
        >
          Enviar
        </button>
      </div>
    </div>
  );
}
