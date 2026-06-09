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

  function run() {
    try {
      // Ensure RTL + lang even if the markup wasn't updated.
      document.documentElement.setAttribute("dir", "rtl");
      document.documentElement.setAttribute("lang", "fa");
      translateText(document.body);
      translateAttrs(document.body);
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
