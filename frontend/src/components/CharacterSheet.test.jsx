/* eslint-env vitest */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import CharacterSheet from './CharacterSheet';

const character = {
  name: 'Hero',
  rpg_system: 'D&D 5e',
  data: {
    attributes: { strength: 10, dexterity: 12, intelligence: 15 },
    skills: ['stealth', 'arcana'],
    powers: ['fireball'],
    background: 'Wanderer',
  },
};

describe('CharacterSheet', () => {
  it('renders character sheet and all fields', () => {
    render(<CharacterSheet character={character} />);
    expect(screen.getByTestId('character-sheet')).toBeInTheDocument();
    expect(screen.getByText(/Name:/)).toHaveTextContent('Name: Hero');
    expect(screen.getByText(/System:/)).toHaveTextContent('System: D&D 5e');
    expect(screen.getByText(/Attributes:/)).toBeInTheDocument();
    expect(screen.getByText(/Skills:/)).toHaveTextContent('Skills: stealth, arcana');
    expect(screen.getByText(/Powers:/)).toHaveTextContent('Powers: fireball');
    expect(screen.getByText(/Background:/)).toHaveTextContent('Background: Wanderer');
    expect(screen.getByText('strength: 10')).toBeInTheDocument();
    expect(screen.getByText('dexterity: 12')).toBeInTheDocument();
    expect(screen.getByText('intelligence: 15')).toBeInTheDocument();
  });
});
