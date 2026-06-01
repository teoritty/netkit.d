// Smart component: port information.

import { byId, setLoading } from '../../utils/dom.js';
import { t } from '../../i18n/i18n.js';

export function mountPortInfoTool({ calculationService, notify }) {
  const form = byId('portForm');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const port = byId('port').value;
    setLoading(button, true);
    try {
      const data = await calculationService.lookupPort(port);
      byId('portResultNum').textContent = `${t('Port')} ${port}`;
      const service = byId('portResultSvc');
      if (data.service) {
        service.textContent = data.service;
        service.className = 'port-result-service';
      } else {
        service.textContent = t('No information about this port');
        service.className = 'port-result-empty';
      }
      byId('portResultCard').classList.add('visible');
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
