// src/components/AuthPage.jsx
import React from 'react';
import { auth, googleProvider } from '../firebase';
import { signInWithPopup } from "firebase/auth";
import { useNavigate } from 'react-router-dom';
import styles from '../styles/AuthPage.module.css';

function AuthPage() {
  const navigate = useNavigate();

  const handleGoogleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      navigate('/chat');
    } catch (err) {
      alert("Sign-in failed. Try again.");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2>Sign in to Ayurveda AI</h2>
        <button className={styles.googleButton} onClick={handleGoogleLogin}>
          Sign in with Google
        </button>
      </div>
    </div>
  );
}
export default AuthPage;
