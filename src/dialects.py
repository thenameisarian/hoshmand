"""Persian / Dari / Tajik dialect catalog for Hooshmand.

Single source of truth (Python side) for the dialect the assistant replies in.
The selected dialect is stored in settings as ``assistant_dialect`` (a code from
this catalog) and turned into a short steering instruction that is injected into
the system prompt at chat time (see src/chat_processor.build_context_preface).

We deliberately list *dialects of Persian* across its three standard varieties
(Iranian Persian / Farsi, Dari, Tajik) plus Auto-detect and English. Separate
but related languages (Gilaki, Mazandarani, Luri/Bakhtiari, Tati, Talysh, the
Pamiri languages, Pashto) are intentionally NOT listed here — they are not
Persian dialects.

Scripts: Iranian Persian and Dari use the Perso-Arabic script; Tajik uses
Cyrillic.
"""

from typing import Optional

# Group keys used to organise the dropdown.
GROUP_GENERAL = "General"
GROUP_FARSI = "Iranian Persian (Farsi)"
GROUP_DARI = "Dari (Afghanistan)"
GROUP_TAJIK = "Tajik (Tajikistan / Central Asia)"

# Each entry: code, group, en (English label), native (endonym),
# script ("perso-arabic" | "cyrillic" | "latin"), region.
# Order within a group puts the "Standard" variety first.
DIALECTS: list[dict] = [
    # ── General ──
    {"code": "auto", "group": GROUP_GENERAL, "en": "Auto-detect (match the user)",
     "native": "خودکار", "script": "any", "region": ""},
    {"code": "en", "group": GROUP_GENERAL, "en": "English",
     "native": "English", "script": "latin", "region": ""},

    # ── Iranian Persian (Farsi) — Perso-Arabic ──
    {"code": "fa-standard", "group": GROUP_FARSI, "en": "Standard Iranian Persian (Tehrani)",
     "native": "فارسی معیار", "script": "perso-arabic", "region": "Iran"},
    {"code": "fa-tehrani", "group": GROUP_FARSI, "en": "Tehrani", "native": "تهرانی",
     "script": "perso-arabic", "region": "Tehran, Iran"},
    {"code": "fa-esfahani", "group": GROUP_FARSI, "en": "Esfahani", "native": "اصفهانی",
     "script": "perso-arabic", "region": "Isfahan, Iran"},
    {"code": "fa-shirazi", "group": GROUP_FARSI, "en": "Shirazi", "native": "شیرازی",
     "script": "perso-arabic", "region": "Shiraz, Iran"},
    {"code": "fa-mashhadi", "group": GROUP_FARSI, "en": "Mashhadi (Khorasani)",
     "native": "مشهدی", "script": "perso-arabic", "region": "Mashhad / Khorasan, Iran"},
    {"code": "fa-yazdi", "group": GROUP_FARSI, "en": "Yazdi", "native": "یزدی",
     "script": "perso-arabic", "region": "Yazd, Iran"},
    {"code": "fa-kermani", "group": GROUP_FARSI, "en": "Kermani", "native": "کرمانی",
     "script": "perso-arabic", "region": "Kerman, Iran"},
    {"code": "fa-tabrizi", "group": GROUP_FARSI, "en": "Tabrizi Persian", "native": "فارسی تبریزی",
     "script": "perso-arabic", "region": "Tabriz, Iran"},
    {"code": "fa-abadani", "group": GROUP_FARSI, "en": "Abadani (Khuzestani)", "native": "آبادانی",
     "script": "perso-arabic", "region": "Abadan / Khuzestan, Iran"},
    {"code": "fa-qazvini", "group": GROUP_FARSI, "en": "Qazvini", "native": "قزوینی",
     "script": "perso-arabic", "region": "Qazvin, Iran"},
    {"code": "fa-kashani", "group": GROUP_FARSI, "en": "Kashani", "native": "کاشانی",
     "script": "perso-arabic", "region": "Kashan, Iran"},
    {"code": "fa-hamedani", "group": GROUP_FARSI, "en": "Hamedani", "native": "همدانی",
     "script": "perso-arabic", "region": "Hamadan, Iran"},

    # ── Dari (Afghanistan) — Perso-Arabic ──
    {"code": "prs-standard", "group": GROUP_DARI, "en": "Standard Dari (Kabuli)",
     "native": "دری معیار", "script": "perso-arabic", "region": "Afghanistan"},
    {"code": "prs-kabuli", "group": GROUP_DARI, "en": "Kabuli", "native": "کابلی",
     "script": "perso-arabic", "region": "Kabul, Afghanistan"},
    {"code": "prs-herati", "group": GROUP_DARI, "en": "Herati", "native": "هراتی",
     "script": "perso-arabic", "region": "Herat, Afghanistan"},
    {"code": "prs-mazari", "group": GROUP_DARI, "en": "Mazari (Balkhi)", "native": "مزاری",
     "script": "perso-arabic", "region": "Mazar-e Sharif / Balkh, Afghanistan"},
    {"code": "prs-badakhshi", "group": GROUP_DARI, "en": "Badakhshi", "native": "بدخشی",
     "script": "perso-arabic", "region": "Badakhshan, Afghanistan"},
    {"code": "prs-panjshiri", "group": GROUP_DARI, "en": "Panjshiri", "native": "پنجشیری",
     "script": "perso-arabic", "region": "Panjshir, Afghanistan"},
    {"code": "prs-hazaragi", "group": GROUP_DARI, "en": "Hazaragi", "native": "هزارگی",
     "script": "perso-arabic", "region": "Hazarajat, Afghanistan"},
    {"code": "prs-aimaqi", "group": GROUP_DARI, "en": "Aimaqi", "native": "ایماقی",
     "script": "perso-arabic", "region": "Western/Central Afghanistan"},

    # ── Tajik (Tajikistan / Central Asia) — Cyrillic ──
    {"code": "tg-standard", "group": GROUP_TAJIK, "en": "Standard Tajik",
     "native": "тоҷикии адабӣ", "script": "cyrillic", "region": "Tajikistan"},
    {"code": "tg-khujandi", "group": GROUP_TAJIK, "en": "Khujandi (Northern)",
     "native": "хуҷандӣ", "script": "cyrillic", "region": "Khujand / Sughd, Tajikistan"},
    {"code": "tg-samarqandi", "group": GROUP_TAJIK, "en": "Samarqandi–Bukhori",
     "native": "самарқандӣ-бухороӣ", "script": "cyrillic", "region": "Samarkand/Bukhara, Uzbekistan"},
    {"code": "tg-bukhori", "group": GROUP_TAJIK, "en": "Bukhori (Bukharan)",
     "native": "бухороӣ", "script": "cyrillic", "region": "Bukhara, Central Asia"},
    {"code": "tg-kulobi", "group": GROUP_TAJIK, "en": "Kulobi (Southern)",
     "native": "кӯлобӣ", "script": "cyrillic", "region": "Kulob, Tajikistan"},
    {"code": "tg-badakhshani", "group": GROUP_TAJIK, "en": "Badakhshani Tajik",
     "native": "бадахшонӣ", "script": "cyrillic", "region": "Gorno-Badakhshan, Tajikistan"},
]

_BY_CODE = {d["code"]: d for d in DIALECTS}

_SCRIPT_NAME = {
    "perso-arabic": "the Perso-Arabic script",
    "cyrillic": "the Cyrillic (Tajik) script",
    "latin": "the Latin alphabet",
}


def is_valid(code: Optional[str]) -> bool:
    return bool(code) and code in _BY_CODE


def get(code: str) -> Optional[dict]:
    return _BY_CODE.get(code)


def choices() -> list[dict]:
    """Catalog for building the UI dropdown (code, group, label, native)."""
    return [
        {"code": d["code"], "group": d["group"], "en": d["en"], "native": d["native"]}
        for d in DIALECTS
    ]


def dialect_directive(code: Optional[str]) -> str:
    """Return a short system-prompt steering instruction for the given dialect
    code, or "" when no explicit steering is needed (auto-detect)."""
    d = _BY_CODE.get(code or "auto")
    if not d or d["code"] == "auto":
        # Auto-detect: let the assistant persona's own language rules apply
        # (Hooshmand defaults to Dari and matches the user otherwise).
        return ""
    if d["code"] == "en":
        return "Respond to the user in English."
    script = _SCRIPT_NAME.get(d["script"], "the appropriate script")
    region = f" as spoken in {d['region']}" if d.get("region") else ""
    return (
        f"LANGUAGE / DIALECT: Respond to the user in {d['en']} "
        f"({d['native']}){region}. Use the characteristic vocabulary, idioms, "
        f"phrasing, and register of this dialect, and write in {script}. "
        f"Keep it natural and fluent to a native speaker of this variety; "
        f"do not drift into a different Persian dialect."
    )
