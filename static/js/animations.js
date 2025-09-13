// Site-wide animations: navbar scroll shadow, reveal-on-scroll, hero float class toggle
(function(){
  const doc = document;
  const root = doc.documentElement;

  // Navbar shadow on scroll
  function updateNavShadow(){
    const nav = doc.querySelector('.navbar-modern');
    if(!nav) return;
    const scrolled = window.scrollY > 50;
    nav.classList.toggle('scrolled', scrolled);
  }

  // Reveal on scroll using IntersectionObserver
  function initReveal(){
    if (!('IntersectionObserver' in window)){
      // Fallback: make visible
      doc.querySelectorAll('.reveal').forEach(el=> el.classList.add('reveal-visible'));
      return;
    }
    const prefersReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const obs = new IntersectionObserver((entries)=>{
      entries.forEach(entry=>{
        if(entry.isIntersecting){
          entry.target.classList.add('reveal-visible');
          if (!prefersReduce) entry.target.style.transitionDelay = (entry.target.dataset.delay || '0')+'ms';
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    doc.querySelectorAll('.reveal').forEach(el=> obs.observe(el));
  }

  // Add float animation to hero illustration if present
  function initHeroFloat(){
    const img = doc.querySelector('.hero-illustration-img');
    if(img) img.classList.add('float-anim');
  }

  // Loading state management
  function initLoadingStates() {
    // Add loading states to forms
    const forms = doc.querySelectorAll('form');
    forms.forEach(form => {
      form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
          submitBtn.classList.add('loading');
          submitBtn.disabled = true;
        }
      });
    });

    // Add loading states to links that might take time
    const slowLinks = doc.querySelectorAll('a[href*="quiz"], a[href*="college-finder"]');
    slowLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        if (!this.classList.contains('loading')) {
          this.classList.add('loading');
          // Remove loading state after navigation
          setTimeout(() => {
            this.classList.remove('loading');
          }, 2000);
        }
      });
    });
  }

  // Smooth scroll for anchor links
  function initSmoothScroll() {
    const anchorLinks = doc.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const target = doc.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }

  // Keyboard navigation improvements
  function initKeyboardNavigation() {
    // Skip link functionality
    const skipLink = doc.querySelector('.skip-link');
    if (skipLink) {
      skipLink.addEventListener('click', function(e) {
        e.preventDefault();
        const target = doc.querySelector(this.getAttribute('href'));
        if (target) {
          target.focus();
          target.scrollIntoView();
        }
      });
    }

    // Escape key to close modals/dropdowns
    doc.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        // Close any open dropdowns
        const openDropdowns = doc.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(dropdown => {
          dropdown.classList.remove('show');
        });
      }
    });
  }

  // Performance optimization: Debounce scroll events
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Run after DOM ready
  document.addEventListener('DOMContentLoaded', function(){
    updateNavShadow();
    initReveal();
    initHeroFloat();
    initLoadingStates();
    initSmoothScroll();
    initKeyboardNavigation();
  });
  
  // Debounced scroll handler for better performance
  const debouncedNavUpdate = debounce(updateNavShadow, 10);
  window.addEventListener('scroll', debouncedNavUpdate, { passive: true });
})();
