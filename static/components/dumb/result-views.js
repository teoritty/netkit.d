// Dumb result renderers: pure data-to-DOM transformation.
// No network calls or state — rendering from input data only.

import { byId, escapeHtml } from '../../utils/dom.js';
import { ipClassInfo, badgeClass } from '../../utils/ip-class-info.js';
import { t } from '../../i18n/i18n.js';

const COPY_ICON =
  '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';

export function renderIpClass(targetId, addressClass) {
  const element = byId(targetId);
  if (!element) return;
  element.innerHTML = `
    <div class="result-row">
      <span class="result-label">${escapeHtml(t('Address type'))}</span>
      <span class="badge ${badgeClass(addressClass)}">${escapeHtml(addressClass)}</span>
    </div>
    <div class="result-row">
      <span class="result-label">${escapeHtml(t('Description'))}</span>
      <span class="result-value">${escapeHtml(t(ipClassInfo(addressClass)))}</span>
    </div>`;
  element.classList.add('visible');
}

export function renderNetworkGroups(container, groups) {
  container.innerHTML = '';
  const entries = Object.entries(groups);
  if (!entries.length) {
    container.innerHTML = `<p class="text-muted" style="padding:8px 0">${escapeHtml(t('No results'))}</p>`;
    container.classList.add('visible');
    return;
  }
  entries.forEach(([network, addresses]) => {
    const group = document.createElement('div');
    group.className = 'network-group';
    const chips = addresses
      .map((address) => `<span class="network-ip-chip">${escapeHtml(address)}</span>`)
      .join('');
    group.innerHTML = `
      <div class="network-group-header">
        <span class="network-group-name">${escapeHtml(network)}</span>
        <span class="network-group-count">${addresses.length} address${addresses.length > 1 ? 'es' : ''}</span>
      </div>
      <div class="network-group-items">${chips}</div>`;
    container.appendChild(group);
  });
  container.classList.add('visible');
}

export function renderRows(tbody, rows) {
  tbody.innerHTML = rows
    .map((cells) => `<tr>${cells.map((cell) => cell).join('')}</tr>`)
    .join('');
}

export function renderDnsRecords(list, records) {
  list.innerHTML = records
    .map((record) => {
      const value =
        typeof record === 'object'
          ? `${record.preference ?? ''} ${record.exchange ?? JSON.stringify(record)}`.trim()
          : record;
      const safe = escapeHtml(value);
      return `<div class="dns-record-item">
        <span class="dns-record-value">${safe}</span>
        <button class="copy-btn" data-copy-text="${safe}" title="Copy">${COPY_ICON}</button>
      </div>`;
    })
    .join('');
}

export function renderWhois(container, fields) {
  container.innerHTML = fields
    .filter(([, value]) => value)
    .map(
      ([key, value]) => `<div class="whois-row">
        <span class="whois-key">${escapeHtml(key)}</span>
        <span class="whois-val">${escapeHtml(value)}</span>
      </div>`
    )
    .join('');
}

export function renderPortScanRows(tbody, results) {
  tbody.innerHTML = results
    .map(
      (row) => `<tr>
        <td class="mono">${escapeHtml(row.port)}</td>
        <td><span class="status-${escapeHtml(row.status)}">${escapeHtml(row.status)}</span></td>
        <td>${escapeHtml(row.service || '—')}</td>
      </tr>`
    )
    .join('');
}
