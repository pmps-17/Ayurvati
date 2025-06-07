// src/components/ChatBubble.jsx
import React from 'react';
import styles from '../styles/ChatBubble.module.css';

function ChatBubble({ message }) {
  const { sender, text } = message;
  return (
    <div className={sender === 'user' ? styles.user : styles.ai}>
      {text}
    </div>
  );
}

export default ChatBubble;
