// Dumb notification component: pure toast rendering into a container.

const ICONS = {
  success: '<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>',
  error: '<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>',
  info: '<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
};

let container = null;

export function mountToasts(element) {
  container = element;
}

export function showToast(message, type = 'info', duration = 3000) {
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.setAttribute('role', 'status');
  toast.innerHTML = `${ICONS[type] || ICONS.info}<span></span>`;
  toast.querySelector('span').textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('exiting');
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
  }, duration);
}
