# Hooshmand — Setup & Quickstart (Arian, the Persian assistant)

This is the short, opinionated path to get **Hooshmand** running and talking to
you as **Arian** in Dari/Persian. Hooshmand is a self-hosted web app: a Python
backend + browser UI. It does **not** include a language model — you connect one
(local via Ollama, or an API). See `dari-finetuning-plan.md` for making its Dari
genuinely good.

## 1. Save your changes first

The working tree has the Hooshmand/Arian edits but they may be uncommitted
(a git lock from the synced folder blocked the commit). From PowerShell:

```powershell
cd C:\Users\arian\odysseus
del .git\index.lock      # if it exists
del .git\index           # clears the corrupt index
git reset                # rebuilds the index from HEAD
git add -A
git commit -m "Hooshmand: Arian persona, Persian STT, dialect picker, rebrand"
```

## 2. Run the app

### Option A — Docker (easiest)
Install Docker Desktop, then:
```powershell
cd C:\Users\arian\odysseus
copy .env.example .env
docker compose up -d --build
```
Open <http://localhost:7000>. Find the first-login admin password with:
```powershell
docker compose logs odysseus | findstr -i password
```

### Option B — Native Windows
Run the bundled launcher (needs Python 3.11+):
```powershell
cd C:\Users\arian\odysseus
./launch-windows.ps1
```

On first launch Hooshmand creates an `admin` account and prints a temporary
password in the terminal. Log in, then change it in **Settings**.

## 3. Connect a model (the step people miss)

Hooshmand needs an LLM endpoint. For a Persian-first assistant, start with a
model that already has strong Persian:

### Local with Ollama (free, private)
```powershell
# install Ollama from https://ollama.com, then:
ollama pull qwen2.5:7b     # strong multilingual incl. Persian
ollama serve               # exposes http://localhost:11434
```
In Hooshmand: **Settings → Models / Endpoints**, add an endpoint:
- Base URL: `http://localhost:11434/v1`
- Model: `qwen2.5:7b`

(If running Hooshmand in Docker, use `http://host.docker.internal:11434/v1`.)

### Or an API
Add your provider's OpenAI-compatible base URL + API key and model name.

## 4. Pick the dialect

**Settings → Assistant Dialect** — defaults to **Standard Dari (Kabuli)**.
Choose Iranian Farsi, Tajik (Cyrillic), a regional dialect, English, or
Auto-detect. The choice is injected into Arian's system prompt, so replies
switch language immediately (no restart).

## 5. Meet Arian

Open the assistant. You'll see Arian greet you in Dari:

> سلام، من آریان هستم — دستیار هوشمند شما. چطور می‌توانم کمک‌تان کنم؟

Voice input transcribes in Persian by default (`stt_language = fa`). Voice
*output* and **your-own-voice cloning** need a TTS engine set up — Kokoro
(the bundled local TTS) doesn't do Persian, so that routes through an external
OpenAI-compatible TTS endpoint (see the voice notes in the plan).

## 6. Next: proper Dari

A system prompt steers the model toward Dari, but real Dari fluency comes from
fine-tuning. See `dari-finetuning-plan.md` and the `training/` scaffold —
that's the project that makes Arian's Dari genuinely native.
