"""Run the Gradio demo using a locally saved LoRA adapter.

After training with the notebook, copy/download the final_adapter directory into
bug_explanation_lora/final_adapter (or set LORA_ADAPTER_PATH).
"""
import os
from pathlib import Path

import gradio as gr
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_MODEL = os.getenv("BASE_MODEL", "Qwen/Qwen2.5-Coder-0.5B-Instruct")
DEFAULT_ADAPTER = Path(__file__).resolve().parents[1] / "bug_explanation_lora" / "final_adapter"
ADAPTER_PATH = Path(os.getenv("LORA_ADAPTER_PATH", str(DEFAULT_ADAPTER)))

if not ADAPTER_PATH.is_dir():
    raise FileNotFoundError(
        f"LoRA adapter not found at {ADAPTER_PATH}. Run the training notebook, "
        "save the final_adapter folder, then set LORA_ADAPTER_PATH if needed."
    )

tokenizer = AutoTokenizer.from_pretrained(str(ADAPTER_PATH))
dtype = torch.float16 if torch.cuda.is_available() else torch.float32
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=dtype,
    device_map="auto" if torch.cuda.is_available() else None,
)
model = PeftModel.from_pretrained(base_model, str(ADAPTER_PATH))
model.eval()

def explain_bug(code):
    if not code or not code.strip():
        return "Please enter some Python code first."

    messages = [
        {"role": "system", "content": (
            "You are a Python debugging assistant. Identify the likely bug, "
            "explain why it occurs, and provide corrected code. If the code is "
            "valid, say so rather than inventing a bug."
        )},
        {"role": "user", "content": f"Explain and fix this Python code:\n```python\n{code}\n```"},
    ]
    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True,
        return_tensors="pt", return_dict=True
    )
    device = next(model.parameters()).device
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        output = model.generate(
            **inputs, max_new_tokens=200, do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
    prompt_len = inputs["input_ids"].shape[1]
    return tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True).strip()

demo = gr.Interface(
    fn=explain_bug,
    inputs=gr.Code(label="Enter Python code", language="python", lines=10),
    outputs=gr.Markdown(label="Bug explanation and suggested fix"),
    title="Code Bug Explanation Assistant using LoRA",
    description="Educational prototype. Review generated explanations and fixes before using them.",
    examples=[
        ["def multiply(a, b):\n    return a + b\n\nprint(multiply(3, 4))"],
        ["numbers = [1, 2, 3]\nprint(numbers[3])"],
        ["for i in range(5)\n    print(i)"],
    ],
)
if __name__ == "__main__":
    demo.launch()
