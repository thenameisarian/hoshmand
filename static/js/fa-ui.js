/* Hooshmand — Persian UI translation layer (starter).
 *
 * Translates a CURATED set of high-visibility chrome strings to Persian by
 * EXACT text match, so it can never corrupt unrelated/dynamic content (an
 * unknown string is simply left untouched). Extend FA below as needed.
 *
 * This is a pragmatic starter authored without a live browser — verify
 * visually and grow the dictionary. To disable: remove the <script> tag for
 * this file (and dir="rtl" on <html>) in static/index.html.
 */
(function () {
  "use strict";

  // English -> Persian (Dari-friendly) for stable chrome strings.
  var FA = {
    "New Chat": "گفت‌وگوی جدید",
    "Settings": "تنظیمات",
    "Send": "ارسال",
    "Save": "ذخیره",
    "Saved": "ذخیره شد",
    "Rename": "تغییر نام",
    "Copy Chat": "کپی گفت‌وگو",
    "Save to Documents": "ذخیره در اسناد",
    "Delete": "حذف",
    "Cancel": "لغو",
    "Close": "بستن",
    "Compare": "مقایسه",
    "Search": "جستجو",
    "Preview": "پیش‌نمایش",
    "Documents": "اسناد",
    "Gallery": "گالری",
    "Notes": "یادداشت‌ها",
    "Tasks": "وظایف",
    "Email": "ایمیل",
    "Memory": "حافظه",
    "Calendar": "تقویم",
    "Library": "کتابخانه",
    "Sessions": "نشست‌ها",
    "Skills": "مهارت‌ها",
    // Settings tabs
    "Services": "سرویس‌ها",
    "AI": "هوش مصنوعی",
    "Integrations": "یکپارچه‌سازی‌ها",
    "Reminders": "یادآوری‌ها",
    "Appearance": "ظاهر",
    "Shortcuts": "میان‌برها",
    "Account": "حساب کاربری",
    "Tools": "ابزارها",
    "Users": "کاربران",
    "System": "سیستم",
    "Dialect": "لهجه",
    "Provider": "ارائه‌دهنده",
    "Model": "مدل",
    "Voice": "صدا",
    "Speed": "سرعت",
    "Brain": "مغز",
    "Cookbook": "کوک‌بوک",
    "Deep Research": "تحقیق عمیق",
    "Theme": "قالب",
    "new": "جدید",
    "Open Admin to add endpoints": "برای افزودن اندپوینت، بخش مدیریت را باز کنید",
    "Add Models": "افزودن مدل‌ها",
    "AI Defaults": "پیش‌فرض‌های هوش مصنوعی",
    "Agent Tools": "ابزارهای ایجنت"
  };

  function translateText(root) {
    // Walk text nodes; replace only when the trimmed value EXACTLY matches a key.
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var node;
    var pending = [];
    while ((node = walker.nextNode())) {
      var raw = node.nodeValue;
      if (!raw) continue;
      var t = raw.trim();
      if (t && Object.prototype.hasOwnProperty.call(FA, t)) {
        pending.push(node);
      }
    }
    pending.forEach(function (n) {
      var t = n.nodeValue.trim();
      n.nodeValue = n.nodeValue.replace(t, FA[t]);
    });
  }

  function translateAttrs(root) {
    ["placeholder", "title", "aria-label"].forEach(function (attr) {
      root.querySelectorAll("[" + attr + "]").forEach(function (el) {
        var v = (el.getAttribute(attr) || "").trim();
        if (v && Object.prototype.hasOwnProperty.call(FA, v)) {
          el.setAttribute(attr, FA[v]);
        }
      });
    });
  }

  // Direction is user-switchable and remembered. Default RTL (Persian-first);
  // flip to LTR anytime via the toggle if RTL layout quirks bother you.
  function applyDir() {
    var d = localStorage.getItem("hooshmand_dir") || "rtl";
    document.documentElement.setAttribute("dir", d);
    document.documentElement.setAttribute("lang", "fa");
    return d;
  }

  function addDirToggle() {
    if (document.getElementById("hooshmand-dir-toggle")) return;
    var cur = localStorage.getItem("hooshmand_dir") || "rtl";
    var btn = document.createElement("button");
    btn.id = "hooshmand-dir-toggle";
    btn.type = "button";
    btn.title = "Switch interface direction (RTL/LTR)";
    btn.textContent = cur === "rtl" ? "⇄ LTR" : "⇄ RTL";
    btn.style.cssText =
      "position:fixed;bottom:10px;" + (cur === "rtl" ? "left:10px;" : "right:10px;") +
      "z-index:9999;font-size:11px;padding:4px 8px;border-radius:6px;" +
      "border:1px solid var(--border,#888);background:var(--panel,#222);" +
      "color:var(--fg,#ddd);opacity:.6;cursor:pointer;font-family:system-ui,sans-serif;";
    btn.onmouseenter = function () { btn.style.opacity = "1"; };
    btn.onmouseleave = function () { btn.style.opacity = ".6"; };
    btn.onclick = function () {
      var next = (localStorage.getItem("hooshmand_dir") || "rtl") === "rtl" ? "ltr" : "rtl";
      localStorage.setItem("hooshmand_dir", next);
      location.reload();
    };
    document.body.appendChild(btn);
  }

  function run() {
    try {
      applyDir();
      translateText(document.body);
      translateAttrs(document.body);
      addDirToggle();
    } catch (e) { /* never break the app over translation */ }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
  // The app renders some chrome asynchronously; re-run a couple of times.
  setTimeout(run, 800);
  setTimeout(run, 2000);
})();
