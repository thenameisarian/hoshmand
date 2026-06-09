# Hooshmand — Dari fine-tuning scaffold

Companion to `../docs/dari-finetuning-plan.md`. Fill in data, pick a GPU, run.

```
training/
├── README.md                 # this file
├── data/
│   └── dari_sft.example.jsonl # dataset format (replace with real, native-reviewed data)
└── train_qlora.py            # Unsloth QLoRA SFT template (edit the CONFIG block)
```

## Dataset format (`data/*.jsonl`)

One JSON object per line. `dialect` lets us mix/seperate dialects later
(`dari` first; `farsi` / `tajik` come after).

```json
{"dialect": "dari", "messages": [
  {"role": "system", "content": "تو آرین هستی، دستیار هوشمند کاربر."},
  {"role": "user", "content": "سلام، حالت چطور است؟"},
  {"role": "assistant", "content": "سلام، تشکر. خوب هستم. چطور می‌توانم کمک‌تان کنم؟"}
]}
```

## Run (after editing CONFIG in train_qlora.py)

```bash
pip install "unsloth[colab-new]" trl peft accelerate bitsandbytes
python train_qlora.py
# → outputs a merged model + GGUF you can serve with Ollama/vLLM
```

Then point Hooshmand's assistant at the served endpoint (Settings → endpoint_url + model).

> Native-speaker review of the Dari data is the single biggest quality lever.
> Prefer a few thousand genuinely good examples over many machine-translated ones.
