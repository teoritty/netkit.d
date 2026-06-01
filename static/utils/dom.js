// Pure DOM helpers with no business-logic side effects.

export function setLoading(button, isLoading) {
  if (!button) return;
  button.classList.toggle('loading', isLoading);
  button.disabled = isLoading;
}

export function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = String(value ?? '');
  return div.innerHTML;
}

export function byId(id) {
  return document.getElementById(id);
}
