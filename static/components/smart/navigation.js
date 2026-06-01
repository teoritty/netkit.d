// Smart component: navigation — mobile sidebar, active-section highlight, chips.

import { byId } from '../../utils/dom.js';

export function mountNavigation() {
  initSidebar();
  initNavHighlight();
  initFillChips();
}

function initSidebar() {
  const sidebar = byId('sidebar');
  const backdrop = byId('sidebarBackdrop');
  const hamburger = byId('hamburgerBtn');
  if (!sidebar) return;

  const open = () => {
    sidebar.classList.add('open');
    backdrop.classList.add('visible');
    document.body.style.overflow = 'hidden';
  };
  const close = () => {
    sidebar.classList.remove('open');
    backdrop.classList.remove('visible');
    document.body.style.overflow = '';
  };

  hamburger?.addEventListener('click', open);
  backdrop?.addEventListener('click', close);
  sidebar.querySelectorAll('.nav-item').forEach((item) =>
    item.addEventListener('click', () => {
      if (window.innerWidth <= 768) close();
    })
  );
}

function initNavHighlight() {
  const sections = document.querySelectorAll('.section[id]');
  const navItems = document.querySelectorAll('.nav-item[data-section]');
  if (!sections.length || !navItems.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navItems.forEach((item) =>
          item.classList.toggle('active', item.dataset.section === entry.target.id)
        );
      });
    },
    { rootMargin: '-20% 0px -70% 0px', threshold: 0 }
  );
  sections.forEach((section) => observer.observe(section));

  navItems.forEach((item) =>
    item.addEventListener('click', () => {
      byId(item.dataset.section)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    })
  );
}

// Quick-fill chips: data-fill names the field id, data-value is the value
// (otherwise the chip's text is used).
function initFillChips() {
  document.querySelectorAll('.chip[data-fill]').forEach((chip) => {
    chip.addEventListener('click', () => {
      const input = byId(chip.dataset.fill);
      if (!input) return;
      input.value = chip.dataset.value ?? chip.textContent.trim();
      input.dispatchEvent(new Event('input'));
      input.focus();
    });
  });
}
