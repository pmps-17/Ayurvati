// src/App.jsx
import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AuthPage from './components/AuthPage';
import ChatPage from './components/ChatPage';
import './styles/global.module.css';
import styles from './styles/variables.module.css';

function App() {
  const [theme, setTheme] = useState(
    window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  );

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<AuthPage setTheme={setTheme} theme={theme} />} />
        <Route path="/chat" element={<ChatPage setTheme={setTheme} theme={theme} />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
