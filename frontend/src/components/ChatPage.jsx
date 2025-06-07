// src/components/ChatPage.jsx
import React, { useEffect, useRef, useState } from 'react';
import { auth } from '../firebase';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/ChatPage.module.css';
import ChatBubble from './ChatBubble';
import { useAuth } from '../hooks/useAuth';
import { getMoodLogs } from '../api/logsApi';

function ChatPage({ theme, setTheme }) {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: "Hi! I'm your Ayurveda personal doctor. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [moodLogs, setMoodLogs] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const chatRef = useRef(null);
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Fetch mood logs when user or showHistory toggles
  useEffect(() => {
    if (!user?.email || !showHistory) return;
    getMoodLogs(user.email)
      .then(setMoodLogs)
      .catch(() => setMoodLogs([]));
  }, [user, showHistory]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages(msgs => [...msgs, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, user_email: user?.email })
      });
      const data = await res.json();
      setMessages(msgs => [
        ...msgs,
        { sender: 'ai', text: data.result || "Sorry, I couldn't process that." }
      ]);
    } catch {
      setMessages(msgs => [
        ...msgs,
        { sender: 'ai', text: "Network error. Please try again." }
      ]);
    }
    setLoading(false);
  };

  const handleLogout = () => {
    auth.signOut();
    navigate('/login');
  };

  const toggleTheme = () => setTheme(t => (t === 'dark' ? 'light' : 'dark'));

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>
        <span>Ayurveda Doctor AI</span>
        <div>
          <button onClick={() => setShowHistory(h => !h)} className={styles.themeToggle}>
            {showHistory ? "Hide History" : "Show History"}
          </button>
          <button onClick={toggleTheme} className={styles.themeToggle}>
            {theme === 'dark' ? '🌙' : '☀️'}
          </button>
          <button onClick={handleLogout} className={styles.logoutButton}>Sign Out</button>
        </div>
      </div>

      {showHistory && (
        <div className={styles.historySection}>
          <h4>Mood Logs</h4>
          {moodLogs.length === 0 && <div>No mood logs yet.</div>}
          <ul>
            {moodLogs.map((log, idx) => (
              <li key={idx}>
                {log.timestamp}: <b>{log.mood}</b> (intensity {log.intensity})
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className={styles.messages}>
        {messages.map((msg, idx) => (
          <ChatBubble key={idx} message={msg} />
        ))}
        <div ref={chatRef} />
      </div>

      <form onSubmit={sendMessage} className={styles.inputForm}>
        <input
          className={styles.input}
          placeholder="Type your question..."
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
        />
        <button className={styles.sendButton} disabled={loading || !input.trim()}>Send</button>
      </form>
      {loading && <div className={styles.loading}>Thinking…</div>}
    </div>
  );
}

export default ChatPage;
