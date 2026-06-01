// Client-side tool (no backend): Base64 / Hex / URL encoding.

import { byId } from '../../utils/dom.js';

export function mountBase64Tool({ notify }) {
  const input = byId('encodeInput');
  if (!input) return;

  input.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'Enter') encode('base64', notify);
  });

  // Mode buttons use delegation via data-encode.
  document.querySelectorAll('[data-encode]').forEach((button) => {
    button.addEventListener('click', () => encode(button.dataset.encode, notify));
  });
}

function encode(mode, notify) {
  const input = byId('encodeInput')?.value ?? '';
  const output = byId('encodeOutput');
  if (!output) return;
  try {
    output.value = transform(mode, input);
  } catch (error) {
    notify(`Error: ${error.message}`, 'error');
    output.value = '';
  }
}

function transform(mode, input) {
  switch (mode) {
    case 'base64':
      return btoa(unescape(encodeURIComponent(input)));
    case 'base64d':
      return decodeURIComponent(escape(atob(input)));
    case 'hex':
      return Array.from(new TextEncoder().encode(input))
        .map((byte) => byte.toString(16).padStart(2, '0'))
        .join(' ');
    case 'hexd': {
      const bytes = input.replace(/\s+/g, '').match(/.{1,2}/g) || [];
      return new TextDecoder().decode(new Uint8Array(bytes.map((byte) => parseInt(byte, 16))));
    }
    case 'url':
      return encodeURIComponent(input);
    case 'urld':
      return decodeURIComponent(input);
    default:
      return '';
  }
}
