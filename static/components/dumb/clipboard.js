// Clipboard copy with a notification and a fallback mechanism.

import { showToast } from './toast.js';
import { t } from '../../i18n/i18n.js';

export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(t('Copied to clipboard!'), 'success', 2000);
  } catch {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
    showToast(t('Copied!'), 'success', 2000);
  }
}
