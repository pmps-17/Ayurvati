// src/hooks/useChat.js
import { useState, useRef, useEffect } from "react";

export default function useChat() {
  const [messages, setMessages] = useState([
    { sender: "ai", text: "Hi! I'm your Ayurveda personal doctor. How can I help you today?" }
  ]);
  const [loading, setLoading] = useState(false);
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (input) => {
    if (!input.trim()) return;
    setMessages(msgs => [...msgs, { sender: "user", text: input }]);
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      setMessages(msgs => [
        ...msgs,
        { sender: "ai", text: data.result || "Sorry, I couldn't process that." }
      ]);
    } catch {
      setMessages(msgs => [
        ...msgs,
        { sender: "ai", text: "Network error. Please try again." }
      ]);
    }
    setLoading(false);
  };

  return { messages, sendMessage, loading, chatRef };
}
