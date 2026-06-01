// Client-side tool (no backend): MTU and throughput calculation.

import { byId } from '../../utils/dom.js';

const ETHERNET_OVERHEAD = 38;

export function mountMtuTool() {
  const button = byId('calcMtuBtn');
  if (!button) return;

  button.addEventListener('click', calculate);
  ['tunnelType', 'physMtu', 'linkSpeed', 'packetSize'].forEach((id) =>
    byId(id)?.addEventListener('change', calculate)
  );
}

function calculate() {
  const overhead = Number.parseInt(byId('tunnelType').value, 10) || 0;
  const physMtu = Number.parseInt(byId('physMtu').value, 10) || 1500;
  const linkSpeed = Number.parseFloat(byId('linkSpeed').value) || 1000;
  const packetSize = Number.parseInt(byId('packetSize').value, 10) || 1500;

  const effectiveMtu = physMtu - overhead;
  const efficiency = ((effectiveMtu / physMtu) * 100).toFixed(1);
  const frameSize = Math.min(packetSize, effectiveMtu) + ETHERNET_OVERHEAD;
  const payloadRatio = Math.min(packetSize, effectiveMtu) / frameSize;
  const throughput = (payloadRatio * linkSpeed).toFixed(1);

  byId('mtuEffective').textContent = `${effectiveMtu} B`;
  byId('mtuOverhead').textContent = `${overhead} B`;
  byId('mtuEfficiency').textContent = `${efficiency}%`;
  byId('mtuThroughput').textContent = `${throughput} Mbit/s`;
  byId('mtuResultGrid').classList.add('visible');
}
