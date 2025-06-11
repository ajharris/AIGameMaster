import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function CharacterSheet({ characterId }) {
  const [character, setCharacter] = useState(null);
  const [attributes, setAttributes] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submitStatus, setSubmitStatus] = useState('');

  useEffect(() => {
    setLoading(true);
    axios.get(`/api/character/${characterId}`)
      .then(res => {
        setCharacter(res.data);
        setAttributes(res.data.data.attributes);
        setLoading(false);
      })
      .catch(e => {
        setError('Failed to load character');
        setLoading(false);
      });
  }, [characterId]);

  const handleAttrChange = (attr, value) => {
    setAttributes(a => ({ ...a, [attr]: Number(value) }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitStatus('');
    try {
      await axios.post(`/api/character/${characterId}/update`, {
        ...character,
        data: {
          ...character.data,
          attributes,
        },
      });
      setSubmitStatus('Saved!');
    } catch {
      setSubmitStatus('Error saving');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!character) return null;

  return (
    <section className="character-panel" data-testid="character-sheet">
      <h2>Character Sheet</h2>
      <div><b>Name:</b> {character.name}</div>
      <div><b>System:</b> {character.rpg_system}</div>
      <form onSubmit={handleSubmit}>
        <div><b>Attributes:</b>
          <ul>
            {Object.entries(attributes).map(([k, v]) => (
              <li key={k}>
                {k}: <input
                  type="number"
                  value={v}
                  onChange={e => handleAttrChange(k, e.target.value)}
                  data-testid={`attr-${k}`}
                />
              </li>
            ))}
          </ul>
        </div>
        <button type="submit">Save</button>
        {submitStatus && <span data-testid="submit-status">{submitStatus}</span>}
      </form>
      <div><b>Skills:</b> {character.data.skills.join(", ")}</div>
      <div><b>Powers:</b> {character.data.powers.join(", ")}</div>
      <div><b>Background:</b> {character.data.background}</div>
    </section>
  );
}
