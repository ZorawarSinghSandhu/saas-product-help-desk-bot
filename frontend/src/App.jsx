import { useState } from "react";
import "./App.css";

//How does seat billing work?

function App() {
  const [messages, setMessages] = useState([]);
  const [currentInput, setCurrentInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (currentInput.trim() === "") return;
    if (loading) return;

    setLoading(true);
    // let result;
    const url = "http://127.0.0.1:8000/ask";
    const userMessage = currentInput;
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setCurrentInput("");

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage }),
      });
      if (!response.ok) {
        console.log(await response.text());
        throw new Error(`Response Status: ${response.status}`);
      }

      const result = await response.json();
      setMessages((prev) => [
        ...prev,
        { role: "system", content: result.answer },
      ]);
      console.log(result.answer);
    } catch (error) {
      console.log(error.message);

      setMessages((prev) => [
        ...prev,
        { role: "system", content: "Sorry, something went wrong." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Chat Header</h2>
      </div>

      <div className="chat-messages">
        <h2>Chat Messages</h2>

        {messages.map((message, index) => (
          <div
            key={index}
            className={message.role === "user" ? "user-message" : "bot-message"}
          >
            {message.content}
          </div>
        ))}
      </div>
      {loading && <div className="loading-div">Loading...</div>}

      <div className="text-box">
        <h2>Input box</h2>
        <input
          type="text"
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
          value={currentInput}
          onChange={(e) => setCurrentInput(e.target.value)}
        />
        <button
          id="send-button"
          type="button"
          onClick={sendMessage}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
