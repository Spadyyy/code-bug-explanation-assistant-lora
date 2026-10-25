"""Generate the small synthetic bug dataset used by the project notebook.

Usage:
    python src/generate_dataset.py

Writes bug_train.jsonl and bug_test.jsonl to the project root. This is a
10-example educational dataset, not a real-world benchmark.
"""
import json
import random
from pathlib import Path

from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
random.seed(42)

EXAMPLES = [
    {"bug": "def add(a, b):\n    return a - b", "explanation": "The function subtracts instead of adding. Replace the minus operator with plus.", "fixed_code": "def add(a, b):\n    return a + b"},
    {"bug": "items = [1, 2, 3]\nprint(items[3])", "explanation": "Python lists use zero-based indexing. A three-element list has valid indices 0, 1, and 2. Use items[2] to access the last element.", "fixed_code": "items = [1, 2, 3]\nprint(items[2])"},
    {"bug": "if x = 5:\n    print('five')", "explanation": "A single equals sign assigns a value and cannot be used for comparison in an if condition. Use == to compare values.", "fixed_code": "if x == 5:\n    print('five')"},
    {"bug": "for i in range(5)\n    print(i)", "explanation": "The for statement is missing a colon at the end of the loop header.", "fixed_code": "for i in range(5):\n    print(i)"},
    {"bug": "def greet(name):\nprint('Hello', name)", "explanation": "The function body must be indented beneath the function definition.", "fixed_code": "def greet(name):\n    print('Hello', name)"},
    {"bug": "name = 'Alex'\nprint(Name)", "explanation": "Python variable names are case-sensitive. Name and name are different identifiers.", "fixed_code": "name = 'Alex'\nprint(name)"},
    {"bug": "numbers = [1, 2, 3]\nnumbers.append[4]", "explanation": "append is a method and must be called with parentheses, not square brackets.", "fixed_code": "numbers = [1, 2, 3]\nnumbers.append(4)"},
    {"bug": "def divide(a, b):\n    return a / b\n\nprint(divide(10, 0))", "explanation": "Dividing by zero raises ZeroDivisionError. Check whether the denominator is zero before dividing.", "fixed_code": "def divide(a, b):\n    if b == 0:\n        raise ValueError('b must not be zero')\n    return a / b"},
    {"bug": "text = 'hello\nprint(text)", "explanation": "The string literal is missing its closing quotation mark.", "fixed_code": "text = 'hello'\nprint(text)"},
    {"bug": "total = 0\nfor n in [1, 2, 3]:\n    total = n\nprint(total)", "explanation": "The loop overwrites total on each iteration instead of accumulating the values. Use total += n.", "fixed_code": "total = 0\nfor n in [1, 2, 3]:\n    total += n\nprint(total)"},
]

def to_record(example):
    prompt = f"Explain the bug in this Python code and suggest a fix:\n```python\n{example['bug']}\n```"
    answer = f"Explanation: {example['explanation']}\n\nCorrected code:\n```python\n{example['fixed_code']}\n```"
    return {**example, "prompt": prompt, "answer": answer}

def write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

def main():
    rows = [to_record(example) for example in EXAMPLES]
    train, test = train_test_split(rows, test_size=0.2, random_state=42)
    write_jsonl(ROOT / "bug_train.jsonl", train)
    write_jsonl(ROOT / "bug_test.jsonl", test)
    print(f"Created {len(train)} training examples and {len(test)} test examples.")
    print("Files: bug_train.jsonl, bug_test.jsonl")

if __name__ == "__main__":
    main()
