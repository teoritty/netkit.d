// Smart component: port scanner.

import { byId, setLoading } from '../../utils/dom.js';
import { renderPortScanRows } from '../dumb/result-views.js';
import { t } from '../../i18n/i18n.js';

export function mountPortScanTool({ diagnosticsService, notify }) {
  const form = byId('port-scan-form');
  if (!form) return;

  // Preset chips set the port list (data-fill="scanPorts" + data-value).
  form.querySelectorAll('.chip[data-value]').forEach((chip) => {
    chip.addEventListener('click', () => {
      byId('scanPorts').value = chip.dataset.value;
    });
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const host = byId('scanHost').value.trim();
    const ports = byId('scanPorts').value.trim();

    setLoading(button, true);
    byId('portScanTable').classList.remove('visible');
    byId('portScanSummary').style.display = 'none';
    try {
      const data = await diagnosticsService.portScan(host, ports);
      renderPortScanRows(byId('portScanBody'), data.results);
      byId('scanOpenCount').textContent = data.open;
      byId('scanClosedCount').textContent = data.closed;
      byId('scanFilteredCount').textContent = data.filtered;
      byId('portScanSummary').style.display = 'flex';
      byId('portScanTable').classList.add('visible');
      notify(`${t('Scan complete:')} ${data.open} ${t('open ports')}`, data.open > 0 ? 'success' : 'info');
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
