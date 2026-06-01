// Delegated handling of all copy buttons.
// Supports three text sources:
//   data-copy-target  — textContent of the element with that id
//   data-copy-input   — value of the input/textarea with that id
//   data-copy-text    — text directly in the attribute
import { copyToClipboard } from './clipboard.js';
import { byId } from '../../utils/dom.js';

export function initCopyDelegation(root) {
  root.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-copy-target],[data-copy-input],[data-copy-text]');
    if (!trigger) return;
    copyToClipboard(resolveText(trigger));
  });
}

function resolveText(trigger) {
  if (trigger.dataset.copyTarget) {
    return byId(trigger.dataset.copyTarget)?.textContent ?? '';
  }
  if (trigger.dataset.copyInput) {
    return byId(trigger.dataset.copyInput)?.value ?? '';
  }
  return trigger.dataset.copyText ?? '';
}
