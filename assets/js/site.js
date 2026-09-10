// Sprocket Player site — tiny, dependency-free helpers.
(function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') links.classList.remove('open');
    });
  }

  // Screenshot slots: if the image file is missing, show the labelled placeholder instead.
  document.querySelectorAll('.device .shot-img').forEach(function (img) {
    var mark = function () { img.closest('.device').classList.add('missing'); };
    if (img.complete && img.naturalWidth === 0) mark();
    img.addEventListener('error', mark);
  });

  // Reveal-on-scroll
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // Language switcher: remember the choice so the root redirector honours it, then jump to the
  // same page under the chosen language.
  var sel = document.getElementById('lang-select');
  if (sel) {
    sel.addEventListener('change', function () {
      var lang = sel.value;
      try { localStorage.setItem('sp-lang', lang); } catch (e) {}
      var page = sel.getAttribute('data-page') || '';
      window.location.href = '/' + lang + '/' + page + window.location.hash;
    });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
