import React from 'react';

export default function DicePanel({ diceInput, setDiceInput, onRoll, diceResult }) {
  return (
    <section className="dice-panel" data-testid="dice-panel">
      <h2>Dice Roller</h2>
      <form onSubmit={onRoll} className="dice-form">
        <input
          type="text"
          value={diceInput}
          onChange={e => setDiceInput(e.target.value)}
          placeholder="e.g. 2d6"
          data-testid="dice-input"
        />
        <button type="submit">Roll</button>
      </form>
      {diceResult && <div className="dice-result" data-testid="dice-result">{diceResult}</div>}
    </section>
  );
}
