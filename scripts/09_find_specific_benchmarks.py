import re
import json
import sys

# --- CONFIGURATION ---
FULL_TRANSLATION_FILE = "voynich_full_translation_v3_IMPROVED.txt"
OUTPUT_REPORT_FILE = "specific_benchmark_report_v1.txt"

# --- BENCHMARK SIGNATURES (Based on Grok's suggestions) ---
# Looking for paragraphs where the *translation* contains ALL keywords in a list
BENCHMARK_SIGNATURES = {
    "POSSIBLE TRIA PRIMA DISCUSSION": [
        "Essence/Distillate (Mercury)", # ro
        "Salt/Fixed Principle",         # lk
        "Potency/Danger (Mars)"         # ol (our proxy for Sulphur)
    ],
    "POSSIBLE QUINTESSENCE/SPIRITUS (Type 1)": [
        "Vital Principle",              # aii/kai/da
        "Essence/Distillate (Mercury)"  # ro
    ],
    "POSSIBLE QUINTESSENCE/SPIRITUS (Type 2)": [
        "Vital Principle",              # aii/kai/da
        "Subtle Property/Emanation"     # y
    ],
    "POSSIBLE DETAILED CALCINATION (Type 1)": [
        "Heat/Energy",                  # ot or al
        "Body/Primordial Matter"        # cth
    ],
    "POSSIBLE DETAILED CALCINATION (Type 2)": [
        "Heat/Energy",                  # ot or al
        "Salt/Fixed Principle"          # lk
    ],
     "POSSIBLE DETAILED CALCINATION (Type 3)": [
        "Igneous/Luminous Quality",     # al
        "Body/Primordial Matter"        # cth
    ],
    "POSSIBLE DETAILED CALCINATION (Type 4)": [
        "Igneous/Luminous Quality",     # al
        "Salt/Fixed Principle"          # lk
    ],
}

# Add aliases for Heat/Energy concept
HEAT_ALIASES = ["Heat/Energy", "Igneous/Luminous Quality"]

def find_specific_benchmarks():
    """
    Analyzes the full translation to find paragraphs that match
    specific iatrochemical concepts suggested by Grok.
    """
    print(f"Starting Specific Benchmark Hunt in '{FULL_TRANSLATION_FILE}'...")

    # --- Step 1: Load Translation File ---
    try:
        with open(FULL_TRANSLATION_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Translation file '{FULL_TRANSLATION_FILE}' not found.")
        return

    current_paragraph_index = 0
    matches_found = 0
    current_original = ""
    total_paragraphs = 0

    # --- Step 2: Analyze Translation Lines ---
    print("Scanning translation file for specific signatures...")
    with open(OUTPUT_REPORT_FILE, 'w', encoding='utf-8') as out_f:
        out_f.write("="*80 + "\n")
        out_f.write("       SPECIFIC IATROCHEMICAL BENCHMARK REPORT (v1)\n")
        out_f.write("="*80 + "\n\n")
        out_f.write(f"Scanning file: '{FULL_TRANSLATION_FILE}'\n")
        out_f.write("Looking for paragraphs matching signatures derived from Grok's historical context.\n\n")

        for line_num, line in enumerate(lines):
            line = line.strip()

            # Store the original line when we see it
            if line.startswith("Original Cleaned:"):
                current_original = line
                continue

            # Process the translation line
            if line.startswith("Translation:"):
                total_paragraphs += 1
                translation_text = line

                # Check this translation against all our signatures
                for benchmark_name, keywords in BENCHMARK_SIGNATURES.items():
                    # Special handling for Heat/Energy aliases
                    match = True
                    for kw in keywords:
                        if kw == "Heat/Energy": # Check for either alias
                            if not any(alias in translation_text for alias in HEAT_ALIASES):
                                match = False; break
                        elif kw == "Igneous/Luminous Quality": # Check for either alias
                             if not any(alias in translation_text for alias in HEAT_ALIASES):
                                 match = False; break
                        elif kw not in translation_text: # Standard keyword check
                            match = False; break

                    # If all keywords (considering aliases) were found
                    if match:
                        out_f.write("="*80 + "\n")
                        out_f.write(f"  MATCH FOUND: {benchmark_name}\n")
                        # Find paragraph number from the preceding "--- Paragraph X ---" line
                        para_num_line = ""
                        for k in range(line_num - 2, max(0, line_num - 5), -1):
                             if lines[k].startswith("--- Paragraph"):
                                 para_num_line = lines[k].strip()
                                 break
                        out_f.write(f"  {para_num_line}\n")
                        out_f.write("="*80 + "\n")
                        out_f.write(f"{current_original}\n")
                        out_f.write(f"{line}\n")
                        out_f.write("\n")
                        matches_found += 1

                current_paragraph_index += 1 # Ensure this increments correctly

        out_f.write("="*80 + "\n")
        out_f.write(f"Scan Complete. Found {matches_found} potential specific benchmark matches in {total_paragraphs} paragraphs.\n")
        out_f.write("="*80 + "\n")

    print(f"\n✅ Specific benchmark search complete. Found {matches_found} matches.")
    print(f"   Results saved to '{OUTPUT_REPORT_FILE}'.")

if __name__ == "__main__":
    find_specific_benchmarks()