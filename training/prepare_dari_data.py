"""
Prepare a Dari instruction-tuning set from an OPEN dataset by rendering each
example into natural Dari with an LLM (OpenAI-compatible endpoint — e.g. your
local Ollama, or a stronger model for better quality), then writing it in
Hooshmand's dialect-tagged chat JSONL format.

This is the "use open datasets" path: start from an existing instruction set,
translate/adapt into Dari, then have a NATIVE SPEAKER review (the biggest
quality lever) before training.

Example (using local Ollama):
    pip install -r requirements-train.txt
    python prepare_dari_data.py \
        --dataset tatsu-lab/alpaca --limit 500 \
        --endpoint http://localhost:11434/v1 --model qwen2.5:7b \
        --out data/dari_sft.jsonl

Tip: for better Dari, point --endpoint/--model at the strongest model you can
run (a 70B or a good API model) just for this data-prep step. The model you
*train* is separate.

Fields supported automatically: alpaca (instruction/input/output),
dolly (instruction/context/response), or generic (prompt/response).
Use --no-translate to only reformat a dataset that is already in Dari/Persian.
"""

import argparse
import json
import os
import sys
import time

SYS_PROMPT = (
    "تو آرین هستی، دستیار هوشمند و مودب کاربر. همیشه به دری روان و طبیعی پاسخ بده."
)

# Instruction to the translation model. Emphasise Dari (Afghan) register, not
# Tehrani Farsi, and to translate faithfully without adding commentary.
TRANSLATE_SYS = (
    "You are a professional translator into DARI (Afghan Persian, as spoken in "
    "Kabul) — NOT Iranian/Tehrani Persian. Translate the user's text into "
    "natural, fluent Dari, preserving meaning, formatting, lists, and code. "
    "Use Dari vocabulary and phrasing. Output ONLY the translation, no notes."
)


def _client(endpoint, api_key):
    from openai import OpenAI
    return OpenAI(base_url=endpoint, api_key=api_key or "not-needed")


def translate(client, model, text, retries=3):
    if not text or not text.strip():
        return text
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": TRANSLATE_SYS},
                          {"role": "user", "content": text}],
                temperature=0.3,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))


def extract_pair(row):
    """Return (user_text, assistant_text) from common schemas, or (None, None)."""
    if "instruction" in row:  # alpaca / dolly
        instr = (row.get("instruction") or "").strip()
        ctx = (row.get("input") or row.get("context") or "").strip()
        out = (row.get("output") or row.get("response") or "").strip()
        user = instr if not ctx else f"{instr}\n\n{ctx}"
        return (user or None), (out or None)
    if "prompt" in row:
        return (row.get("prompt") or "").strip() or None, (row.get("response") or "").strip() or None
    return None, None


def load_examples(dataset, split):
    """Load examples WITHOUT the heavy `datasets` lib when given a URL or a
    local .json/.jsonl path (works on any Python, incl. 3.14). Falls back to
    HuggingFace `datasets` for plain dataset ids (needs Python <=3.12)."""
    if dataset.startswith(("http://", "https://")) or dataset.endswith((".json", ".jsonl")):
        if dataset.startswith("http"):
            import urllib.request
            with urllib.request.urlopen(dataset) as r:
                raw = r.read().decode("utf-8")
        else:
            with open(dataset, encoding="utf-8") as f:
                raw = f.read()
        if dataset.endswith(".jsonl"):
            return [json.loads(l) for l in raw.splitlines() if l.strip()]
        return json.loads(raw)
    from datasets import load_dataset
    return load_dataset(dataset, split=split)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="tatsu-lab/alpaca",
                    help="HuggingFace dataset id (open instruction set)")
    ap.add_argument("--split", default="train")
    ap.add_argument("--limit", type=int, default=500, help="how many examples")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--endpoint", default="http://localhost:11434/v1")
    ap.add_argument("--api-key", default="")
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--dialect", default="dari")
    ap.add_argument("--out", default="data/dari_sft.jsonl")
    ap.add_argument("--no-translate", action="store_true",
                    help="dataset already Dari/Persian: just reformat")
    args = ap.parse_args()

    ds = load_examples(args.dataset, args.split)
    end = min(len(ds), args.offset + args.limit)
    client = None if args.no_translate else _client(args.endpoint, args.api_key)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    written = 0
    with open(args.out, "w", encoding="utf-8") as w:
        for i in range(args.offset, end):
            user, asst = extract_pair(ds[i])
            if not user or not asst:
                continue
            if not args.no_translate:
                try:
                    user = translate(client, args.model, user)
                    asst = translate(client, args.model, asst)
                except Exception as e:
                    print(f"  [skip {i}: {e}]", file=sys.stderr)
                    continue
            obj = {"dialect": args.dialect, "messages": [
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": user},
                {"role": "assistant", "content": asst},
            ]}
            w.write(json.dumps(obj, ensure_ascii=False) + "\n")
            written += 1
            if written % 25 == 0:
                print(f"  {written} written...", file=sys.stderr)

    print(f"Done: {written} Dari examples -> {args.out}", file=sys.stderr)
    print("NEXT: have a native Dari speaker review/fix, then run train_qlora.py",
          file=sys.stderr)


if __name__ == "__main__":
    main()
