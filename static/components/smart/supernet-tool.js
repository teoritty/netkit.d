// Smart component: network summarization (supernet).

import { byId, setLoading, escapeHtml } from '../../utils/dom.js';
import { appendRow, removeIconMarkup } from '../dumb/dynamic-rows.js';
import { renderRows } from '../dumb/result-views.js';
import { t, applyDomTranslations } from '../../i18n/i18n.js';

export function mountSupernetTool({ calculationService, notify }) {
  const form = byId('supernet-form');
  if (!form) return;

  byId('addSupernetRowBtn')?.addEventListener('click', () => {
    appendRow(
      byId('supernetRows'),
      `<div class="network-entry-row">
        <input type="text" class="form-input text-mono" placeholder="10.0.0.0/24">
        <button type="button" class="remove-btn" title="Remove" aria-label="Remove network">${removeIconMarkup()}</button>
      </div>`
    );
    applyDomTranslations();
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const networks = [...document.querySelectorAll('#supernetRows .form-input')]
      .map((input) => input.value.trim())
      .filter(Boolean);

    if (!networks.length) {
      notify(t('Add at least one network'), 'error');
      return;
    }

    setLoading(button, true);
    try {
      const data = await calculationService.summarizeSupernet(networks);
      renderRows(
        byId('supernetTableBody'),
        data.summarized.map((item) => [
          `<td class="mono">${escapeHtml(item.cidr)}</td>`,
          `<td class="mono">${escapeHtml(item.network)}</td>`,
          `<td class="mono">${escapeHtml(item.broadcast)}</td>`,
          `<td>${escapeHtml(item.hosts)}</td>`,
          `<td>/${escapeHtml(item.prefix)}</td>`,
        ])
      );
      byId('supernetStats').textContent = `${data.input_count} → ${data.output_count} ${t('route(s)')}`;
      byId('supernetResult').classList.add('visible');
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
