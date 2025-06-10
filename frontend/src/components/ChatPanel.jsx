import React from 'react';

export default function ChatPanel({ messages, chatInput, setChatInput, onSubmit }) {
  return (
    <section className="chat-panel" data-testid="chat-panel">
      <h2>Chat</h2>
      <div className="chat-messages" data-testid="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`msg msg-${msg.sender}`}>
            <b>{msg.sender === "user" ? "You" : msg.sender === "ai" ? "AI" : "System"}:</b> {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={onSubmit} className="chat-form">
        <input
          type="text"
          value={chatInput}
          onChange={e => setChatInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </section>
  );
}
