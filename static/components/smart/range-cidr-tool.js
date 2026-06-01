// Smart component: IP range to CIDR blocks.

import { byId, setLoading, escapeHtml } from '../../utils/dom.js';
import { renderRows } from '../dumb/result-views.js';
import { t } from '../../i18n/i18n.js';

export function mountRangeCidrTool({ calculationService, notify }) {
  const form = byId('range-cidr-form');
  if (!form) return;

  // Preset chips fill both fields (data-fill-start / data-fill-end).
  form.querySelectorAll('[data-fill-start]').forEach((chip) => {
    chip.addEventListener('click', () => {
      byId('rangeStartIp').value = chip.dataset.fillStart;
      byId('rangeEndIp').value = chip.dataset.fillEnd;
    });
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    setLoading(button, true);
    try {
      const data = await calculationService.rangeToCidr(
        byId('rangeStartIp').value.trim(),
        byId('rangeEndIp').value.trim()
      );
      renderRows(
        byId('rangeCidrTableBody'),
        data.cidrs.map((item) => [
          `<td class="mono">${escapeHtml(item.cidr)}</td>`,
          `<td class="mono">${escapeHtml(item.network)}</td>`,
          `<td class="mono">${escapeHtml(item.broadcast)}</td>`,
          `<td>${escapeHtml(item.hosts)}</td>`,
        ])
      );
      byId('rangeCidrStats').textContent = `${t('Total IPs:')} ${data.total_ips} | ${t('Blocks:')} ${data.blocks}`;
      byId('rangeCidrResult').classList.add('visible');
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
