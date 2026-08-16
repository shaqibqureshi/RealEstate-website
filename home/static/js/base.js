document.addEventListener('DOMContentLoaded', () => {
  // Highlight the nav link matching the current page (set via <body data-page="...">)
  const page = document.body.dataset.page;
  if (page) {
    document.querySelectorAll(`[data-nav="${page}"]`).forEach((link) => {
      link.classList.add('nav-active');
    });
  }

  // Mobile menu toggle
  const toggle = document.getElementById('menu-toggle');
  const menu = document.getElementById('mobile-menu');
  const bar1 = document.getElementById('bar-1');
  const bar2 = document.getElementById('bar-2');
  const bar3 = document.getElementById('bar-3');

  if (toggle && menu) {
    let open = false;

    toggle.addEventListener('click', () => {
      open = !open;
      toggle.setAttribute('aria-expanded', String(open));
      menu.classList.toggle('hidden', !open);
      menu.classList.toggle('flex', open);
      bar1.style.transform = open ? 'translateY(6.5px) rotate(45deg)' : '';
      bar3.style.transform = open ? 'translateY(-6.5px) rotate(-45deg)' : '';
      bar2.style.opacity = open ? '0' : '1';
    });

    menu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        open = false;
        toggle.setAttribute('aria-expanded', 'false');
        menu.classList.add('hidden');
        menu.classList.remove('flex');
        bar1.style.transform = '';
        bar3.style.transform = '';
        bar2.style.opacity = '1';
      });
    });
  }

  // Footer year
  const yearEl = document.getElementById('copyright-year');
  if (yearEl) {
    yearEl.textContent = `© ${new Date().getFullYear()} Meridian Properties`;
  }
});