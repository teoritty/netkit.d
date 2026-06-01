// Smart component: subnet calculator. Orchestrates input, service, and rendering.

import { byId, setLoading } from '../../utils/dom.js';
import { renderCidrBar } from '../dumb/cidr-bar.js';
import { copyToClipboard } from '../dumb/clipboard.js';
import { t } from '../../i18n/i18n.js';

export function mountSubnetTool({ calculationService, notify }) {
  const form = byId('network-info-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('[data-submit-btn]');
    const ip = byId('subnetIpInput').value.trim();
    const prefix = Number.parseInt(byId('subnetMaskSelect').value, 10);

    setLoading(button, true);
    try {
      const result = await calculationService.calculateSubnet(ip, String(prefix));
      const wildcard = wildcardMask(prefix);
      fillResult(result, wildcard);
      renderCidrBar(prefix);
      bindCopyAll(result, wildcard);
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}

function fillResult(result, wildcard) {
  byId('res-hosts').textContent = result.hosts_count;
  byId('res-network').textContent = result.network_address;
  byId('res-first').textContent = result.first_address;
  byId('res-last').textContent = result.last_address;
  byId('res-broadcast').textContent = result.broadcast_address;
  byId('res-wildcard').textContent = wildcard;
  byId('subnetResult').classList.add('visible');
}

function bindCopyAll(result, wildcard) {
  byId('copyAllSubnet').onclick = () =>
    copyToClipboard(
      [
        `${t('Network:')} ${result.network_address}`,
        `${t('First:')} ${result.first_address}`,
        `${t('Last:')} ${result.last_address}`,
        `Broadcast: ${result.broadcast_address}`,
        `${t('Hosts:')} ${result.hosts_count}`,
        `Wildcard: ${wildcard}`,
      ].join('\n')
    );
}

function wildcardMask(prefix) {
  return [0, 1, 2, 3]
    .map((octet) => {
      const maskByte =
        prefix >= (octet + 1) * 8
          ? 255
          : prefix >= octet * 8
            ? 256 - (1 << (8 - (prefix - octet * 8)))
            : 0;
      return 255 - maskByte;
    })
    .join('.');
}
