# Code Bug Explanation Assistant using LoRA

An educational prototype that fine-tunes Qwen2.5-Coder-0.5B-Instruct with LoRA to explain code bugs. The notebook uses a very small synthetic dataset, so results are for demonstration and not a benchmark of real-world accuracy.

## Getting started

1. Open `Code_Bug_Explanation_Assistant_Documented.ipynb` in Google Colab.
2. Run the notebook cells in order.
3. Review the dataset, training configuration, and Gradio demo.

## Model and training

- Base model: `Qwen/Qwen2.5-Coder-0.5B-Instruct`
- Fine-tuning: PEFT LoRA
- LoRA configuration: r=8, alpha=16, dropout=0.05
- Dataset: 10 synthetic examples (8 train, 2 test)

## Limitations

This is a small educational prototype. Evaluate on a larger, diverse dataset before making claims about reliability.
