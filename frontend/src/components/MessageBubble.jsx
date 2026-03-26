export default function MessageBubble({ sender, text }) {
  const isBot = sender === "bot";

  return (
    <div style={{
      display: "flex",
      justifyContent: isBot ? "flex-start" : "flex-end",
      marginBottom: "10px"
    }}>
      <div style={{
        maxWidth: "70%",
        padding: "10px 14px",
        borderRadius: "12px",
        backgroundColor: isBot ? "#eaeaea" : "#007bff",
        color: isBot ? "#000" : "#fff",
        whiteSpace: "pre-line"
      }}>
        {text}
      </div>
    </div>
  );
}
