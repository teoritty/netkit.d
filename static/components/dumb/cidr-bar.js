// Dumb component: network/host bit distribution.

import { byId } from '../../utils/dom.js';

export function renderCidrBar(prefix) {
  const value = Number.parseInt(prefix, 10);
  if (Number.isNaN(value) || value < 0 || value > 32) return;

  const track = byId('cidrTrack');
  const networkPart = byId('cidrNetwork');
  const hostPart = byId('cidrHost');
  const bar = byId('cidrBar');
  if (!networkPart || !hostPart || !bar) return;

  const hostBits = 32 - value;
  networkPart.style.width = `${(value / 32) * 100}%`;
  networkPart.textContent = value > 4 ? `/${value} net` : '';
  hostPart.textContent = hostBits > 4 ? `${hostBits} host` : '';
  bar.style.display = '';
}
