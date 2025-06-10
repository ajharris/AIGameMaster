/* eslint-env vitest */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('TTS (Text-to-Speech) integration', () => {
  let originalSpeechSynthesis;
  let originalUtterance;
  let speakMock;

  beforeEach(() => {
    // Mock window.speechSynthesis
    originalSpeechSynthesis = window.speechSynthesis;
    speakMock = vi.fn();
    window.speechSynthesis = { speak: speakMock };
    // Mock window.SpeechSynthesisUtterance
    originalUtterance = window.SpeechSynthesisUtterance;
    window.SpeechSynthesisUtterance = function(text) {
      this.text = text;
    };
  });

  afterEach(() => {
    window.speechSynthesis = originalSpeechSynthesis;
    window.SpeechSynthesisUtterance = originalUtterance;
  });

  it('TTS is off by default and does not speak AI messages', async () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.submit(input.closest('form'));
    await waitFor(() => expect(screen.getByText('AI says: Hello')).toBeInTheDocument());
    expect(speakMock).not.toHaveBeenCalled();
  });

  it('TTS can be enabled and speaks AI messages', async () => {
    render(<App />);
    const ttsBtn = screen.getByTestId('tts-toggle');
    fireEvent.click(ttsBtn); // Enable TTS
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Speak this' } });
    fireEvent.submit(input.closest('form'));
    await waitFor(() => expect(screen.getByText('AI says: Speak this')).toBeInTheDocument());
    expect(speakMock).toHaveBeenCalledWith(expect.objectContaining({ text: 'AI says: Speak this' }));
  });

  it('TTS can be toggled off and on', () => {
    render(<App />);
    const ttsBtn = screen.getByTestId('tts-toggle');
    expect(ttsBtn).toHaveTextContent('Enable TTS');
    fireEvent.click(ttsBtn);
    expect(ttsBtn).toHaveTextContent('Disable TTS');
    fireEvent.click(ttsBtn);
    expect(ttsBtn).toHaveTextContent('Enable TTS');
  });
});
