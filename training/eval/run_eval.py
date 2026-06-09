"""
Run an eval set through a served model (OpenAI-compatible endpoint) and dump the
model's answers to a file for **native-speaker review** — the right way to judge
dialect quality (automatic metrics miss it).

Usage:
    python run_eval.py dari_eval.example.jsonl \
        --base-url http://localhost:11434/v1 \
        --model qwen2.5:7b \
        --system "تو آریان هستی، دستیار هوشمند کاربر. به دری روان پاسخ بده." \
        --out results.md

Then a native Dari speaker rates each answer for: fluency, dialect-correctness
(Dari vs Tehrani markers), and helpfulness. Use the scores to fix the SFT data.

Requires: pip install openai
"""

import argparse
import json


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("evalset")
    ap.add_argument("--base-url", default="http://localhost:11434/v1")
    ap.add_argument("--api-key", default="not-needed")
    ap.add_argument("--model", required=True)
    ap.add_argument("--system", default="")
    ap.add_argument("--out", default="results.md")
    ap.add_argument("--temperature", type=float, default=0.7)
    args = ap.parse_args()

    from openai import OpenAI
    client = OpenAI(base_url=args.base_url, api_key=args.api_key)

    rows = load_jsonl(args.evalset)
    with open(args.out, "w", encoding="utf-8") as w:
        w.write(f"# Eval results — model `{args.model}`\n\n")
        w.write("Rate each answer 1-5 on fluency, dialect-correctness, helpfulness.\n\n")
        for r in rows:
            msgs = ([{"role": "system", "content": args.system}] if args.system else []) + [
                {"role": "user", "content": r["prompt"]}
            ]
            try:
                resp = client.chat.completions.create(
                    model=args.model, messages=msgs, temperature=args.temperature)
                answer = resp.choices[0].message.content.strip()
            except Exception as e:
                answer = f"[ERROR: {e}]"
            w.write(f"## {r.get('id','?')} ({r.get('dialect','?')})\n\n")
            w.write(f"**Prompt:** {r['prompt']}\n\n")
            w.write(f"**Answer:**\n\n{answer}\n\n")
            w.write("**Scores:** fluency __/5 · dialect __/5 · helpful __/5 · notes: \n\n---\n\n")
            print(f"done: {r.get('id','?')}")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
