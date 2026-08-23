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

  // Hero photo slider
  const sliderSection = document.getElementById('hero-slider');
  if (sliderSection) {
    const slides = Array.from(sliderSection.querySelectorAll('[data-slide]'));
    const dotsWrap = document.getElementById('slider-dots');
    const prevBtn = document.getElementById('slider-prev');
    const nextBtn = document.getElementById('slider-next');
    let current = 0;
    let timer = null;

    // Build dots
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'slider-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
      dot.addEventListener('click', () => goTo(i));
      dotsWrap.appendChild(dot);
    });
    const dots = Array.from(dotsWrap.children);

    function goTo(index) {
      slides[current].classList.remove('opacity-100');
      slides[current].classList.add('opacity-0');
      dots[current].classList.remove('active');

      current = (index + slides.length) % slides.length;

      slides[current].classList.remove('opacity-0');
      slides[current].classList.add('opacity-100');
      dots[current].classList.add('active');
    }

    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    function startAutoplay() {
      timer = setInterval(next, 5000);
    }
    function stopAutoplay() {
      clearInterval(timer);
    }

    nextBtn?.addEventListener('click', () => { next(); stopAutoplay(); startAutoplay(); });
    prevBtn?.addEventListener('click', () => { prev(); stopAutoplay(); startAutoplay(); });
    sliderSection.addEventListener('mouseenter', stopAutoplay);
    sliderSection.addEventListener('mouseleave', startAutoplay);

    startAutoplay();
  }

  // Appointment form (contact page)
  const appointmentForm = document.getElementById('appointment-form');
  if (appointmentForm) {
    const dateInput = document.getElementById('date');
    if (dateInput) {
      dateInput.min = new Date().toISOString().split('T')[0];
    }

    const successMsg = document.getElementById('form-success');

    appointmentForm.addEventListener('submit', (e) => {
      e.preventDefault();

      if (!appointmentForm.checkValidity()) {
        appointmentForm.reportValidity();
        return;
      }

      // No backend wired up yet — swap this block out for a real fetch()
      // call to your booking endpoint when one exists.
      successMsg?.classList.remove('hidden');
      appointmentForm.reset();
      successMsg?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  }

  // FAQ accordion (contact page)
  document.querySelectorAll('.faq-item').forEach((item) => {
    const question = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');
    const icon = item.querySelector('.faq-icon');

    question?.addEventListener('click', () => {
      const isOpen = !answer.classList.contains('hidden');

      // Close any other open items (accordion behaviour)
      document.querySelectorAll('.faq-answer').forEach((a) => a.classList.add('hidden'));
      document.querySelectorAll('.faq-icon').forEach((i) => (i.textContent = '+'));

      if (!isOpen) {
        answer.classList.remove('hidden');
        icon.textContent = '−';
      }
    });
  });
});