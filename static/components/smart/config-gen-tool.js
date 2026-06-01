// Client-side tool (no backend): Nginx/HAProxy/Traefik config generator.

import { byId } from '../../utils/dom.js';
import { copyToClipboard } from '../dumb/clipboard.js';
import { t } from '../../i18n/i18n.js';

const LABELS = {
  nginx: 'Nginx configuration',
  haproxy: 'HAProxy configuration',
  traefik: 'Traefik configuration',
};

export function mountConfigGenTool({ notify }) {
  const button = byId('generateCfgBtn');
  if (!button) return;

  button.addEventListener('click', () => {
    const type = document.querySelector('input[name="cfgType"]:checked')?.value || 'nginx';
    const name = byId('cfgName').value.trim() || 'backend';
    const balance = byId('cfgBalance').value;
    const servers = byId('cfgServers').value.split('\n').map((line) => line.trim()).filter(Boolean);

    if (!servers.length) {
      notify(t('Add at least one server'), 'error');
      return;
    }

    const config = buildConfig(type, name, balance, servers);
    byId('configText').value = config;
    byId('configOutputLabel').textContent = t(LABELS[type]);
    byId('configOutput').classList.add('visible');
    byId('copyCfgBtn').onclick = () => copyToClipboard(config);
  });
}

function buildConfig(type, name, balance, servers) {
  if (type === 'nginx') return buildNginx(name, balance, servers);
  if (type === 'haproxy') return buildHaproxy(name, servers);
  return buildTraefik(name, servers);
}

function buildNginx(name, balance, servers) {
  const lines = servers.map((server) => `    server ${server};`).join('\n');
  const balanceLine = balance ? `    ${balance}\n` : '';
  return `upstream ${name} {\n${balanceLine}${lines}\n\n    keepalive 32;\n}\n\nserver {\n    listen 80;\n\n    location / {\n        proxy_pass http://${name};\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n        proxy_connect_timeout 5s;\n        proxy_read_timeout 60s;\n    }\n}`;
}

function buildHaproxy(name, servers) {
  const lines = servers
    .map((server, index) => `    server app${index + 1} ${server} check inter 2000 rise 2 fall 3`)
    .join('\n');
  return `backend ${name}\n    balance roundrobin\n    option httpchk GET /health\n    http-check expect status 200\n${lines}\n\nfrontend http-in\n    bind *:80\n    default_backend ${name}`;
}

function buildTraefik(name, servers) {
  const lines = servers.map((server) => `          - url: "http://${server}"`).join('\n');
  return `http:\n  services:\n    ${name}:\n      loadBalancer:\n        servers:\n${lines}\n        healthCheck:\n          path: /health\n          interval: "10s"\n          timeout: "3s"`;
}
