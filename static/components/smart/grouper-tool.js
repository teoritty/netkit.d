// Smart component: network grouping. Builds a JSON array of pairs from the form rows.

import { byId, setLoading } from '../../utils/dom.js';
import { appendRow, removeIconMarkup } from '../dumb/dynamic-rows.js';
import { renderNetworkGroups } from '../dumb/result-views.js';
import { buildMaskOptions } from '../../utils/mask-options.js';
import { t, applyDomTranslations } from '../../i18n/i18n.js';

let rowIndex = 1;

export function mountGrouperTool({ calculationService, notify }) {
  const form = byId('find-same-network-form');
  if (!form) return;

  byId('addNetworkRowBtn')?.addEventListener('click', addRow);

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const pairs = collectPairs(form);
    if (!pairs.length) {
      notify(t('Add at least one address'), 'error');
      return;
    }
    setLoading(button, true);
    try {
      const data = await calculationService.groupNetworks(pairs);
      renderNetworkGroups(byId('networkGroupResult'), data.networks);
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}

function collectPairs(form) {
  const rows = form.querySelectorAll('.ip-row');
  const pairs = [];
  rows.forEach((row) => {
    const ip = row.querySelector('.js-group-ip')?.value.trim();
    const mask = row.querySelector('.js-group-mask')?.value;
    if (ip) pairs.push({ ip, mask });
  });
  return pairs;
}

function addRow() {
  appendRow(
    byId('network-rows'),
    `<div class="ip-row" data-row-index="${rowIndex}">
      <div class="form-group">
        <label class="form-label">IP address</label>
        <input type="text" class="form-input text-mono js-group-ip" placeholder="10.0.0.2">
      </div>
      <div class="form-group">
        <label class="form-label">Mask</label>
        <select class="form-select js-group-mask">${buildMaskOptions(24)}</select>
      </div>
      <button type="button" class="remove-btn" title="Remove" aria-label="Remove row">${removeIconMarkup()}</button>
    </div>`
  );
  rowIndex += 1;
  applyDomTranslations(); // localize the freshly added row when RU is active
}
