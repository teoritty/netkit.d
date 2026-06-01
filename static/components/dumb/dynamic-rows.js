// Dumb dynamic-rows widget: add and remove via delegation.
// Removal is handled by a single delegated listener (no inline onclick).

const REMOVE_ICON =
  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6 6 18M6 6l12 12"/></svg>';

export function removeIconMarkup() {
  return REMOVE_ICON;
}

export function appendRow(container, html) {
  if (!container) return;
  const wrapper = document.createElement('div');
  wrapper.innerHTML = html.trim();
  container.appendChild(wrapper.firstElementChild);
}

// One delegated handler removes the nearest row of any type.
export function initRowRemoval(root, rowSelector) {
  root.addEventListener('click', (event) => {
    const button = event.target.closest('.remove-btn');
    if (button) button.closest(rowSelector)?.remove();
  });
}
