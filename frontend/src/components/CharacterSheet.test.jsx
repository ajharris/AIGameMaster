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
    const sheet = screen.getByTestId('character-sheet');
    expect(sheet).toBeInTheDocument();
    expect(sheet).toHaveTextContent(/Name:/);
    expect(sheet).toHaveTextContent(/Hero/);
    expect(sheet).toHaveTextContent(/System:/);
    expect(sheet).toHaveTextContent(/D&D 5e/);
    expect(sheet).toHaveTextContent(/Attributes:/);
    expect(sheet).toHaveTextContent(/Skills:/);
    expect(sheet).toHaveTextContent(/stealth/);
    expect(sheet).toHaveTextContent(/arcana/);
    expect(sheet).toHaveTextContent(/Powers:/);
    expect(sheet).toHaveTextContent(/fireball/);
    expect(sheet).toHaveTextContent(/Background:/);
    expect(sheet).toHaveTextContent(/Wanderer/);
    expect(sheet).toHaveTextContent(/strength/);
    expect(sheet).toHaveTextContent(/10/);
    expect(sheet).toHaveTextContent(/dexterity/);
    expect(sheet).toHaveTextContent(/12/);
    expect(sheet).toHaveTextContent(/intelligence/);
    expect(sheet).toHaveTextContent(/15/);
  });
});
