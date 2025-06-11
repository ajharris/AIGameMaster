import React, { useState } from 'react';
import axios from 'axios';

export default function ResumeGameButton({ characterId, setGameState }) {
  const [error, setError] = useState('');
  const [noGame, setNoGame] = useState(false);

  const handleResume = async () => {
    setError('');
    setNoGame(false);
    try {
      const res = await axios.get(`/api/load_game/${characterId}`);
      if (res.data) {
        setGameState(res.data);
      } else {
        setNoGame(true);
      }
    } catch (err) {
      setError('Failed to load game');
    }
  };

  return (
    <div>
      <button onClick={handleResume}>Resume Game</button>
      {noGame && <div data-testid="resume-nogame">No saved game</div>}
      {error && <div data-testid="resume-error">{error}</div>}
    </div>
  );
}
