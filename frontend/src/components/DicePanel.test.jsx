/* eslint-env vitest */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import DicePanel from './DicePanel';

describe('DicePanel', () => {
  it('renders dice panel and input', () => {
    render(<DicePanel diceInput="" setDiceInput={() => {}} onRoll={() => {}} diceResult={null} />);
    expect(screen.getByTestId('dice-panel')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/e\.g\. 2d6/i)).toBeInTheDocument();
    expect(screen.getByText('Roll')).toBeInTheDocument();
  });

  it('shows dice result if present', () => {
    render(<DicePanel diceInput="2d6" setDiceInput={() => {}} onRoll={() => {}} diceResult="Rolls: [3, 4] Total: 7" />);
    expect(screen.getByTestId('dice-result')).toHaveTextContent('Rolls: [3, 4] Total: 7');
  });

  it('calls setDiceInput on input change', () => {
    const setDiceInput = vi.fn();
    render(<DicePanel diceInput="" setDiceInput={setDiceInput} onRoll={() => {}} diceResult={null} />);
    const input = screen.getByPlaceholderText(/e\.g\. 2d6/i);
    fireEvent.change(input, { target: { value: '1d20' } });
    expect(setDiceInput).toHaveBeenCalledWith('1d20');
  });

  it('calls onRoll when form is submitted', () => {
    const onRoll = vi.fn((e) => e.preventDefault());
    render(<DicePanel diceInput="2d6" setDiceInput={() => {}} onRoll={onRoll} diceResult={null} />);
    const input = screen.getByPlaceholderText(/e\.g\. 2d6/i);
    fireEvent.change(input, { target: { value: '2d6' } });
    fireEvent.submit(input.closest('form'));
    expect(onRoll).toHaveBeenCalled();
  });
});
