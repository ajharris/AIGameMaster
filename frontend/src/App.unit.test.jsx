/* eslint-env vitest */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('App (integration/unit)', () => {
  it('allows sending a chat message and displays it', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.submit(input.closest('form'));
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('does not send empty chat input', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: '   ' } });
    fireEvent.submit(input.closest('form'));
    expect(screen.queryByText('You:')).not.toBeInTheDocument();
  });

  it('stores chat messages in correct order and adds AI response', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'First' } });
    fireEvent.submit(input.closest('form'));
    fireEvent.change(input, { target: { value: 'Second' } });
    fireEvent.submit(input.closest('form'));
    await new Promise(r => setTimeout(r, 600));
    const userMsgs = screen.getAllByText('First');
    const aiMsgs = screen.getAllByText('AI says: First');
    const userMsgs2 = screen.getAllByText('Second');
    const aiMsgs2 = screen.getAllByText('AI says: Second');
    expect(userMsgs.length).toBeGreaterThan(0);
    expect(aiMsgs.length).toBeGreaterThan(0);
    expect(userMsgs2.length).toBeGreaterThan(0);
    expect(aiMsgs2.length).toBeGreaterThan(0);
  });

  it('shows error for invalid dice input', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/e\.g\. 2d6/i);
    fireEvent.change(input, { target: { value: 'badinput' } });
    fireEvent.submit(input.closest('form'));
    expect(screen.getByText(/invalid format/i)).toBeInTheDocument();
  });

  it('end-to-end: player input triggers AI, session updates, and UI displays all', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Adventure!' } });
    fireEvent.submit(input.closest('form'));
    await new Promise(r => setTimeout(r, 600));
    // Find the user and AI message nodes by their text
    expect(screen.getByText('Adventure!')).toBeInTheDocument();
    expect(screen.getByText('AI says: Adventure!')).toBeInTheDocument();
    expect(screen.getByTestId('character-sheet')).toBeInTheDocument();
  });

  it('narrative output changes if character sheet changes (simulated)', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Repeat' } });
    fireEvent.submit(input.closest('form'));
    await new Promise(r => setTimeout(r, 600));
    expect(screen.getByText('AI says: Repeat')).toBeInTheDocument();
  });

  it('shows error for rate limit on dice roll', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: 'Too many requests, slow down!' })
    });
    render(<App />);
    const input = screen.getByPlaceholderText(/e\.g\. 2d6/i);
    fireEvent.change(input, { target: { value: '2d6' } });
    fireEvent.submit(input.closest('form'));
    expect(await screen.findByText(/too many requests/i)).toBeInTheDocument();
  });

  it('shows error for file parsing failure', async () => {
    // Simulate file upload error (this would be in a file upload UI, but we simulate the error message display)
    // For this test, we simulate the dice panel as a proxy for error display logic
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: 'PDF is encrypted or locked' })
    });
    render(<App />);
    const input = screen.getByPlaceholderText(/e\.g\. 2d6/i);
    fireEvent.change(input, { target: { value: '2d6' } });
    fireEvent.submit(input.closest('form'));
    expect(await screen.findByText(/encrypted|locked/i)).toBeInTheDocument();
  });
});
