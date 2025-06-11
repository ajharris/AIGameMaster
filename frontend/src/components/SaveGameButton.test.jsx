import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SaveGameButton from './SaveGameButton';
import axios from 'axios';

vi.mock('axios');

describe('SaveGameButton', () => {
  const gameState = { characterId: 'abc', progress: 42 };

  it('calls POST /api/save_game with gameState and shows success', async () => {
    axios.post.mockResolvedValueOnce({});
    render(<SaveGameButton gameState={gameState} />);
    fireEvent.click(screen.getByText(/save game/i));
    await waitFor(() => expect(axios.post).toHaveBeenCalledWith('/api/save_game', gameState));
    expect(await screen.findByTestId('save-status')).toHaveTextContent('Game saved!');
  });

  it('shows error message on failure', async () => {
    axios.post.mockRejectedValueOnce(new Error('fail'));
    render(<SaveGameButton gameState={gameState} />);
    fireEvent.click(screen.getByText(/save game/i));
    expect(await screen.findByTestId('save-error')).toHaveTextContent('Failed to save game');
  });
});
