# Results and evaluation

**Status: not yet populated with verified run results.** No model accuracy or performance claim is made in this repository until actual outputs are reviewed.

## How to record results

1. Run the notebook through the Gradio demo, or start the standalone app after placing the trained adapter at the expected path.
2. Test the same input snippets consistently.
3. Paste the actual model response into `evaluation_results.csv`.
4. Mark diagnosis and fix as `Yes`, `Partial`, or `No` after manually reviewing the response.
5. Capture genuine screenshots of the running interface and representative outputs for the `screenshots/` folder.

The current synthetic dataset contains only 10 examples, with an 80/20 train/test split. This is a small educational demonstration, not a robust benchmark. Do not treat training loss alone as debugging accuracy.
