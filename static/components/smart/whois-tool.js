// Smart component: Whois / ASN.

import { byId, setLoading } from '../../utils/dom.js';
import { renderWhois } from '../dumb/result-views.js';
import { copyToClipboard } from '../dumb/clipboard.js';
import { t } from '../../i18n/i18n.js';

export function mountWhoisTool({ diagnosticsService, notify }) {
  const form = byId('whois-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    setLoading(button, true);
    try {
      const data = await diagnosticsService.whois(byId('whoisIp').value.trim());
      const fields = [
        [t('IP address'), data.ip],
        ['ASN', data.asn ? `AS${data.asn}` : null],
        ['ASN CIDR', data.asn_cidr],
        [t('Country'), data.asn_country],
        [t('Description'), data.asn_description],
        [t('Organization'), data.org],
        ['Abuse Email', data.abuse_emails?.join(', ') || null],
      ];
      renderWhois(byId('whoisBody'), fields);
      byId('whoisResult').classList.add('visible');
      byId('copyWhoisBtn').onclick = () =>
        copyToClipboard(
          fields.filter(([, value]) => value).map(([key, value]) => `${key}: ${value}`).join('\n')
        );
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
