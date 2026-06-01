// Theme state, centralized in the store.
// The theme is the only genuinely shared application state.

import { createStore } from './store.js';

export const THEMES = ['light', 'dark', 'hacker'];
const STORAGE_KEY = 'nt-theme';
const DEFAULT_THEME = 'dark';

function readStoredTheme() {
  return localStorage.getItem(STORAGE_KEY) || DEFAULT_THEME;
}

export function createThemeStore() {
  const store = createStore({ theme: readStoredTheme() });

  // Apply the theme to the DOM and persist it on every state change.
  store.subscribe(({ theme }) => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    document.querySelectorAll('.theme-btn[data-theme]').forEach((button) => {
      button.classList.toggle('active', button.dataset.theme === theme);
    });
  });

  function setTheme(theme) {
    if (THEMES.includes(theme)) store.setState({ theme });
  }

  function applyCurrent() {
    store.setState({ theme: store.getState().theme });
  }

  return { setTheme, applyCurrent };
}
