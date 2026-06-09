# Dari / Persian / Tajik training data — sources & strategy

Goal: assemble (A) raw text for fluency and (B) instruction pairs for assistant
behavior, **tagged by dialect** (`dari` first, then `farsi`, `tajik`). Quality
and native review matter far more than raw volume.

> **Always check licensing** before training on a source, and keep a record of
> provenance per dataset. Prefer openly-licensed or your-own-collected data.

## A. Raw text (continued-pretraining / fluency)

Dari (Afghanistan):
- Dari Wikipedia (fa-AF content where separable; otherwise tag carefully)
- Afghan news outlets publishing in Dari (e.g. national broadcasters, agencies)
- Dari literature, poetry, and public-domain books
- Government / NGO Dari documents (often plain, clean register)
- Transcripts/subtitles of Dari radio, podcasts, and YouTube

Iranian Persian (Farsi):
- Persian Wikipedia, OSCAR / mC4 Persian splits, CommonCrawl Persian
- Persian news and literature corpora

Tajik (Cyrillic):
- Tajik Wikipedia, Tajik news sites, Tajik literature (Cyrillic)
- Note the script: keep Tajik in Cyrillic; don't transliterate unless intended

## B. Instruction data (SFT — makes it a good assistant)

Best → acceptable:
1. **Native-written** Dari prompt→response pairs (highest quality; aim for a few
   thousand covering Q&A, summarize, rewrite, explain, task help, tool-style
   replies in Arian's voice).
2. **Translated-then-edited**: take high-quality English/Persian instruction
   sets (e.g. open Alpaca-style / Dolly-style / OASST-style data) and translate
   to Dari, then have a native speaker fix register and vocabulary.
3. **Your real Hooshmand chats** once it's running (with consent), as ongoing
   fine-tuning fuel.

Tag every example: `{"dialect": "dari", ...}` so dialects can be mixed or kept
as separate LoRA adapters later.

## Cleaning checklist
- Deduplicate (exact + near-dup) and strip boilerplate / nav text.
- Normalize characters: use the correct Persian forms — `ی`/`ک` (not Arabic
  `ي`/`ك`), and normalize ZWNJ usage.
- Drop machine-translated text that wasn't human-reviewed for SFT.
- Filter Iranian-Farsi-specific markers out of the Dari set (and vice-versa) so
  dialects don't bleed.
- Remove PII and anything you don't have the right to use.

## Pipeline
1. Collect → `training/data/raw/<dialect>/...`
2. Convert instruction data to our format with `convert_to_jsonl.py`
   → `training/data/<dialect>_sft.jsonl`
3. Native-speaker review pass (the single biggest quality lever).
4. Train with `train_qlora.py`; evaluate with `eval/run_eval.py`.
