// Smart component: DNS lookup.

import { byId, setLoading } from '../../utils/dom.js';
import { renderDnsRecords } from '../dumb/result-views.js';
import { t } from '../../i18n/i18n.js';

export function mountDnsTool({ diagnosticsService, notify }) {
  const form = byId('dns-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const hostname = byId('dnsHostname').value.trim();
    const recordType = form.querySelector('input[name="dnsType"]:checked')?.value || 'A';

    setLoading(button, true);
    try {
      const data = await diagnosticsService.dnsLookup(hostname, recordType);
      byId('dnsResultType').textContent = data.type;
      byId('dnsResultTtl').textContent = data.ttl ? `TTL: ${data.ttl}s` : '';
      byId('dnsResultCount').textContent = `${data.records.length} ${t('record(s)')}`;
      renderDnsRecords(byId('dnsRecordList'), data.records);
      byId('dnsResult').classList.add('visible');
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
