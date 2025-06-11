/* eslint-env vitest */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import CharacterSheet from './CharacterSheet';
import axios from 'axios';

vi.mock('axios');

const mockCharacter = {
  name: 'Hero',
  rpg_system: 'D&D 5e',
  data: {
    attributes: { strength: 15, agility: 12, intelligence: 14 },
    skills: ['stealth', 'arcana'],
    powers: ['fireball'],
    background: 'Wanderer',
  },
};

describe('CharacterSheet (with backend)', () => {
  beforeEach(() => {
    axios.get.mockReset();
    axios.post.mockReset();
  });

  it('mocks backend call and displays character name and stats after loading', async () => {
    axios.get.mockResolvedValueOnce({ data: mockCharacter });
    render(<CharacterSheet characterId={1} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByTestId('character-sheet')).toBeInTheDocument());
    expect(screen.getByText(/Hero/)).toBeInTheDocument();
    expect(screen.getByText(/D&D 5e/)).toBeInTheDocument();
    expect(screen.getByDisplayValue('15')).toBeInTheDocument();
    expect(screen.getByDisplayValue('12')).toBeInTheDocument();
    expect(screen.getByDisplayValue('14')).toBeInTheDocument();
  });

  it('renders and verifies character name and stat values after data loads', async () => {
    axios.get.mockResolvedValueOnce({ data: mockCharacter });
    render(<CharacterSheet characterId={1} />);
    await waitFor(() => expect(screen.getByTestId('character-sheet')).toBeInTheDocument());
    expect(screen.getByText('Hero')).toBeInTheDocument();
    expect(screen.getByTestId('attr-strength')).toHaveValue(15);
    expect(screen.getByTestId('attr-agility')).toHaveValue(12);
    expect(screen.getByTestId('attr-intelligence')).toHaveValue(14);
  });

  it('simulates user changing a stat input and checks value updates', async () => {
    axios.get.mockResolvedValueOnce({ data: mockCharacter });
    render(<CharacterSheet characterId={1} />);
    await waitFor(() => expect(screen.getByTestId('character-sheet')).toBeInTheDocument());
    const strengthInput = screen.getByTestId('attr-strength');
    fireEvent.change(strengthInput, { target: { value: 17 } });
    expect(strengthInput).toHaveValue(17);
  });

  it('mocks API call for submitting updated character data', async () => {
    axios.get.mockResolvedValueOnce({ data: mockCharacter });
    axios.post.mockResolvedValueOnce({});
    render(<CharacterSheet characterId={1} />);
    await waitFor(() => expect(screen.getByTestId('character-sheet')).toBeInTheDocument());
    const strengthInput = screen.getByTestId('attr-strength');
    fireEvent.change(strengthInput, { target: { value: 17 } });
    const saveBtn = screen.getByText(/save/i);
    fireEvent.click(saveBtn);
    await waitFor(() => expect(axios.post).toHaveBeenCalled());
    expect(axios.post).toHaveBeenCalledWith(
      '/api/character/1/update',
      expect.objectContaining({
        ...mockCharacter,
        data: expect.objectContaining({
          ...mockCharacter.data,
          attributes: expect.objectContaining({ strength: 17 }),
        }),
      })
    );
    await waitFor(() => expect(screen.getByTestId('submit-status')).toHaveTextContent('Saved!'));
  });
});
