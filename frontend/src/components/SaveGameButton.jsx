import React, { useState } from 'react';
import axios from 'axios';

export default function SaveGameButton({ gameState }) {
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  const handleSave = async () => {
    setStatus('');
    setError('');
    try {
      await axios.post('/api/save_game', gameState);
      setStatus('Game saved!');
    } catch (err) {
      setError('Failed to save game');
    }
  };

  return (
    <div>
      <button onClick={handleSave}>Save Game</button>
      {status && <div data-testid="save-status">{status}</div>}
      {error && <div data-testid="save-error">{error}</div>}
    </div>
  );
}
