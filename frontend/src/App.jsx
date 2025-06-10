import { useState } from 'react';
import './App.css';

function App() {
  // Chat state
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");

  // Dice roll state
  const [diceInput, setDiceInput] = useState("");
  const [diceResult, setDiceResult] = useState(null);

  // Character sheet state (simple example)
  const [character, setCharacter] = useState({
    name: "Hero",
    rpg_system: "D&D 5e",
    data: {
      attributes: { strength: 10, dexterity: 12, intelligence: 15 },
      skills: ["stealth", "arcana"],
      powers: ["fireball"],
      background: "Wanderer"
    }
  });

  // Game session state
  const [sessionId, setSessionId] = useState(null);

  // Chat submit handler
  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    setMessages((msgs) => [...msgs, { sender: "user", text: chatInput }]);
    // Simulate AI response (replace with API call)
    setTimeout(() => {
      setMessages((msgs) => [...msgs, { sender: "ai", text: `AI says: ${chatInput}` }]);
    }, 500);
    setChatInput("");
  };

  // Dice roll handler
  const handleDiceRoll = async (e) => {
    e.preventDefault();
    if (!diceInput.match(/^\d+d\d+$/i)) {
      setDiceResult("Invalid format. Use XdY.");
      return;
    }
    // Call backend API
    try {
      const resp = await fetch("/api/roll_dice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression: diceInput })
      });
      const data = await resp.json();
      if (resp.ok) {
        setDiceResult(`Rolls: [${data.rolls.join(", ")}] Total: ${data.total}`);
      } else {
        setDiceResult(data.error || "Error");
      }
    } catch (err) {
      setDiceResult("Network error");
    }
  };

  // New Game handler
  const handleNewGame = async () => {
    const resp = await fetch("/api/start_session", { method: "POST" });
    const data = await resp.json();
    setSessionId(data.session_id || null);
    setMessages([]);
  };

  // Resume Game handler
  const handleResumeGame = async () => {
    if (!sessionId) return;
    const resp = await fetch("/api/continue_session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId })
    });
    const data = await resp.json();
    setMessages((msgs) => [...msgs, { sender: "system", text: data.message || data.error || "Resumed" }]);
  };

  return (
    <div className="app-container">
      <header>
        <h1>AI Game Master</h1>
        <div className="game-buttons">
          <button onClick={handleNewGame}>New Game</button>
          <button onClick={handleResumeGame} disabled={!sessionId}>Resume Game</button>
        </div>
      </header>
      <main className="main-layout">
        <section className="chat-panel" data-testid="chat-panel">
          <h2>Chat</h2>
          <div className="chat-messages" data-testid="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`msg msg-${msg.sender}`}>
                <b>{msg.sender === "user" ? "You" : msg.sender === "ai" ? "AI" : "System"}:</b> {msg.text}
              </div>
            ))}
          </div>
          <form onSubmit={handleChatSubmit} className="chat-form">
            <input
              type="text"
              value={chatInput}
              onChange={e => setChatInput(e.target.value)}
              placeholder="Type your message..."
            />
            <button type="submit">Send</button>
          </form>
        </section>
        <section className="dice-panel" data-testid="dice-panel">
          <h2>Dice Roller</h2>
          <form onSubmit={handleDiceRoll} className="dice-form">
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
      </main>
    </div>
  );
}

export default App;
