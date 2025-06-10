import React from 'react';

export default function GameButtons({ onNewGame, onResumeGame, sessionId }) {
  return (
    <div className="game-buttons">
      <button onClick={onNewGame}>New Game</button>
      <button onClick={onResumeGame} disabled={!sessionId}>Resume Game</button>
    </div>
  );
}
