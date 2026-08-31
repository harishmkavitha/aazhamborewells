/* =============================================================================
   Aazham Borewells — main.js  (V1)
   Progressive enhancement only. Every page stays readable and navigable with
   JavaScript disabled: menus fall back to hover/focus, links all resolve.
   ============================================================================= */
(function () {
  'use strict';

  var mq = window.matchMedia('(max-width: 900px)');

  /* ---- mobile nav open/close ---- */
  var toggle = document.querySelector('.site-nav__toggle');
  var list = document.querySelector('.nav-list');

  function closeMenu() {
    if (!list) return;
    list.classList.remove('is-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    document.querySelectorAll('.mega.is-open').forEach(function (m) {
      m.classList.remove('is-open');
      var b = m.previousElementSibling;
      if (b && b.classList.contains('nav-list__btn')) b.setAttribute('aria-expanded', 'false');
    });
  }

  if (toggle && list) {
    toggle.addEventListener('click', function () {
      var open = list.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      if (!open) closeMenu();
    });
  }

  /* ---- dropdown buttons (accordion on mobile, click-toggle on desktop) ---- */
  document.querySelectorAll('.nav-list__btn').forEach(function (btn) {
    var mega = btn.nextElementSibling;
    if (!mega || !mega.classList.contains('mega')) return;

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = mega.classList.contains('is-open');
      // close siblings
      document.querySelectorAll('.mega.is-open').forEach(function (m) {
        if (m !== mega) {
          m.classList.remove('is-open');
          var b = m.previousElementSibling;
          if (b) b.setAttribute('aria-expanded', 'false');
        }
      });
      mega.classList.toggle('is-open', !isOpen);
      btn.setAttribute('aria-expanded', String(!isOpen));
    });
  });

  /* ---- close on outside click / escape ---- */
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.site-nav')) {
      document.querySelectorAll('.mega.is-open').forEach(function (m) {
        m.classList.remove('is-open');
        var b = m.previousElementSibling;
        if (b) b.setAttribute('aria-expanded', 'false');
      });
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeMenu();
      if (toggle && list && !list.classList.contains('is-open')) toggle.focus();
    }
  });

  mq.addEventListener('change', closeMenu);

  /* ---- depth-ruler reveal (home hero) ---- */
  var ruler = document.querySelector('.ruler');
  if (ruler) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      ruler.classList.add('is-drawn');
    } else {
      window.requestAnimationFrame(function () {
        window.setTimeout(function () { ruler.classList.add('is-drawn'); }, 120);
      });
    }
  }

  /* ---- footer year ---- */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  /* ---- enquiry form ----
     Set the form's action to a form-service endpoint (Formspree, Basin, etc.)
     before launch. Until then this handler shows an inline success state and
     still directs people to phone / WhatsApp as the reliable fallback. */
  var form = document.querySelector('[data-ajax-form]');
  if (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var button = form.querySelector('[type="submit"]');
      var endpoint = form.getAttribute('action') || '';
      if (button) button.disabled = true;
      if (status) { status.removeAttribute('data-state'); status.textContent = 'Sending your enquiry…'; }

      if (!endpoint || endpoint.indexOf('example') !== -1) {
        // No live endpoint wired yet — acknowledge locally.
        window.setTimeout(function () {
          form.reset();
          if (status) { status.setAttribute('data-state', 'ok'); status.textContent = 'Thanks — your enquiry is noted. For a fast response, please also call or WhatsApp us.'; }
          if (button) button.disabled = false;
        }, 500);
        return;
      }

      fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) { if (!res.ok) throw new Error('bad'); form.reset();
          if (status) { status.setAttribute('data-state', 'ok'); status.textContent = 'Thanks — we have your enquiry and will call you back shortly.'; } })
        .catch(function () {
          if (status) { status.setAttribute('data-state', 'error'); status.textContent = 'That did not go through. Please call or WhatsApp us instead.'; } })
        .finally(function () { if (button) button.disabled = false; });
    });
  }
})();
