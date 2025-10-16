# The Voynich System: A Functional Decipherment

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

This repository contains the full codebase, data, and publications for the final phase of a three-part research project on the Voynich Manuscript's language. The research culminates in a complete functional decipherment of the manuscript's underlying logical and grammatical system.

---

## Research Papers

This project has resulted in three publications which build upon each other and should be read in sequence.

### Paper 1: Experimental Verification of the Voynich Manuscript's Artificial Language Hypothesis
* **Description:** This foundational paper uses a generative LSTM model to prove that the manuscript's language is artificial and rule-based, paving the way for further analysis.
* **Publication:** Zenodo. [![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.17345194-blue)](https://doi.org/10.5281/zenodo.17345194)

### Paper 2: From Grammar to Meaning: A Computational and Historical Framework for Decoding the Voynich Manuscript
* **Description:** This second paper reverse-engineers the manuscript's grammar and decodes its core conceptual system by linking it to medieval astrological frameworks.
* **Publication:** Zenodo. [![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.17345195-blue)](https://doi.org/10.5281/zenodo.17345195)
* *(Note: The code and data for Papers 1 & 2 are archived in the original repository: [voynich-generative-analysis](https://github.com/GSimonin90/voynich-generative-analysis))*

### Paper 3: The Voynich System: A Functional Grammar and Logical Framework for an Artificial Knowledge Language
* **Description:** This final paper deciphers the complete logical syntax (Connectors), morphology (Prefixes/Suffixes as category/case markers), and validates the entire system by solving the puzzle of Currier's Dialects with quantitative data.
* **Publication:** Zenodo. [![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.17345196-blue)](https://doi.org/10.5281/zenodo.17345196)

---

## Repository Structure

* `/scripts/`: Contains the complete Python analysis suite, with scripts numbered in the recommended order of execution.
* `/data/`: Contains all the necessary input files (`voynich.txt`, `roots.txt`, `prefixes.txt`, `suffixes.txt`).
* `Voynich_Analysis_Pipeline.ipynb`: A Jupyter Notebook that provides a step-by-step, executable guide through the entire analysis pipeline. **This is the recommended way to reproduce the results.**
* `The_Voynich_System.pdf`: The final research paper (same as the Zenodo publication).
* `appendix_C_chart.png`: The chart generated for Appendix C of the paper.
* `requirements.txt`: A list of all Python dependencies required to run the scripts.

---

## How to Replicate the Experiments

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/GSimonin90/voynich-system-decipherment.git](https://github.com/GSimonin90/voynich-system-decipherment.git)
    cd voynich-system-decipherment
    ```
2.  **Set Up the Environment:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate
    pip install -r requirements.txt
    ```
3.  **Explore the Pipeline:** The most straightforward way to reproduce the results is to open and run the cells sequentially in **`Voynich_Analysis_Pipeline.ipynb`**. Alternatively, you can run the Python scripts in the `/scripts` directory in their numbered order from your terminal.

---

## Acknowledgements

This research was conducted in collaboration with Gemini, a large language model from Google. The human author defined all research hypotheses, directed the experimental phases, executed and debugged all code, and is solely responsible for the final interpretation of the results. The AI served as advanced tool for code generation, and structuring of the research papers.

---

## License

This project is licensed under the MIT License.
