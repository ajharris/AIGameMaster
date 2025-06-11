import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResumeGameButton from './ResumeGameButton';
import axios from 'axios';

vi.mock('axios');

describe('ResumeGameButton', () => {
  const characterId = 'abc';
  const setGameState = vi.fn();

  beforeEach(() => {
    setGameState.mockClear();
  });

  it('calls GET /api/load_game/:characterId and sets game state on success', async () => {
    axios.get.mockResolvedValueOnce({ data: { characterId, progress: 99 } });
    render(<ResumeGameButton characterId={characterId} setGameState={setGameState} />);
    fireEvent.click(screen.getByText(/resume game/i));
    await waitFor(() => expect(axios.get).toHaveBeenCalledWith(`/api/load_game/${characterId}`));
    expect(setGameState).toHaveBeenCalledWith({ characterId, progress: 99 });
  });

  it('shows "No saved game" if no data returned', async () => {
    axios.get.mockResolvedValueOnce({ data: null });
    render(<ResumeGameButton characterId={characterId} setGameState={setGameState} />);
    fireEvent.click(screen.getByText(/resume game/i));
    expect(await screen.findByTestId('resume-nogame')).toHaveTextContent('No saved game');
    expect(setGameState).not.toHaveBeenCalled();
  });

  it('shows error message on fetch failure', async () => {
    axios.get.mockRejectedValueOnce(new Error('fail'));
    render(<ResumeGameButton characterId={characterId} setGameState={setGameState} />);
    fireEvent.click(screen.getByText(/resume game/i));
    expect(await screen.findByTestId('resume-error')).toHaveTextContent('Failed to load game');
    expect(setGameState).not.toHaveBeenCalled();
  });
});
