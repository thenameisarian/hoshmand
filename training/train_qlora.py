"""
Hooshmand — Dari QLoRA SFT template (Unsloth).

Edit the CONFIG block, drop native-reviewed data into data/*.jsonl, then:
    pip install "unsloth" trl peft accelerate bitsandbytes
    python train_qlora.py

Produces a LoRA adapter + merged model. Export to GGUF for Ollama, or serve
the merged model with vLLM, then point Hooshmand's assistant endpoint at it.

This is a STARTING POINT, not a tuned recipe — expect to iterate on data and
hyperparameters with native-speaker eval (see ../docs/dari-finetuning-plan.md).
"""

# ─────────────────────────── CONFIG ───────────────────────────
BASE_MODEL   = "unsloth/Qwen2.5-7B-Instruct"   # strong Persian baseline; 14B if GPU allows
DATA_GLOB    = "data/*.jsonl"                    # dialect-tagged SFT data
OUTPUT_DIR   = "outputs/hooshmand-dari-qlora"
MAX_SEQ_LEN  = 2048
EPOCHS       = 2          # raise once you have more/better data
LR           = 2e-4
BATCH        = 2
GRAD_ACCUM   = 8         # effective batch = BATCH * GRAD_ACCUM
DIALECTS     = ["dari"]  # Stage 1 = Dari only; add "farsi","tajik" later
EXPORT_GGUF  = True      # for Ollama serving
# ───────────────────────────────────────────────────────────────

import glob, json

from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from datasets import Dataset
from trl import SFTTrainer, SFTConfig


def load_rows():
    rows = []
    for path in glob.glob(DATA_GLOB):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if obj.get("dialect", "dari") in DIALECTS and obj.get("messages"):
                    rows.append({"messages": obj["messages"]})
    if not rows:
        raise SystemExit(f"No rows matched dialects {DIALECTS} in {DATA_GLOB}. "
                         "Add real, native-reviewed Dari data first.")
    print(f"Loaded {len(rows)} examples for dialects={DIALECTS}")
    return Dataset.from_list(rows)


def main():
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=BASE_MODEL, max_seq_length=MAX_SEQ_LEN,
        load_in_4bit=True,  # QLoRA
    )
    model = FastLanguageModel.get_peft_model(
        model, r=16, lora_alpha=16, lora_dropout=0.0,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        use_gradient_checkpointing="unsloth",
    )
    tokenizer = get_chat_template(tokenizer, chat_template="qwen-2.5")

    ds = load_rows()

    def fmt(ex):
        return {"text": tokenizer.apply_chat_template(
            ex["messages"], tokenize=False, add_generation_prompt=False)}
    ds = ds.map(fmt)

    trainer = SFTTrainer(
        model=model, tokenizer=tokenizer, train_dataset=ds,
        args=SFTConfig(
            dataset_text_field="text", max_seq_length=MAX_SEQ_LEN,
            per_device_train_batch_size=BATCH,
            gradient_accumulation_steps=GRAD_ACCUM,
            num_train_epochs=EPOCHS, learning_rate=LR,
            warmup_ratio=0.05, logging_steps=5,
            optim="adamw_8bit", output_dir=OUTPUT_DIR, seed=42,
        ),
    )
    trainer.train()

    model.save_pretrained_merged(OUTPUT_DIR + "-merged", tokenizer, save_method="merged_16bit")
    if EXPORT_GGUF:
        model.save_pretrained_gguf(OUTPUT_DIR + "-gguf", tokenizer, quantization_method="q4_k_m")
    print("Done. Serve with Ollama (GGUF) or vLLM (merged), then set it in Hooshmand Settings.")


if __name__ == "__main__":
    main()
