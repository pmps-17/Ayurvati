// src/components/Header.jsx
import React from 'react'
import styles from '../styles/Header.module.css'
import { auth } from '../firebase'
import { useRouter } from 'next/router'

export default function Header({ user, theme, onToggleTheme }) {
  const router = useRouter()

  const handleLogout = async () => {
    try {
      await auth.signOut()
      router.push('/login')
    } catch (err) {
      console.error('Logout failed', err)
    }
  }

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <span className={styles.logo}>🌱 Ayurvati AI</span>
      </div>
      <div className={styles.right}>
        <button onClick={onToggleTheme} className={styles.themeToggle}>
          {theme === 'dark' ? '🌙' : '☀️'}
        </button>
        {user && (
          <>
            <span className={styles.userName}>
              {user.displayName}
              {user.photoURL && (
                <img
                  src={user.photoURL}
                  alt="profile"
                  className={styles.avatar}
                />
              )}
            </span>
            <button onClick={handleLogout} className={styles.logoutButton}>
              Sign Out
            </button>
          </>
        )}
      </div>
    </header>
  )
}