// Client-side tool (no backend): convert numbers between bases.

import { byId } from '../../utils/dom.js';
import { copyToClipboard } from '../dumb/clipboard.js';
import { t } from '../../i18n/i18n.js';

export function mountBaseConverterTool({ notify }) {
  const form = byId('converterForm');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const number = byId('number').value.trim();
    const fromBase = Number.parseInt(byId('fromBase').value, 10);
    const toBase = Number.parseInt(byId('toBase').value, 10);
    const decimal = Number.parseInt(number, fromBase);
    if (Number.isNaN(decimal)) {
      notify(t('Invalid number format'), 'error');
      return;
    }
    const converted = decimal.toString(toBase).toUpperCase();
    byId('convertResult').textContent = converted;
    byId('convertResultBox').classList.add('visible');
    byId('convertCopyBtn').onclick = () => copyToClipboard(converted);
  });
}
