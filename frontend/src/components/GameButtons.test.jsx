/* eslint-env vitest */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import GameButtons from './GameButtons';

describe('GameButtons', () => {
  it('renders New Game and Resume Game buttons', () => {
    render(<GameButtons onNewGame={() => {}} onResumeGame={() => {}} sessionId={null} />);
    expect(screen.getByText(/new game/i)).toBeInTheDocument();
    expect(screen.getByText(/resume game/i)).toBeInTheDocument();
  });

  it('calls onNewGame when New Game is clicked', () => {
    const onNewGame = vi.fn();
    render(<GameButtons onNewGame={onNewGame} onResumeGame={() => {}} sessionId={null} />);
    fireEvent.click(screen.getByText(/new game/i));
    expect(onNewGame).toHaveBeenCalled();
  });

  it('calls onResumeGame when Resume Game is clicked and enabled', () => {
    const onResumeGame = vi.fn();
    render(<GameButtons onNewGame={() => {}} onResumeGame={onResumeGame} sessionId={'abc'} />);
    const resumeBtn = screen.getByText(/resume game/i);
    expect(resumeBtn).not.toBeDisabled();
    fireEvent.click(resumeBtn);
    expect(onResumeGame).toHaveBeenCalled();
  });

  it('disables Resume Game button if no sessionId', () => {
    render(<GameButtons onNewGame={() => {}} onResumeGame={() => {}} sessionId={null} />);
    expect(screen.getByText(/resume game/i)).toBeDisabled();
  });
});
