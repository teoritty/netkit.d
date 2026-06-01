// Internationalization core.
//   t(en)                  — translate a dynamic string to the current language
//   applyDomTranslations() — swap known phrases in the static DOM (text + attrs)
// English is the default; switching to "ru" replaces known phrases and switching
// back restores the captured English originals.

import { RU } from './translations.js';

const ATTRS = ['placeholder', 'title', 'aria-label'];
const textOriginals = new WeakMap(); // text node -> original English nodeValue
const attrOriginals = new WeakMap(); // element  -> { attr: original English value }

let currentLang = 'en';

export function setLanguage(lang) {
  currentLang = lang;
}

export function getLanguage() {
  return currentLang;
}

export function t(english) {
  return currentLang === 'ru' ? RU[english] ?? english : english;
}

export function applyDomTranslations() {
  const roots = [
    document.querySelector('.sidebar'),
    document.querySelector('.main-content'),
    document.querySelector('.mobile-header'),
  ].filter(Boolean);
  roots.forEach(translateTextNodes);
  roots.forEach(translateAttributes);
}

function translateTextNodes(root) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    let original = textOriginals.get(node);
    if (original === undefined) {
      const trimmed = node.nodeValue.trim();
      if (!trimmed || !(trimmed in RU)) continue; // only track translatable phrases
      original = node.nodeValue;
      textOriginals.set(node, original);
    }
    const trimmed = original.trim();
    node.nodeValue =
      currentLang === 'ru' ? original.replace(trimmed, RU[trimmed]) : original;
  }
}

function translateAttributes(root) {
  root.querySelectorAll('[placeholder],[title],[aria-label]').forEach((element) => {
    ATTRS.forEach((attr) => {
      if (!element.hasAttribute(attr)) return;
      const store = attrOriginals.get(element) || {};
      if (store[attr] === undefined) {
        const value = element.getAttribute(attr).trim();
        if (!(value in RU)) return;
        store[attr] = element.getAttribute(attr);
        attrOriginals.set(element, store);
      }
      const original = store[attr];
      const trimmed = original.trim();
      element.setAttribute(
        attr,
        currentLang === 'ru' ? original.replace(trimmed, RU[trimmed]) : original
      );
    });
  });
}
