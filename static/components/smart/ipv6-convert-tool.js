// Smart component: IPv6 converter (full <-> compressed notation).

import { byId, setLoading } from '../../utils/dom.js';

export function mountIpv6ConvertTool({ calculationService, notify }) {
  const form = byId('ipv6-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    setLoading(button, true);
    try {
      const data = await calculationService.convertIpv6(byId('ipv6AddrInput').value.trim());
      byId('ipv6Full').textContent = data.full;
      byId('ipv6Compact').textContent = data.compact;
      byId('ipv6ConvertResult').classList.add('visible');
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
