# Dari fine-tuning — resume here (next session)

Status as of last session:
- ✅ Python 3.11.9 confirmed (`py -3.11`)
- ✅ Data script wired to **Claude** (Anthropic), with the "translate-don't-answer" fix
- ✅ A 20-example Claude test produced **excellent, authentic Dari** (موتر، فابریکه، کیمیاوی…)
- ✅ API key safe: lives in `$env:ANTHROPIC_API_KEY` only; `.env`/keys gitignored
- ⏳ Last action pending: re-run the 20 to confirm the question-vs-answer fix

Your key is a **session** env var, so set it again each new PowerShell window:
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."   # don't paste this line anywhere public
cd C:\Users\arian\odysseus\training
```

## 1. Confirm the fix (re-run 20)
```powershell
python prepare_dari_data.py --dataset https://raw.githubusercontent.com/tatsu-lab/stanford_alpaca/main/alpaca_data.json --limit 20 --model claude-sonnet-4-6 --out data/dari_sft.jsonl
```
Check that the **user** turn is now the *question* and the **assistant** turn the *answer*.

## 2. Bulk-generate the real dataset (a few hundred)
```powershell
python prepare_dari_data.py --dataset https://raw.githubusercontent.com/tatsu-lab/stanford_alpaca/main/alpaca_data.json --limit 500 --model claude-sonnet-4-6 --out data/dari_sft.jsonl
```
(500 examples ≈ a few dollars on the API; bump higher for a stronger model.)

## 3. Native-speaker review
Skim `data/dari_sft.jsonl`, fix any Tehrani-Farsi leakage / errors. Biggest quality lever.

## 4. Training environment (Python 3.11)
```powershell
py -3.11 -m venv venv-train
venv-train\Scripts\activate
pip install -r requirements-train.txt
```
⚠️ Heads-up: **unsloth on native Windows is unreliable.** If `pip install` or training
fails, the robust fallbacks are: (a) run training under **WSL2** (Ubuntu) on the same
GPU, or (b) switch `train_qlora.py` to plain `transformers + peft + bitsandbytes`
(no unsloth). Flag it and we'll pick the path.

## 5. Train, then serve
```powershell
python train_qlora.py            # QLoRA on Qwen2.5-7B; outputs a GGUF
# import GGUF into Ollama as 'hooshmand-dari', then in Hooshmand Settings
# set the assistant's model to hooshmand-dari and evaluate with eval/run_eval.py
```

## Don't forget
Commit the uncommitted script + gitignore changes from last session:
```powershell
cd C:\Users\arian\odysseus
git add -A
git commit -m "training: Claude data generator + prompt fix; gitignore hardening"
git push
```
