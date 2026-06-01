// Smart component: VLSM network splitting.

import { byId, setLoading, escapeHtml } from '../../utils/dom.js';
import { appendRow, removeIconMarkup } from '../dumb/dynamic-rows.js';
import { renderRows } from '../dumb/result-views.js';
import { copyToClipboard } from '../dumb/clipboard.js';
import { t, applyDomTranslations } from '../../i18n/i18n.js';

export function mountVlsmTool({ calculationService, notify }) {
  const form = byId('vlsm-form');
  if (!form) return;

  byId('addVlsmReqBtn')?.addEventListener('click', () => {
    appendRow(
      byId('vlsmRequirements'),
      `<div class="req-row">
        <input type="number" class="form-input text-mono vlsm-req" placeholder="50" min="1" max="16777214">
        <button type="button" class="remove-btn" title="Remove" aria-label="Remove requirement">${removeIconMarkup()}</button>
      </div>`
    );
    applyDomTranslations();
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const network = byId('vlsmNetwork').value.trim();
    const requirements = [...document.querySelectorAll('.vlsm-req')]
      .map((input) => Number.parseInt(input.value, 10))
      .filter((value) => !Number.isNaN(value) && value > 0);

    if (!requirements.length) {
      notify(t('Add at least one requirement'), 'error');
      return;
    }

    setLoading(button, true);
    try {
      const data = await calculationService.splitVlsm(network, requirements);
      renderRows(
        byId('vlsmTableBody'),
        data.subnets.map((subnet, index) => [
          `<td>${index + 1}</td>`,
          `<td>${escapeHtml(subnet.required_hosts)}</td>`,
          `<td class="mono">${escapeHtml(subnet.subnet)}</td>`,
          `<td class="mono">${escapeHtml(subnet.mask)}</td>`,
          `<td class="mono">${escapeHtml(subnet.first)} — ${escapeHtml(subnet.last)}</td>`,
          `<td>${escapeHtml(subnet.hosts_available)}</td>`,
        ])
      );
      byId('vlsmResult').classList.add('visible');
      byId('copyVlsmBtn').onclick = () =>
        copyToClipboard(
          data.subnets
            .map(
              (subnet, index) =>
                `#${index + 1} /${subnet.prefix} ${subnet.subnet} | ${subnet.first}—${subnet.last} | hosts: ${subnet.hosts_available}`
            )
            .join('\n')
        );
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
