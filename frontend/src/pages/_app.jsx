// src/pages/_app.jsx
import React from 'react'
import '../styles/global.css'   // adjust or remove if you have other global styles

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}