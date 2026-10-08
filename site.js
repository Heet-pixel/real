"use strict";
/* Swastiik Group — shared behaviour for every page (no dependencies) */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var svg = function (p) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + p + "</svg>"; };
  var ICONS = {
    "map-pin": svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>'),
    "arrow-right": svg('<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'),
    "check-circle": svg('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>'),
    "shield-check": svg('<path d="M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3Z"/><path d="m9 12 2 2 4-4"/>'),
    car: svg('<path d="M19 17h2v-4l-2-5H5L3 13v4h2"/><circle cx="7.5" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/><path d="M5 17h10"/>'),
    video: svg('<path d="m22 8-6 4 6 4V8Z"/><rect x="2" y="6" width="14" height="12" rx="2"/>'),
    ruler: svg('<path d="m16 3 5 5-12 12-5-5Z"/><path d="m14.5 6.5 1.5 1.5"/><path d="m11.5 9.5 1.5 1.5"/><path d="m8.5 12.5 1.5 1.5"/>'),
    users: svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
    x: svg('<path d="M18 6 6 18"/><path d="m6 6 12 12"/>'),
    phone: svg('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/>'),
    mail: svg('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'),
    "chev-l": svg('<path d="m15 18-6-6 6-6"/>'),
    "chev-r": svg('<path d="m9 18 6-6-6-6"/>')
  };
  function icons(root) {
    $$("[data-lucide]", root).forEach(function (el) {
      var n = el.getAttribute("data-lucide");
      if (ICONS[n]) { el.innerHTML = ICONS[n]; el.classList.add("icon-svg"); }
    });
  }
  icons();

  /* Splash (home only) */
  var splash = $("#splashScreen");
  if (splash) {
    document.body.classList.add("no-scroll");
    var hide = function () {
      splash.classList.add("splash-hide");
      setTimeout(function () { splash.style.display = "none"; document.body.classList.remove("no-scroll"); }, 700);
    };
    var minWait = new Promise(function (r) { setTimeout(r, 1200); });
    var loaded = new Promise(function (r) { document.readyState === "complete" ? r() : window.addEventListener("load", r); });
    Promise.all([minWait, loaded]).then(hide);
    setTimeout(hide, 4000);
  }

  /* Navbar */
  var nav = $("#navbar"), burger = $("#hamburger"), menu = $("#mobileMenu");
  var onScroll = function () { nav.classList.toggle("scrolled", window.scrollY > 40); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  burger.addEventListener("click", function () {
    var open = menu.classList.toggle("open");
    burger.classList.toggle("active", open);
    burger.setAttribute("aria-expanded", open);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { menu.classList.remove("open"); burger.classList.remove("active"); burger.setAttribute("aria-expanded", "false"); }
  });
  document.addEventListener("click", function (e) {
    if (menu.classList.contains("open") && !menu.contains(e.target) && !burger.contains(e.target)) {
      menu.classList.remove("open"); burger.classList.remove("active");
    }
  });

  /* Scroll reveal */
  if ("IntersectionObserver" in window) {
    var ro = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("revealed"); ro.unobserve(e.target); } });
    }, { threshold: 0.1 });
    $$(".reveal").forEach(function (el) { ro.observe(el); });
    /* Counters */
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, t = parseInt(el.dataset.count, 10), s = performance.now();
        (function tick(n) {
          var p = Math.min((n - s) / 1400, 1);
          el.textContent = Math.round(t * (1 - Math.pow(1 - p, 3))).toLocaleString("en-IN");
          if (p < 1) requestAnimationFrame(tick);
        })(s);
        co.unobserve(el);
      });
    }, { threshold: 0.5 });
    $$(".stat-number[data-count]").forEach(function (el) { co.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("revealed"); });
    $$(".stat-number[data-count]").forEach(function (el) { el.textContent = el.dataset.count; });
  }

  /* Hero slider */
  var slides = $$(".slide");
  if (slides.length > 1) {
    var idx = 0, timer, dotsBox = $(".hero-dots");
    slides.forEach(function (_, i) {
      var b = document.createElement("button");
      b.setAttribute("aria-label", "Go to slide " + (i + 1));
      b.addEventListener("click", function () { go(i, true); });
      dotsBox.appendChild(b);
    });
    var dots = $$("button", dotsBox);
    function go(i, manual) {
      idx = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle("active", k === idx); });
      dots.forEach(function (d, k) { d.classList.toggle("active", k === idx); });
      if (manual) start();
    }
    function start() { clearInterval(timer); timer = setInterval(function () { go(idx + 1); }, 6500); }
    $(".hero-arrow.prev").addEventListener("click", function () { go(idx - 1, true); });
    $(".hero-arrow.next").addEventListener("click", function () { go(idx + 1, true); });
    var tx = null, hero = $(".hero");
    hero.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener("touchend", function (e) {
      if (tx === null) return;
      var d = e.changedTouches[0].clientX - tx;
      if (Math.abs(d) > 50) go(idx + (d < 0 ? 1 : -1), true);
      tx = null;
    });
    go(0); start();
  }

  /* Filters (projects + photos pages) */
  $$("[data-filter-group]").forEach(function (group) {
    var target = $(group.dataset.filterGroup), items = $$("[data-tags]", target);
    var note = $(".empty-note");
    group.addEventListener("click", function (e) {
      var b = e.target.closest(".chip"); if (!b) return;
      $$(".chip", group).forEach(function (c) { c.classList.toggle("active", c === b); });
      var f = b.dataset.filter, shown = 0;
      items.forEach(function (it) {
        var ok = f === "all" || it.dataset.tags.split(" ").indexOf(f) > -1;
        it.classList.toggle("is-hidden", !ok); if (ok) shown++;
      });
      if (note) note.classList.toggle("is-hidden", shown > 0);
      lbRefresh();
    });
  });

  /* Lightbox */
  var lb, lbImg, lbCap, list = [], cur = 0;
  function lbRefresh() { list = $$("[data-lb]").filter(function (a) { return !a.classList.contains("is-hidden"); }); }
  function lbShow(i) {
    cur = (i + list.length) % list.length;
    lbImg.src = list[cur].getAttribute("href");
    lbImg.alt = list[cur].dataset.cap || "";
    lbCap.textContent = (list[cur].dataset.cap || "") + "  ·  " + (cur + 1) + " / " + list.length;
  }
  function lbClose() { lb.classList.remove("open"); document.body.classList.remove("no-scroll"); }
  if ($("[data-lb]")) {
    lb = document.createElement("div");
    lb.className = "lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true");
    lb.innerHTML = '<button class="lb-x" aria-label="Close"><i data-lucide="x"></i></button><button class="lb-p" aria-label="Previous"><i data-lucide="chev-l"></i></button><img alt=""><button class="lb-n" aria-label="Next"><i data-lucide="chev-r"></i></button><div class="lb-cap"></div>';
    document.body.appendChild(lb); icons(lb);
    lbImg = $("img", lb); lbCap = $(".lb-cap", lb);
    lbRefresh();
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lb]");
      if (a) { e.preventDefault(); lbRefresh(); lbShow(list.indexOf(a)); lb.classList.add("open"); document.body.classList.add("no-scroll"); }
    });
    $(".lb-x", lb).addEventListener("click", lbClose);
    $(".lb-p", lb).addEventListener("click", function () { lbShow(cur - 1); });
    $(".lb-n", lb).addEventListener("click", function () { lbShow(cur + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) lbClose(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") lbClose();
      if (e.key === "ArrowLeft") lbShow(cur - 1);
      if (e.key === "ArrowRight") lbShow(cur + 1);
    });
    var sx = null;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var d = e.changedTouches[0].clientX - sx;
      if (Math.abs(d) > 50) lbShow(cur + (d < 0 ? 1 : -1));
      sx = null;
    });
  }

  /* Enquiry form -> opens the visitor's mail app (static site, no server needed) */
  var form = $("#enquiryForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = new FormData(form);
      var body = "Name: " + f.get("name") + "\nPhone: " + f.get("phone") + "\nProject: " + f.get("project") + "\n\n" + f.get("message");
      window.location.href = "mailto:" + form.dataset.to + "?subject=" + encodeURIComponent("Enquiry: " + f.get("project")) + "&body=" + encodeURIComponent(body);
    });
    var q = new URLSearchParams(location.search).get("project");
    if (q && form.elements.project) form.elements.project.value = q;
  }
})();
