/* SHOMIT — 共通スクリプト */
(function () {
  "use strict";

  /* お問い合わせの送信先メールアドレス。空のままだとフォームは「準備中」表示になる */
  var CONTACT_EMAIL = "";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header scroll state */
  var header = document.getElementById("header");
  var onScroll = function () { if (header) header.classList.toggle("is-scrolled", window.scrollY > 40); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile nav */
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    };
    toggle.addEventListener("click", function () { setOpen(!nav.classList.contains("is-open")); });
    nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
  }

  /* Marquee loop */
  document.querySelectorAll(".marquee__track").forEach(function (track) { track.innerHTML = track.innerHTML + track.innerHTML; });

  /* Reveal on scroll */
  var reveals = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && reveals.length && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* Contact form: メールソフトを起動して送信（サーバー不要） */
  var form = document.getElementById("contactForm");
  var pending = document.getElementById("formPending");
  if (form) {
    if (!CONTACT_EMAIL) {
      form.hidden = true;
      if (pending) pending.hidden = false;
      return;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var f = new FormData(form);
      var subject = "【お問い合わせ】" + (f.get("category") || "") + " / " + (f.get("name") || "");
      var body = ["お名前: " + f.get("name"), "会社名: " + (f.get("company") || ""), "メール: " + f.get("email"), "電話: " + (f.get("tel") || ""), "種別: " + f.get("category"), "", f.get("message")].join("\n");
      window.location.href = "mailto:" + CONTACT_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      var msg = document.getElementById("formMsg");
      if (msg) { msg.classList.add("is-show"); }
    });
  }
})();
