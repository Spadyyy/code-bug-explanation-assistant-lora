# Code Bug Explanation Assistant using LoRA

An educational mini-project that fine-tunes `Qwen/Qwen2.5-Coder-0.5B-Instruct` with Low-Rank Adaptation (LoRA) to generate explanations and suggested corrections for buggy Python code.

> **Project status:** prototype/demo. The training dataset is small and synthetic. Outputs may be incorrect; this project is not a production debugging tool or a benchmark of real-world accuracy.

## Project objectives

- Explore parameter-efficient fine-tuning with PEFT/LoRA.
- Build a simple interface where a user can submit buggy Python code.
- Generate a natural-language explanation and a possible correction.
- Compare model outputs on examples and document limitations.

## How it works

1. Load and inspect the example dataset.
2. Prepare prompts and split examples into training and evaluation sets.
3. Load the base code model and configure LoRA adapters.
4. Fine-tune the model.
5. Generate explanations for test snippets.
6. Launch a Gradio interface for interactive experimentation.

## Technology stack

- Python and Google Colab
- Hugging Face Transformers and Datasets
- PEFT (LoRA)
- PyTorch
- Gradio

## Model configuration

- **Base model:** `Qwen/Qwen2.5-Coder-0.5B-Instruct`
- **LoRA rank (r):** 8
- **LoRA alpha:** 16
- **LoRA dropout:** 0.05
- **Target modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj` (as configured in the notebook)

Check the notebook itself for the definitive dataset size, split, training arguments, and current implementation. Do not assume a metric or result that has not been recorded from an actual run.

## Getting started

1. Open `Code_Bug_Explanation_Assistant_Documented.ipynb` in [Google Colab](https://colab.research.google.com/).
2. Choose **Runtime → Change runtime type** and select a GPU if one is available.
3. Run the notebook cells from top to bottom.
4. Test the interface with a few examples, including an off-by-one error and division by zero.
5. Inspect the generated explanations and fixes before treating them as correct.

The notebook may install its own dependencies. `requirements.txt` lists the main packages for reference; GPU-specific PyTorch installation can depend on the runtime.

## Example test cases

### 1. Off-by-one error

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

Expected issue to look for: the function does not handle a zero divisor. A suitable fix depends on the program's intended behavior, such as validating the divisor and returning or raising an appropriate error.

These are reference test cases, not claims that the model always diagnoses them correctly.

## Results and evaluation

Record the outputs from your own run before reporting performance. For each test case, check whether the model:
- identifies the actual bug,
- gives a valid explanation,
- suggests a syntactically plausible fix.

| Test case | Actual observation | Correct diagnosis? | Fix valid? |
|---|---|---|---|
| Off-by-one / list index | Fill in from your run | Yes / No / Partial | Yes / No / Partial |
| Division by zero | Fill in from your run | Yes / No / Partial | Yes / No / Partial |

Do not report accuracy, loss, or other numerical results unless they come from the notebook's actual output. A tiny test set is not enough to establish general reliability.

## Limitations

- Small, synthetic examples may not represent real code defects.
- Performance can vary across bug types and prompts.
- Generated code can be incorrect, incomplete, or unsafe to run.
- Evaluation on a small test split is not evidence of general debugging ability.
- The demo should be treated as an educational experiment; review all suggested fixes.

## Future improvements

- Add a larger, diverse, manually reviewed dataset.
- Keep training, validation, and test sets separate.
- Evaluate with a documented rubric and executable unit tests.
- Compare base-model and LoRA outputs on the same held-out examples.
- Record package versions, training configuration, and actual results.
- Add screenshots of the running interface and representative test outputs.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
└── Code_Bug_Explanation_Assistant_Documented.ipynb
```

If you add screenshots later, place only genuine screenshots from your own run in a `screenshots/` directory and update this README with their paths.
