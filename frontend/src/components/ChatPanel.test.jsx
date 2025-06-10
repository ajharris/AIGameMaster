/* eslint-env vitest */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatPanel from './ChatPanel';

const baseProps = {
  messages: [],
  chatInput: '',
  setChatInput: () => {},
  onSubmit: () => {},
};

describe('ChatPanel', () => {
  it('renders chat panel and input', () => {
    render(<ChatPanel {...baseProps} />);
    expect(screen.getByTestId('chat-panel')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
  });

  it('renders messages in order', () => {
    const messages = [
      { sender: 'user', text: 'Hi' },
      { sender: 'ai', text: 'Hello' },
      { sender: 'system', text: 'System message' },
    ];
    render(<ChatPanel {...baseProps} messages={messages} />);
    expect(screen.getByText('You: Hi')).toBeInTheDocument();
    expect(screen.getByText('AI: Hello')).toBeInTheDocument();
    expect(screen.getByText('System: System message')).toBeInTheDocument();
  });

  it('calls setChatInput on input change', () => {
    const setChatInput = vi.fn();
    render(<ChatPanel {...baseProps} setChatInput={setChatInput} />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Test' } });
    expect(setChatInput).toHaveBeenCalledWith('Test');
  });

  it('calls onSubmit when form is submitted', () => {
    const onSubmit = vi.fn((e) => e.preventDefault());
    render(<ChatPanel {...baseProps} onSubmit={onSubmit} />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.submit(input.closest('form'));
    expect(onSubmit).toHaveBeenCalled();
  });
});
