# Code Bug Explanation Assistant using LoRA

An educational mini-project that fine-tunes `Qwen/Qwen2.5-Coder-0.5B-Instruct` with Low-Rank Adaptation (LoRA) to generate explanations and suggested corrections for buggy Python code.

> **Project status:** prototype/demo. The training data is a 10-example synthetic dataset. Outputs may be incorrect; this is not a production debugging tool or a benchmark of real-world accuracy. No performance metrics are claimed until actual run outputs have been reviewed.

## Project objectives

- Explore parameter-efficient fine-tuning with PEFT/LoRA.
- Build a simple interface where a user can submit buggy Python code.
- Generate a natural-language explanation and a possible correction.
- Record qualitative results on held-out examples.

## How it works

1. Generate a small synthetic dataset of Python bug examples.
2. Split examples into training and test sets.
3. Load the base code model and configure LoRA adapters.
4. Fine-tune the model.
5. Generate explanations for test snippets.
6. Launch a Gradio interface for interactive experimentation.

## Technology stack

- Python and Google Colab
- PyTorch
- Hugging Face Transformers and Datasets
- PEFT (LoRA)
- Gradio
- scikit-learn (dataset split)

## Model configuration

- **Base model:** `Qwen/Qwen2.5-Coder-0.5B-Instruct`
- **LoRA rank (r):** 8
- **LoRA alpha:** 16
- **LoRA dropout:** 0.05
- **Target modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`

The notebook is the primary reference for the training configuration and sequence of steps.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── Code_Bug_Explanation_Assistant_Documented.ipynb
├── src/
│   ├── generate_dataset.py
│   └── app.py
├── results/
│   ├── evaluation_results.csv
│   └── results.md
└── screenshots/
    └── .gitkeep
```

## Getting started: train in Google Colab

1. Open [the documented notebook](Code_Bug_Explanation_Assistant_Documented.ipynb) in Google Colab.
2. Choose **Runtime → Change runtime type** and select a GPU if available.
3. Run the notebook cells from top to bottom.
4. Review the model's actual responses and training metrics. The dataset is intentionally tiny and synthetic.

The notebook generates `bug_train.jsonl` and `bug_test.jsonl` from 10 examples using an 80/20 split (8 training examples and 2 test examples).

## Generate the dataset locally

Install dependencies first, then run:

```bash
python -m pip install -r requirements.txt
python src/generate_dataset.py
```

This writes `bug_train.jsonl` and `bug_test.jsonl` in the repository root. The notebook also contains its own dataset-generation cells.

## Run the standalone Gradio app

The app needs a trained LoRA adapter. After running the notebook's adapter-saving cell, put the resulting `final_adapter` directory at `bug_explanation_lora/final_adapter` in the repository root, or point `LORA_ADAPTER_PATH` to the adapter directory.

```bash
python -m pip install -r requirements.txt
python src/app.py
```

The app loads the base model and the saved adapter. The base model may require a first-time internet download and sufficient RAM/VRAM. GPU-specific PyTorch installation can depend on your operating system and CUDA version. The Gradio app runs locally by default; do not expose it publicly without considering privacy and resource use.

## Example test cases

### 1. Off-by-one / invalid list index

```python
numbers = [10, 20, 30]
for i in range(len(numbers) + 1):
    print(numbers[i])
```

Expected issue to look for: the final loop iteration uses an index outside the list's valid range. A typical correction is to iterate over `range(len(numbers))` or directly over the list.

### 2. Division by zero

```python
def divide(a, b):
    return a / b

print(divide(10, 0))
```

Expected issue to look for: the function does not handle a zero divisor. A suitable fix depends on the program's intended behavior.

These are reference cases, not claims that the model always diagnoses them correctly.

## Results and evaluation

See [results/results.md](results/results.md) for the evaluation procedure and [results/evaluation_results.csv](results/evaluation_results.csv) for a blank recording template.

Record the actual model response for each test case. Review whether it:
- identifies the actual bug,
- explains the cause correctly,
- suggests a syntactically plausible and appropriate fix.

Do not report accuracy, loss, or other numerical results unless they come from an actual run. The held-out test split contains only two examples, so it is not sufficient to establish general reliability.

## Screenshots

The `screenshots/` folder is prepared, but genuine screenshots have not yet been committed. After launching the demo, capture:
- the Gradio interface,
- a representative bug input and its generated response,
- another distinct test case and its response.

Save the images in `screenshots/` and add them to this section. Do not use mockups as evidence of a real model run.

## Limitations

- Small synthetic examples may not represent real code defects.
- A two-example test set is far too small for robust performance claims.
- Generated code can be incorrect, incomplete, or unsafe to run.
- Training loss is not the same as debugging accuracy.
- Review suggested fixes before using them.

## Future improvements

- Add a larger, diverse, manually reviewed dataset.
- Keep training, validation, and test data separate.
- Evaluate with a documented rubric and executable unit tests.
- Compare base-model and LoRA outputs on the same held-out examples.
- Record package versions, training configuration, and actual results.
- Add genuine screenshots from the running interface.
