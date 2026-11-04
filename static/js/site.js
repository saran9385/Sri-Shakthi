/* Sri Shakthi — shared behaviour. No dependencies. */
(function () {
  "use strict";
  var doc = document;
  var root = doc.documentElement;
  root.classList.add("js");

  var $ = function (s, c) {
    return (c || doc).querySelector(s);
  };
  var $$ = function (s, c) {
    return Array.prototype.slice.call((c || doc).querySelectorAll(s));
  };

  /* ---------- Toast ---------- */
  var toastEl = $("#toast");
  var toastTimer;
  function toast(message) {
    if (!toastEl || !message) return;
    $("span", toastEl).textContent = message;
    toastEl.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toastEl.classList.remove("is-visible");
    }, 5000);
  }
  window.showToast = toast;
  if (toastEl && toastEl.dataset.flash) {
    setTimeout(function () {
      toast(toastEl.dataset.flash);
    }, 400);
  }

  /* ---------- Sticky nav state ---------- */
  var nav = $(".nav");
  var topBtn = $(".float .top");
  function onScroll() {
    var y = window.scrollY;
    if (nav) nav.classList.toggle("is-solid", y > 40);
    if (topBtn) topBtn.classList.toggle("is-visible", y > 700);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  if (topBtn) {
    topBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- Mobile menu ---------- */
  var menu = $("#mobileMenu");
  var burger = $("#hamburgerIcon");
  var closeIcon = $("#closeIcon");
  function setMenu(open) {
    if (!menu) return;
    menu.classList.toggle("is-open", open);
    menu.setAttribute("aria-hidden", open ? "false" : "true");
    if (burger) burger.setAttribute("aria-expanded", open ? "true" : "false");
    doc.body.style.overflow = open ? "hidden" : "";
    if (open && closeIcon) closeIcon.focus();
  }
  if (burger) burger.addEventListener("click", function () { setMenu(true); });
  if (closeIcon) closeIcon.addEventListener("click", function () { setMenu(false); if (burger) burger.focus(); });
  if (menu) {
    $$("a", menu).forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
  }

  /* ---------- Enquiry modal (posts to /enquiry_form) ---------- */
  var dlg = $("#popupForm");
  window.showForm = function () {
    if (!dlg) return;
    setMenu(false);
    if (typeof dlg.showModal === "function") dlg.showModal();
    else dlg.setAttribute("open", "");
  };
  window.hideForm = function () {
    if (!dlg) return;
    if (typeof dlg.close === "function") dlg.close();
    else dlg.removeAttribute("open");
  };
  $$("[data-open-enquiry]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      window.showForm();
    });
  });
  if (dlg) {
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg) window.hideForm();
    });
    var closeBtn = $(".modal__close", dlg);
    if (closeBtn) closeBtn.addEventListener("click", window.hideForm);
  }

  var form = $("#enquiryForm");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var note = $("#responseMessage");
      var btn = $("button[type=submit]", form);
      note.className = "form-note";
      note.textContent = "";
      btn.disabled = true;
      fetch("/enquiry_form", { method: "POST", body: new FormData(form) })
        .then(function (r) {
          return r.json().then(function (data) {
            return { status: r.status, body: data };
          });
        })
        .then(function (res) {
          if (res.status === 400) {
            note.textContent = res.body.error;
            note.classList.add("is-error");
          } else {
            form.reset();
            window.hideForm();
            toast(res.body.message || "Thank you. We will get back to you shortly.");
          }
        })
        .catch(function () {
          note.textContent = "Something went wrong. Please try again.";
          note.classList.add("is-error");
        })
        .then(function () {
          btn.disabled = false;
        });
    });
  }

  /* ---------- Contact page form (posts to /contactform) ---------- */
  var form2 = $("#enquiryForm2");
  if (form2) {
    form2.addEventListener("submit", function (event) {
      event.preventDefault();
      var note = $("#responseMessage2");
      var btn = $("button[type=submit]", form2);
      note.className = "form-note";
      btn.disabled = true;
      fetch("/contactform", { method: "POST", body: new FormData(form2) })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.error) {
            note.textContent = data.error;
            note.classList.add("is-error");
          } else {
            note.textContent = data.success;
            note.classList.add("is-ok");
            form2.reset();
          }
        })
        .catch(function () {
          note.textContent = "An error occurred. Please try again.";
          note.classList.add("is-error");
        })
        .then(function () {
          btn.disabled = false;
        });
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = $$("[data-reveal]");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    reveals.forEach(function (el, idx) {
      var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : idx;
      el.style.setProperty("--i", Math.min(sib, 6));
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Broken remote images fall back to a tinted tile ---------- */
  function markBroken(img) {
    var host = img.closest(".media");
    if (host) host.classList.add("is-broken");
  }
  $$(".media img").forEach(function (img) {
    if (img.complete && img.naturalWidth === 0 && img.currentSrc) markBroken(img);
    img.addEventListener("error", function () { markBroken(img); });
  });

  /* ---------- "Read more" on long place descriptions ---------- */
  $$(".place").forEach(function (card) {
    var p = $(".place__body p", card);
    var btn = $(".more", card);
    if (!p || !btn) return;
    function check() {
      if (card.classList.contains("is-open")) return;
      btn.hidden = p.scrollHeight <= p.clientHeight + 1;
    }
    check();
    window.addEventListener("resize", check);
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(check);
    btn.addEventListener("click", function () {
      var open = card.classList.toggle("is-open");
      btn.textContent = open ? "Show less" : "Read more";
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* ---------- Events strip arrows ---------- */
  var strip = $("#eventStrip");
  if (strip) {
    $$("[data-strip]").forEach(function (b) {
      b.addEventListener("click", function () {
        var step = strip.firstElementChild ? strip.firstElementChild.getBoundingClientRect().width + 20 : 300;
        strip.scrollBy({ left: Number(b.dataset.strip) * step, behavior: "smooth" });
      });
    });
  }

  /* ---------- Terms: highlight current section ---------- */
  var docLinks = $$(".doc__nav a");
  if (docLinks.length && "IntersectionObserver" in window) {
    var secs = docLinks.map(function (a) { return $(a.getAttribute("href")); }).filter(Boolean);
    var so = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            docLinks.forEach(function (a) {
              a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id);
            });
          }
        });
      },
      { rootMargin: "-30% 0px -60% 0px" }
    );
    secs.forEach(function (s) { so.observe(s); });
  }

  /* ---------- Gallery lightbox ---------- */
  var lb = $("#lightbox");
  if (lb) {
    var lbImg = $("#lightbox-img");
    var lbCount = $(".lightbox__count", lb);
    var items = $$("[data-lightbox]");
    var urls = items.map(function (el) { return el.dataset.lightbox; });
    var current = 0;
    var lastFocus = null;
    var show = function (i) {
      current = (i + urls.length) % urls.length;
      lbImg.src = urls[current];
      if (lbCount) lbCount.textContent = current + 1 + " / " + urls.length;
    };
    window.openLightbox = function (url) {
      var i = urls.indexOf(url);
      lastFocus = doc.activeElement;
      show(i < 0 ? 0 : i);
      lb.classList.add("is-open");
      doc.body.style.overflow = "hidden";
      $(".close", lb).focus();
    };
    window.closeLightbox = function () {
      lb.classList.remove("is-open");
      doc.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    };
    window.changeImage = function (d) { show(current + d); };
    items.forEach(function (el) {
      el.addEventListener("click", function () { window.openLightbox(el.dataset.lightbox); });
    });
    lb.addEventListener("click", function (e) {
      if (e.target === lb) window.closeLightbox();
    });
    doc.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "ArrowRight") window.changeImage(1);
      else if (e.key === "ArrowLeft") window.changeImage(-1);
      else if (e.key === "Escape") window.closeLightbox();
    });
  }

  /* ---------- Attractions filter ---------- */
  var filterBtns = $$("[data-filter]");
  if (filterBtns.length) {
    var cards = $$("#placeGrid .place");
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = btn.dataset.filter;
        filterBtns.forEach(function (b) { b.classList.toggle("is-active", b === btn); });
        cards.forEach(function (c) {
          c.hidden = !(f === "all" || c.dataset.cat === f);
        });
      });
    });
  }

  /* ---------- Contact map (Leaflet loaded on that page only) ---------- */
  var mapEl = $("#map");
  if (mapEl && window.L) {
    var pos = [8.102564045030881, 77.54931383233777];
    var map = L.map("map", { scrollWheelZoom: false }).setView(pos, 15);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);
    L.marker(pos).addTo(map);
  }
})();
