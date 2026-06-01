// Thin fetch wrapper: JSON in/out and error normalization.
// On error the server returns {"error": "..."} — we turn that into an ApiError.

import { t } from '../i18n/i18n.js';

export class ApiError extends Error {}

async function parse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new ApiError(data.error || t('Failed to connect to the server'));
  }
  return data;
}

export function createApiClient() {
  async function get(url) {
    const response = await fetch(url);
    return parse(response);
  }

  async function postJson(url, body) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return parse(response);
  }

  return { get, postJson };
}
