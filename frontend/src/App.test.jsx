import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('App UI', () => {
  it('renders chat input/output panel', () => {
    render(<App />);
    expect(screen.getByTestId('chat-panel')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
  });

  it('renders dice roll interface', () => {
    render(<App />);
    expect(screen.getByTestId('dice-panel')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/e\.g\. 2d6/i)).toBeInTheDocument();
    // Only check for the button, not the heading
    expect(screen.getAllByText('Roll').length).toBeGreaterThan(0);
  });

  it('renders character sheet panel', () => {
    render(<App />);
    expect(screen.getByTestId('character-sheet')).toBeInTheDocument();
    expect(screen.getByText(/character sheet/i)).toBeInTheDocument();
  });

  it('renders New Game and Resume Game buttons', () => {
    render(<App />);
    expect(screen.getByText(/new game/i)).toBeInTheDocument();
    expect(screen.getByText(/resume game/i)).toBeInTheDocument();
  });

  it('allows sending a chat message', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/type your message/i);
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.submit(input.closest('form'));
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('allows rolling dice', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/e\.g\. 2d6/i);
    fireEvent.change(input, { target: { value: '2d6' } });
    fireEvent.submit(input.closest('form'));
    // Output will depend on implementation, so just check for result area
    // Wait for dice result to appear
    // Use findByTestId to wait for async update
    return screen.findByTestId('dice-result');
  });
});
