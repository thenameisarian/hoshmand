"""
Convert common instruction-dataset formats into Hooshmand's dialect-tagged
chat JSONL (one object per line):

    {"dialect": "dari", "messages": [{"role": "...","content": "..."}, ...]}

Supported inputs (auto-detected, or force with --format):
  * alpaca   : [{"instruction","input","output"}, ...]   (.json)
  * sharegpt : [{"conversations":[{"from","value"}, ...]}, ...]  (.json)
  * messages : [{"messages":[{"role","content"}, ...]}, ...]  (.json/.jsonl)
  * csv      : columns prompt,response (+ optional system)   (.csv)

Usage:
    python convert_to_jsonl.py input.json --dialect dari --out data/dari_sft.jsonl
    python convert_to_jsonl.py pairs.csv  --dialect farsi --system "تو آریان هستی."

Normalizes Persian characters (Arabic ي/ك -> Persian ی/ک) by default.
This does NOT translate or review — pair it with native-speaker review.
"""

import argparse
import csv
import json
import os
import sys

# Arabic -> Persian character normalization (common in scraped text).
_NORM = {"ي": "ی", "ك": "ک"}  # ي->ی , ك->ک


def normalize(s):
    if not isinstance(s, str):
        return s
    for a, b in _NORM.items():
        s = s.replace(a, b)
    return s


def from_alpaca(rows, system):
    for r in rows:
        instr = (r.get("instruction") or "").strip()
        inp = (r.get("input") or "").strip()
        out = (r.get("output") or "").strip()
        if not instr or not out:
            continue
        user = instr if not inp else f"{instr}\n\n{inp}"
        msgs = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": user},
            {"role": "assistant", "content": out},
        ]
        yield msgs


def from_sharegpt(rows, system):
    role_map = {"human": "user", "user": "user", "gpt": "assistant",
                "assistant": "assistant", "system": "system"}
    for r in rows:
        conv = r.get("conversations") or r.get("conversation") or []
        msgs = [{"role": "system", "content": system}] if system else []
        for turn in conv:
            role = role_map.get((turn.get("from") or turn.get("role") or "").lower())
            content = (turn.get("value") or turn.get("content") or "").strip()
            if role and content:
                msgs.append({"role": role, "content": content})
        if any(m["role"] == "assistant" for m in msgs):
            yield msgs


def from_messages(rows, system):
    for r in rows:
        msgs = r.get("messages") or []
        if system and not any(m.get("role") == "system" for m in msgs):
            msgs = [{"role": "system", "content": system}] + msgs
        if msgs and any(m.get("role") == "assistant" for m in msgs):
            yield [{"role": m["role"], "content": m["content"]} for m in msgs]


def from_csv(path, system):
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            user = (row.get("prompt") or row.get("question") or "").strip()
            out = (row.get("response") or row.get("answer") or "").strip()
            sys_ = (row.get("system") or system or "").strip()
            if not user or not out:
                continue
            msgs = ([{"role": "system", "content": sys_}] if sys_ else []) + [
                {"role": "user", "content": user},
                {"role": "assistant", "content": out},
            ]
            yield msgs


def load_json_any(path):
    with open(path, encoding="utf-8") as f:
        if path.endswith(".jsonl"):
            return [json.loads(l) for l in f if l.strip()]
        return json.load(f)


def detect(path, rows):
    if path.endswith(".csv"):
        return "csv"
    if rows and isinstance(rows[0], dict):
        if "conversations" in rows[0]:
            return "sharegpt"
        if "messages" in rows[0]:
            return "messages"
        if "instruction" in rows[0]:
            return "alpaca"
    return "messages"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--dialect", required=True,
                    help="dialect tag, e.g. dari / farsi / tajik")
    ap.add_argument("--out", default=None)
    ap.add_argument("--format", choices=["alpaca", "sharegpt", "messages", "csv"])
    ap.add_argument("--system", default="", help="optional system prompt to prepend")
    ap.add_argument("--no-normalize", action="store_true")
    args = ap.parse_args()

    out_path = args.out or f"data/{args.dialect}_sft.jsonl"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    if args.input.endswith(".csv"):
        rows, fmt = None, "csv"
    else:
        rows = load_json_any(args.input)
        fmt = args.format or detect(args.input, rows)

    if fmt == "csv":
        gen = from_csv(args.input, args.system)
    elif fmt == "alpaca":
        gen = from_alpaca(rows, args.system)
    elif fmt == "sharegpt":
        gen = from_sharegpt(rows, args.system)
    else:
        gen = from_messages(rows, args.system)

    n = 0
    with open(out_path, "w", encoding="utf-8") as w:
        for msgs in gen:
            if not args.no_normalize:
                for m in msgs:
                    m["content"] = normalize(m["content"])
            w.write(json.dumps({"dialect": args.dialect, "messages": msgs},
                               ensure_ascii=False) + "\n")
            n += 1
    print(f"Wrote {n} examples (dialect={args.dialect}, format={fmt}) -> {out_path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
