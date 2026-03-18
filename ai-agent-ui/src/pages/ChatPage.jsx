import { useState, useRef, useEffect } from "react";
import { sendMessage } from "../api/client";
import MessageBubble from "../components/MessageBubble";
import Sidebar from "../components/SideBar";
import "../styles/chat.css";

export default function ChatPage({ token, onLogout }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hey! I'm your multi-agent assistant. Tell me what you need — I'll create tasks, schedule events, or set reminders.",
      plan: null,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeAgent, setActiveAgent] = useState(null);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text, plan: null }]);
    setLoading(true);

    try {
      const data = await sendMessage(token, text);
      const agentUsed = data.plan?.[0]?.agent?.replace("_agent", "") || null;
      setActiveAgent(agentUsed);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response, plan: data.plan },
      ]);
    } catch (err) {
      if (err.message === "Request failed") onLogout();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Something went wrong. Please try again.", plan: null },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const autoResize = (e) => {
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
  };

  return (
    <div className="chat-shell">
      <Sidebar activeAgent={activeAgent} onLogout={onLogout} />

      <div className="chat-main">
        <div className="chat-header">
          <div className="header-left">
            <span className="header-title">Assistant</span>
            <span className="status-pill">
              <span className="status-dot" />
              Live
            </span>
          </div>
        </div>

        <div className="messages-area">
          {messages.map((msg, i) => (
            <MessageBubble key={i} message={msg} />
          ))}
          {loading && (
            <div className="typing-indicator">
              <span /><span /><span />
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="input-bar">
          <textarea
            ref={textareaRef}
            className="chat-textarea"
            rows={1}
            value={input}
            onChange={(e) => { setInput(e.target.value); autoResize(e); }}
            onKeyDown={handleKey}
            placeholder="Create a task, schedule a meeting, set a reminder..."
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={!input.trim() || loading}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}