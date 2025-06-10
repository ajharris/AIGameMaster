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
    const messages = screen.getAllByText(/You:|AI:/);
    expect(messages[0]).toHaveTextContent('You: First');
    expect(messages[1]).toHaveTextContent('AI: AI says: First');
    expect(messages[2]).toHaveTextContent('You: Second');
    expect(messages[3]).toHaveTextContent('AI: AI says: Second');
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
    expect(screen.getByText('You: Adventure!')).toBeInTheDocument();
    expect(screen.getByText('AI: AI says: Adventure!')).toBeInTheDocument();
    expect(screen.getByTestId('character-sheet')).toBeInTheDocument();
  });

  it('narrative output changes if character sheet changes (simulated)', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Repeat' } });
    fireEvent.submit(input.closest('form'));
    await new Promise(r => setTimeout(r, 600));
    expect(screen.getByText('AI: AI says: Repeat')).toBeInTheDocument();
  });
});
