// Smart component: traceroute.

import { byId, setLoading } from '../../utils/dom.js';
import { t } from '../../i18n/i18n.js';

export function mountTracerouteTool({ diagnosticsService, notify }) {
  const form = byId('traceroute-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const host = byId('tracerouteHost').value.trim();
    const maxHops = Number.parseInt(byId('tracerouteHops').value, 10);
    const output = byId('tracerouteOutput');

    setLoading(button, true);
    output.textContent = `${t('Tracing route to')} ${host}...`;
    output.classList.add('visible');
    try {
      const data = await diagnosticsService.traceroute(host, maxHops);
      output.textContent = data.output;
    } catch (error) {
      output.classList.remove('visible');
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
