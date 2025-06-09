'use client';
import React from 'react';
import { auth, googleProvider } from '../firebase';
import { signInWithPopup } from 'firebase/auth';
import styles from '../styles/AuthPage.module.css';

export default function AuthPage() {
  const handleGoogleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      window.location.href = '/chat';
    } catch {
      alert('Sign-in failed. Try again.');
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <img src="/evernote-logo.png" alt="Logo" className={styles.logo} />
        <h2 className={styles.title}>Sign in</h2>
        <button className={styles.googleButton} onClick={handleGoogleLogin}>
          Sign in with Google
        </button>
        <div className={styles.divider}><span>or</span></div>
        <input
          type="text"
          className={styles.input}
          placeholder="Email address or username"
        />
        <label className={styles.remember}>
          <input type="checkbox" />
          Remember me for 30 days
        </label>
        <button className={styles.continueButton}>Continue</button>
        <div className={styles.footer}>
          Don’t have an account? <a href="/signup">Create account</a>
        </div>
      </div>
    </div>
  );
}