import React from 'react';

export default function CharacterSheet({ character }) {
  return (
    <section className="character-panel" data-testid="character-sheet">
      <h2>Character Sheet</h2>
      <div><b>Name:</b> {character.name}</div>
      <div><b>System:</b> {character.rpg_system}</div>
      <div><b>Attributes:</b>
        <ul>
          {Object.entries(character.data.attributes).map(([k, v]) => (
            <li key={k}>{k}: {v}</li>
          ))}
        </ul>
      </div>
      <div><b>Skills:</b> {character.data.skills.join(", ")}</div>
      <div><b>Powers:</b> {character.data.powers.join(", ")}</div>
      <div><b>Background:</b> {character.data.background}</div>
    </section>
  );
}
