// UI language state, centralized in the store. Default is English; the choice
// is persisted in localStorage and applied to the DOM on every change.

import { createStore } from './store.js';
import { setLanguage, applyDomTranslations } from '../i18n/i18n.js';

export const LANGUAGES = ['en', 'ru'];
const STORAGE_KEY = 'nt-lang';
const DEFAULT_LANGUAGE = 'en';

function readStoredLanguage() {
  return localStorage.getItem(STORAGE_KEY) || DEFAULT_LANGUAGE;
}

export function createLanguageStore() {
  const store = createStore({ lang: readStoredLanguage() });

  store.subscribe(({ lang }) => {
    setLanguage(lang);
    localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.setAttribute('lang', lang);
    applyDomTranslations();
    document.querySelectorAll('.lang-btn').forEach((button) => {
      button.classList.toggle('active', button.dataset.lang === lang);
    });
  });

  function setLang(lang) {
    if (LANGUAGES.includes(lang)) store.setState({ lang });
  }

  function applyCurrent() {
    store.setState({ lang: store.getState().lang });
  }

  return { setLang, applyCurrent };
}
