import axios from 'axios';
import { vi } from 'vitest';
import '@testing-library/jest-dom';

// Provide a default mock for axios in all tests
beforeAll(() => {
  vi.spyOn(axios, 'get').mockImplementation((url) => {
    if (url.startsWith('/api/character/')) {
      return Promise.resolve({
        data: {
          name: 'Hero',
          rpg_system: 'D&D 5e',
          data: {
            attributes: { strength: 15, agility: 12, intelligence: 14 },
            skills: ['stealth', 'arcana'],
            powers: ['fireball'],
            background: 'Wanderer',
          },
        },
      });
    }
    return Promise.reject(new Error('Unknown endpoint'));
  });
  vi.spyOn(axios, 'post').mockImplementation(() => Promise.resolve({}));
});

afterAll(() => {
  vi.restoreAllMocks();
});
