# Hooshmand — Plan: Teaching the model proper Dari (then other dialects)

> Status: **draft for review.** Nothing here is executed yet — training needs your
> decisions (compute, base model, data) and approval. This is the priority track:
> get *proper Dari* right first, then add Iranian Farsi and Tajik.

## The key reality

Hooshmand (the app) does **not** train or contain a model. It is an orchestration
layer that sends your messages to an **LLM endpoint** (OpenAI-compatible API, Ollama,
vLLM, etc.) configured in Settings. A system prompt can *steer* a model toward Dari,
but it cannot give a model Dari fluency it doesn't already have.

So "train the model for proper Dari" is its own small ML project with three stages:

```
   (1) Fine-tune a base model on Dari      ──►   (2) Serve it behind an
       (improve real Dari fluency)               OpenAI-compatible endpoint
                                                          │
                                                          ▼
                                            (3) Point Hooshmand's assistant
                                                at that endpoint + model
                                                (endpoint_url + model in Settings)
```

Stage 3 is trivial and already wired (the Arian persona is built). Stages 1–2 are
the work.

## Why Dari is the hard part

Most open models have seen a fair amount of **Iranian Farsi** (Persian) but very
little **Dari** specifically. Dari and Iranian Farsi share writing and most grammar,
but differ in vocabulary, idiom, register, some pronunciation, and common phrasing.
A model trained mostly on Iranian Farsi will sound subtly "off" / Tehrani to an Afghan
ear. Our job is to **shift the model's Persian toward Dari register and vocabulary**,
which is mostly a *data* problem, not a *compute* problem.

## Stage 1 — choosing a base model

We want strong existing Persian, open weights, and a size we can fine-tune affordably.
Candidates (all open-weight as of this writing):

| Model | Size | Persian strength | Notes |
|---|---|---|---|
| **Qwen2.5** | 7B / 14B | Very strong multilingual incl. Persian | Best default starting point; great quality-per-param |
| **Aya Expanse** (Cohere) | 8B / 32B | Explicitly multilingual, good Persian | Built for non-English; license is research-leaning — check terms |
| **Llama 3.1** | 8B | Decent Persian | Huge ecosystem/tooling, permissive license |
| **Gemma 2** | 9B | Decent Persian | Good small-model quality |

**Recommendation:** start from **Qwen2.5-7B-Instruct** (or 14B if your GPU allows).
Strongest Persian baseline, so the Dari fine-tune has the least distance to travel.

## Stage 1 — data strategy (this is where Dari quality is won)

Two complementary datasets:

**A. Raw Dari text** (for continued-pretraining / fluency — optional but high-impact)
- Afghan Dari news outlets, Dari Wikipedia, Dari literature/poetry, religious texts
- Transcribed Dari speech (radio, podcasts, YouTube with Dari subtitles)
- Goal: tens of millions of tokens, cleaned and deduplicated

**B. Dari instruction data** (for SFT — the part that makes it a good *assistant*)
- prompt → ideal Dari response pairs, covering: Q&A, summarization, rewriting,
  task help, tool-use style replies that match the Arian persona
- Sources: (i) human-written by native Dari speakers, (ii) high-quality existing
  Persian/English instruction sets *translated to Dari and then human-edited*,
  (iii) your own real Hooshmand conversations once it's running
- Tag every example with dialect = `dari` so we can mix dialects later cleanly

**Quality > quantity.** A few thousand *genuinely good, native-reviewed* Dari
instruction examples beat 100k machine-translated ones. Native-speaker review is the
single biggest lever on "proper Dari."

Data schema (JSONL) and a starter file are scaffolded in `training/` (see below).

## Stage 1 — training method

For a solo developer this is very doable with **QLoRA** (4-bit) on a single GPU:

- **Hardware:** one 24 GB GPU (RTX 4090 / A5000) fine-tunes a 7–9B model in QLoRA.
  No GPU? Rent an A100 40/80GB by the hour (cheap for a few-hour run).
- **Tooling:** **Unsloth** (fastest, lowest VRAM) or **Axolotl** (config-driven) on
  top of HF TRL. Both produce a LoRA adapter you merge into the base model.
- **Recipe:**
  1. (optional) continued-pretrain LoRA on raw Dari text — improves fluency
  2. SFT LoRA on the Dari instruction set — makes it a good Dari assistant
  3. (optional, later) DPO on native-speaker preference pairs — polishes tone
- **Output:** merged weights → export to **GGUF** (for Ollama) or serve fp16 with vLLM.

A ready-to-edit Unsloth QLoRA script is scaffolded in `training/train_qlora.py`.

## Stage 2 — serving + connecting to Hooshmand

- **Ollama** (easiest): `ollama create hooshmand-dari -f Modelfile` then it exposes an
  OpenAI-compatible endpoint at `http://localhost:11434/v1`.
- **vLLM** (faster, GPU): `vllm serve <merged-model> --api-key ...` → OpenAI-compatible.
- In Hooshmand: Settings → set the assistant's `endpoint_url` + `model` to your served
  Dari model. The Arian persona (already built) then speaks through *your* Dari model.

## Stage 2 — evaluation (don't skip)

- Build a **held-out Dari eval set** (~200 prompts) the model never trained on.
- **Native-speaker rating** of fluency, dialect-correctness (Dari vs Tehrani markers),
  and helpfulness — automated metrics (BLEU/ROUGE) miss dialect quality entirely.
- Quick automatic check: flag Iranian-Farsi-specific tokens leaking into outputs.

## Stage 3 — then the other dialects

Once Dari is solid, add **Iranian Farsi** and **Tajik** without regressing Dari:
- Gather the same A/B data for each, tagged `farsi` / `tajik` (Tajik = Cyrillic).
- Either (i) one model trained on all three with dialect tags + system-prompt steering,
  or (ii) **separate LoRA adapters per dialect** swapped at serve time (clean, no
  cross-contamination). Recommendation: per-dialect adapters — matches the
  "Dari first, then others" sequencing perfectly.

## What I need from you to start (we'll do this together)

1. **Compute:** own GPU (which one?) or cloud budget for rented hours?
2. **Base model:** Qwen2.5-7B (my default) or another?
3. **Data:** do you have any Dari text/conversations already, or should we plan a
   collection + native-review pass first?
4. **Scale/timeline:** quick proof-of-concept adapter, or a serious run?

## Rough effort / cost (QLoRA, 7B, single run)

- Data prep + native review: the real time cost (days–weeks depending on volume).
- Actual training: a few GPU-hours (~$5–30 rented, or free on your own GPU).
- Iterate: expect 2–4 cycles of train → eval → fix data.

---
*Companion scaffolding lives in `training/` — dataset schema, an example Dari SFT
file, and a QLoRA training script template, all ready to fill in.*
