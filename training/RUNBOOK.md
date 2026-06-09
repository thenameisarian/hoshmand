# Dari fine-tuning runbook — Qwen2.5-7B QLoRA on an NVIDIA RTX

Tailored to: **NVIDIA RTX GPU**, **open datasets** (LLM-rendered into Dari),
**Qwen2.5-7B** base. Goal: a first proper-Dari adapter, then iterate.

## 0. One-time setup (on the RTX machine)
```bash
cd training
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements-train.txt
```
A 24GB card (3090/4090) is comfortable for QLoRA on 7B. Smaller VRAM: lower
`MAX_SEQ_LEN`/`BATCH` in `train_qlora.py`, or use a 3B base.

## 1. Build the Dari dataset (open data -> Dari)
Use a strong model for the *translation* step if you can (better Dari); the
model you train is separate. Local Ollama works for a first pass:
```bash
ollama pull qwen2.5:7b      # or a bigger model for higher-quality Dari
python prepare_dari_data.py --dataset tatsu-lab/alpaca --limit 800 \
    --endpoint http://localhost:11434/v1 --model qwen2.5:7b \
    --out data/dari_sft.jsonl
```
You can run it several times with different `--dataset` / `--offset` to grow the
set (databricks/databricks-dolly-15k, OpenAssistant, etc.).

## 2. Native-speaker review (the most important step)
Open `data/dari_sft.jsonl` and have a native Dari speaker fix register,
vocabulary, and any Tehrani-Farsi leakage. Quality here beats quantity.

## 3. Train
```bash
python train_qlora.py     # reads data/*.jsonl where dialect == "dari"
```
Outputs a merged model and a GGUF (`outputs/hooshmand-dari-qlora-*`).

## 4. Evaluate
```bash
# serve the new model (e.g. import the GGUF into Ollama), then:
python eval/run_eval.py eval/dari_eval.example.jsonl \
    --base-url http://localhost:11434/v1 --model hooshmand-dari \
    --system "تو آریان هستی، به دری روان پاسخ بده." --out eval/results.md
```
Native-rate fluency / dialect-correctness / helpfulness in `results.md`.
If weak, improve the data (step 1–2) and retrain. Expect 2–4 cycles.

## 5. Serve + connect to Hooshmand
- **Ollama:** `ollama create hooshmand-dari -f Modelfile` (point at the GGUF).
- In Hooshmand → Settings → Models/Endpoints, set the assistant's model to
  `hooshmand-dari`. Arian now speaks through your Dari model.

## 6. Then other dialects
Repeat steps 1–5 with `--dialect farsi` and `--dialect tajik` (Tajik in
Cyrillic). Recommended: keep a **separate LoRA adapter per dialect** and switch
based on the Settings → Assistant Dialect choice (same dialect codes already in
`src/dialects.py`). This matches the "Dari first, then others" sequencing.
