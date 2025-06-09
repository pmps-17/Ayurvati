// src/components/ChatPage.jsx

import React, { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/router'
import { auth } from '../firebase'
import styles from '../styles/ChatPage.module.css'
import ChatBubble from './ChatBubble'
import useAuth from '../hooks/useAuth'
import { logMood } from '../components/logsApi'

export default function ChatPage({ theme, onToggleTheme }) {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: "Hi! I'm your Ayurveda personal doctor. How can I help you today?" }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [moodLogs, setMoodLogs] = useState([])
  const [showHistory, setShowHistory] = useState(false)
  const chatEndRef = useRef(null)

  const router = useRouter()
  const { user } = useAuth()

  // Auto-scroll on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Fetch mood logs when toggled
  useEffect(() => {
    if (!user?.email || !showHistory) return
    logMood(user.email)
      .then(setMoodLogs)
      .catch(() => setMoodLogs([]))
  }, [user, showHistory])

  const sendMessage = async e => {
    e.preventDefault()
    if (!input.trim()) return

    const userMsg = { sender: 'user', text: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/recommend`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: input, user_email: user?.email })
        }
      )
      const data = await res.json()
      setMessages(prev => [
        ...prev,
        { sender: 'ai', text: data.result || "Sorry, I couldn't process that." }
      ])
    } catch {
      setMessages(prev => [
        ...prev,
        { sender: 'ai', text: 'Network error. Please try again.' }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    await auth.signOut()
    router.push('/login')
  }

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>
        <span>Ayurveda Doctor AI</span>
        <div className={styles.controls}>
          <button
            onClick={() => setShowHistory(h => !h)}
            className={styles.historyToggle}
          >
            {showHistory ? 'Hide History' : 'Show History'}
          </button>
          <button onClick={onToggleTheme} className={styles.themeToggle}>
            {theme === 'dark' ? '🌙' : '☀️'}
          </button>
          <button onClick={handleLogout} className={styles.logoutButton}>
            Sign Out
          </button>
        </div>
      </div>

      {showHistory && (
        <div className={styles.historySection}>
          <h4>Mood Logs</h4>
          {moodLogs.length === 0 ? (
            <div>No mood logs yet.</div>
          ) : (
            <ul>
              {moodLogs.map((log, idx) => (
                <li key={idx}>
                  {log.timestamp}: <b>{log.mood}</b> (intensity {log.intensity})
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className={styles.messages}>
        {messages.map((msg, idx) => (
          <ChatBubble key={idx} message={msg} />
        ))}
        <div ref={chatEndRef} />
      </div>

      <form onSubmit={sendMessage} className={styles.inputForm}>
        <input
          className={styles.input}
          placeholder="Type your question..."
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </form>

      {loading && <div className={styles.loading}>Thinking…</div>}
    </div>
  )
}