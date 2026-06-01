// Smart component: ping.

import { byId, setLoading } from '../../utils/dom.js';
import { t } from '../../i18n/i18n.js';

export function mountPingTool({ diagnosticsService, notify }) {
  const form = byId('ping-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const host = byId('pingHost').value.trim();
    const count = Number.parseInt(byId('pingCount').value, 10);
    const output = byId('pingOutput');

    setLoading(button, true);
    output.textContent = `${t('Pinging')} ${host}...`;
    output.classList.add('visible');
    try {
      const data = await diagnosticsService.ping(host, count);
      output.textContent = data.output;
      if (data.success) {
        notify(
          data.avg_ms ? `${t('Average RTT:')} ${data.avg_ms} ${t('ms')}` : t('Host is reachable'),
          'success'
        );
      } else {
        notify(t('Host is unreachable'), 'error');
      }
    } catch (error) {
      output.classList.remove('visible');
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
