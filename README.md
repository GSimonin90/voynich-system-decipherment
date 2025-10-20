# The Voynich System: A Functional Decipherment

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

This repository contains the full codebase, data, and analysis pipeline for a multi-phase research project on the Voynich Manuscript's language. The research culminates in a proposed functional decipherment of the manuscript's underlying logical and grammatical system. **The final phase ("Final Test") provides comprehensive validation for this system.**

---

## Research Papers

This project has resulted in **four** publications which build upon each other:

### Paper 1: Experimental Verification of the Voynich Manuscript's Artificial Language Hypothesis
* **Description:** This foundational paper uses a generative LSTM model to demonstrate the artificial and rule-based nature of the manuscript's language.
* **Publication:** Simonin, G. (2025a). Zenodo. [![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.17345194-blue)](https://doi.org/10.5281/zenodo.17345194)
* *(Note: The original code for Paper 1 is archived in the [voynich-generative-analysis](https://github.com/GSimonin90/voynich-generative-analysis) repository)*

### Paper 2: From Grammar to Meaning: A Computational and Historical Framework
* **Description:** This paper reverse-engineers the core grammar and links the conceptual system to medieval astrological frameworks.
* **Publication:** Simonin, G. (2025b). Zenodo. [![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.17360252-blue)](https://doi.org/10.5281/zenodo.17360252)

### Paper 3: The Voynich System: A Functional Grammar and Logical Framework
* **Description:** This paper details the complete logical syntax (Connectors), morphology (Affixes), and validates the system against Currier's Dialects.
* **Publication:** Simonin, G. (2025c). Zenodo. [![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.17371265-blue)](https://doi.org/10.5281/zenodo.17371265)

**### Paper 4 (Final Test): Validation, Application, and Extended Analysis**
* **Description:** This validation phase ("Final Test") rigorously tests the system using statistical linguistics (Entropy, Zipf's Law), syntactic analysis (SVO asymmetry), thematic analysis (Lift Score), content benchmarking (f78r, process signatures), predictive translation (f57v), and comparative analysis (Copiale Cipher, Sefer Yetzirah).
* **Publication:** Simonin, G. (2025d). Zenodo. [![DOI](https://zenodo.org/badge/DOI/YOUR_PAPER_IV_DOI.svg)](https://doi.org/YOUR_PAPER_IV_DOI) <-- *Aggiungi il DOI Zenodo del Paper 4 qui*

---

## Repository Structure

* `/scripts/`: Contains the Python analysis suite.
    * **Previous Work:** Scripts related to Paper 3.
    * **Final Test:** Scripts for the final validation phase (numbered `01_...` to `11_...` for suggested execution order).
* `/data/`: Contains necessary input files:
    * **Previous Work:** `roots.txt`, `prefixes.txt`, `suffixes.txt`.
    * **Final Test:** `voynich.txt` (Source), `voynich_ready_nlp.txt` (Clean Corpus), `section_map.json`, `copiale_english_translation.txt`, `sefer_yetzirah_english.txt`.
* `Voynich_Analysis_Pipeline.ipynb`: A Jupyter Notebook providing a step-by-step guide through the analysis pipeline related to Paper 3. **Recommended for reproducing Paper 3 results.**
* **Root Directory Files:** Contains key outputs from the **Final Test** validation for easy access:
    * **Reports & Data:** `thematic_analysis_results.csv`, `violation_lift_score_report.csv`, `syntax_pattern_report_v2_with_violations.txt`, `process_finder_v5_output.txt`, `specific_benchmark_report_v1.txt`, `compound_root_context_report.txt`, `unknown_word_report_v2_DICT_COMPARE.txt`.
    * **Figures:** `thematic_heatmap.png`, `zipf_plot_Voynich.png`, `zipf_plot_Copiale_Eng.png`, `zipf_plot_Sefer_Yetzirah_Eng.png`, `process_by_section_barchart.png`.
    * **Translations:** `voynich_full_translation_v3_IMPROVED.txt`, `translation_f57v_SYNTH_ADVANCED.txt`, `translation_f78r_FINAL_benchmark.txt`.
    * **Paper:** `The_Voynich_System_Phase_IV.pdf`.
* `requirements.txt`: Python dependencies required for **all scripts** in the repository.
* `appendix_C_chart.png`: Chart for Appendix C of Paper III.
* `LICENSE`: Project license file (MIT).

---

## How to Replicate Experiments

### Paper 3 Analysis (using Notebook)
1.  **Clone & Setup:** Follow steps 1 & 2 below.
2.  **Run Notebook:** Open and run cells sequentially in `Voynich_Analysis_Pipeline.ipynb`.

### Final Test Validation (using Scripts)
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/GSimonin90/voynich-system-decipherment.git](https://github.com/GSimonin90/voynich-system-decipherment.git)
    cd voynich-system-decipherment
    ```
2.  **Set Up the Environment:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate  # On Windows PowerShell
    # source .venv/bin/activate # On Linux/macOS
    pip install -r requirements.txt
    ```
3.  **Run Final Test Analysis Pipeline:**
    * **Crucial First Step:** Run `python scripts/01_generate_clean_data.py` to create necessary files in `data/`.
    * Run other Final Test scripts (`02a_...` onwards) located in `/scripts/`. Input files are expected in `/data/`, outputs will appear in the root directory.

---

## Acknowledgements

This research was conducted independently. The author acknowledges the use of open-access computational tools and datasets. Special thanks to collaborative AI frameworks (ChatGPT, Gemini, Grok) used solely as research assistants for code generation, data visualization, structural editing, and critical feedback during the **Final Test** validation phase. The human author defined all research hypotheses, directed experimental phases, executed and debugged all code, and is solely responsible for the final interpretation of the results.

---

## License

This project is licensed under the **MIT License**.
