'use client'

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [url, setUrl] = useState('');
  const [qrCodeUrl, setQrCodeUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setQrCodeUrl('');

    try {
      console.log('Generating QR for URL:', url); // Debug log
      
      // Use GET request instead of POST
      const response = await axios.get(`/api/generate-qr?url=${encodeURIComponent(url)}`, {
        timeout: 15000 // 15 second timeout
      });
      
      console.log('Frontend received:', response.data); // Debug log
      
      if (response.data.qr_code_url) {
        setQrCodeUrl(response.data.qr_code_url);
      } else if (response.data.qr_code) {
        setQrCodeUrl(response.data.qr_code);
      } else {
        setError('QR Code generated but no image URL returned');
      }
      
    } catch (error) {
      console.error('Error generating QR Code:', error);
      setError(error.response?.data?.error || error.message || 'Failed to generate QR Code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>QR Code Generator</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL like https://example.com"
          style={styles.input}
          required
        />
        <button 
          type="submit" 
          style={{...styles.button, opacity: loading ? 0.6 : 1}} 
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate QR Code'}
        </button>
      </form>
      
      {error && (
        <div style={styles.error}>
          Error: {error}
        </div>
      )}
      
      {qrCodeUrl && (
        <div style={styles.qrContainer}>
          <img src={qrCodeUrl} alt="QR Code" style={styles.qrCode} />
        </div>
      )}
    </div>
  );
}

// Styles
const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#121212',
    color: 'white',
  },
  title: {
    margin: '0',
    lineHeight: '1.15',
    fontSize: '4rem',
    textAlign: 'center',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  input: {
    padding: '10px',
    borderRadius: '5px',
    border: 'none',
    marginTop: '20px',
    width: '300px',
    color: '#121212'
  },
  button: {
    padding: '10px 20px',
    marginTop: '20px',
    border: 'none',
    borderRadius: '5px',
    backgroundColor: '#0070f3',
    color: 'white',
    cursor: 'pointer',
  },
  error: {
    marginTop: '20px',
    padding: '10px',
    backgroundColor: '#ff4444',
    color: 'white',
    borderRadius: '5px',
    textAlign: 'center',
  },
  qrContainer: {
    marginTop: '20px',
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '10px',
  },
  qrCode: {
    maxWidth: '300px',
    height: 'auto',
  },
};