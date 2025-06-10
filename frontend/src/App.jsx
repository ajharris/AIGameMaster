import { useState } from 'react';
import './App.css';
import ChatPanel from './components/ChatPanel';
import DicePanel from './components/DicePanel';
import CharacterSheet from './components/CharacterSheet';
import GameButtons from './components/GameButtons';

function App() {
  // Chat state
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");

  // Dice roll state
  const [diceInput, setDiceInput] = useState("");
  const [diceResult, setDiceResult] = useState(null);

  // Character sheet state (simple example)
  const [character] = useState({
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
    } catch {
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
        <GameButtons onNewGame={handleNewGame} onResumeGame={handleResumeGame} sessionId={sessionId} />
      </header>
      <main className="main-layout">
        <ChatPanel
          messages={messages}
          chatInput={chatInput}
          setChatInput={setChatInput}
          onSubmit={handleChatSubmit}
        />
        <DicePanel
          diceInput={diceInput}
          setDiceInput={setDiceInput}
          onRoll={handleDiceRoll}
          diceResult={diceResult}
        />
        <CharacterSheet character={character} />
      </main>
    </div>
  );
}

export default App;
