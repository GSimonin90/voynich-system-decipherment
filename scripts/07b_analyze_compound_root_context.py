import re
import json
from collections import Counter, defaultdict
import sys

# --- CONFIGURATION ---
VOYNICH_FILE = "voynich_ready_nlp.txt" # Our clean ground truth
SECTION_MAP_FILE = "section_map.json"
OUTPUT_REPORT_FILE = "compound_root_context_report.txt"

# --- TARGET: The 20 new compound roots we added ---
# (Copied from translate_folio_EXPANDED_DICT_v1.py)
TARGET_ROOTS = [
    "qoky", "chdy", "qoty", "chody", "shody", "qoteey", "choky", "chos",
    "okody", "qotam", "okees", "qotody", "qokl", "qokody", "shos",
    "otody", "shoky", "okchd", "shok", "qoly"
]
CONTEXT_WINDOW = 3 # Words before/after
MIN_FREQ = 2       # Minimum frequency to report context word

# --- DICTIONARY (For context reference ONLY) ---
# [Dictionary v3.1 identical to translate_folio_EXPANDED_DICT_v1.py, omitted for brevity]
CONCEPTUAL_DICTIONARY = {
    # Radici Originali (v3.0)
    "ro": "Essence/Distillate (Mercury)", "tai": "Balance/Order", "ek": "Group/Set", "et": "Root/Origin", "eke": "Structure/Node", "yk": "Complex Root/Rhizome", "eo": "Celestial Quality", "al": "Igneous/Luminous Quality", "ot": "Heat/Energy/Active Principle", "y": "Subtle Property/Emanation", "or": "Cycle/Cosmos", "pch": "Process/Action", "ar": "Quality/Property/Aspect", "ka": "Action/Manifestation", "ke": "Component/Part of", "aii": "Vital Principle (Jupiter)", "kai": "Vital Principle (Specific)", "da": "Vital Principle (Essence of)", "ol": "Potency/Danger (Mars)", "kch": "Structuring Principle (Saturn)", "ckh": "Internal Structure", "teo": "Harmonic Principle (Venus)", "che": "Substance (Generic)", "cho": "Substance (Specific)", "she": "Substance (Prepared)", "lk": "Salt/Fixed Principle", "cth": "Body/Primordial Matter", "tch": "Material Form", "ra": "Ingredient", "ara": "Compound/Mixture", "pche": "Product/Result", "lche": "Type of Astral Influence", "lshe": "Class of Emanation",
    "ed": "[particle]", "i": "[particle]", # Ignored particles
    "s": "is", "r": "possesses", "l": "is a type of", "d": "is defined as", "f": "is connected to", "t": "relates to", "k": "is fixed in", "p": "results in",
    # --- NUOVE RADICI COMPOSTE (dall'analisi delle violazioni v1.0) ---
    "qoky": "Specific Fixation/Process", "chdy": "Defined Substance (Astro)", "qoty": "Specific Relation/Aspect (Proc)", "chody": "Defined Substance/Class (Pharm)", "shody": "Defined Prepared Substance", "qoteey": "Specific Property (Recipe)", "choky": "Fixed Substance (Herbal)", "chos": "Substantial Essence", "okody": "Defined Celestial State", "qotam": "Specific Influence (Object)", "okees": "Current Celestial State", "qotody": "Specific Defined Class (Pharm)", "qokl": "Specific Type of Solid", "qokody": "Specific Defined Fixed Element", "shos": "Prepared Essence", "otody": "Defined Active State", "shoky": "Prepared Fixed Element", "okchd": "Defined Structural State", "shok": "Fixed Prepared Substance", "qoly": "Specific Potency/Agent",
}


def analyze_compound_context():
    """
    Analyzes the context (preceding/succeeding words and section)
    for the newly defined compound roots.
    """
    print("Starting Context Analysis for Compound Roots...")

    # --- Step 1: Load Section Map ---
    try:
        with open(SECTION_MAP_FILE, 'r', encoding='utf-8') as f:
            section_map = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Section map file '{SECTION_MAP_FILE}' not found.")
        return

    # --- Step 2: Read Clean File ---
    try:
        with open(VOYNICH_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Clean file '{VOYNICH_FILE}' not found.")
        return

    # --- Step 3: Collect Context Data ---
    print("Scanning text and collecting context...")
    context_data = defaultdict(lambda: {
        'before': Counter(),
        'after': Counter(),
        'sections': Counter(),
        'count': 0
    })
    target_set = set(TARGET_ROOTS) # Faster lookup

    for i, line in enumerate(lines):
        words = line.strip().split()
        n = len(words)
        if n == 0: continue

        current_section = section_map.get(str(i), "Unknown")

        for j, word in enumerate(words):
            if word in target_set:
                root_data = context_data[word]
                root_data['count'] += 1
                if current_section != "Unknown":
                    root_data['sections'][current_section] += 1

                # Collect words before
                start = max(0, j - CONTEXT_WINDOW)
                for k in range(start, j):
                    root_data['before'][words[k]] += 1

                # Collect words after
                end = min(n, j + 1 + CONTEXT_WINDOW)
                for k in range(j + 1, end):
                    root_data['after'][words[k]] += 1

    # --- Step 4: Generate Report ---
    print(f"Generating report file '{OUTPUT_REPORT_FILE}'...")
    with open(OUTPUT_REPORT_FILE, 'w', encoding='utf-8') as f_out:
        f_out.write("="*80 + "\n")
        f_out.write("       CONTEXT ANALYSIS REPORT - COMPOUND ROOTS (v1)\n")
        f_out.write("="*80 + "\n")
        f_out.write(f"Analyzed context for {len(TARGET_ROOTS)} potential compound roots.\n\n")

        # Sort roots by frequency for the report
        sorted_roots = sorted(TARGET_ROOTS, key=lambda r: context_data[r]['count'], reverse=True)

        for root in sorted_roots:
            data = context_data[root]
            total_count = data['count']
            if total_count == 0: continue # Skip roots not found

            # Get current hypothesized meaning
            meaning = CONCEPTUAL_DICTIONARY.get(root, "Meaning Hypothesis Missing")

            f_out.write(f"\n--- Compound Root: '{root}' ---\n")
            f_out.write(f"  Hypothesized Meaning: {meaning}\n")
            f_out.write(f"  Total Occurrences: {total_count}\n")

            # Dominant Section
            dominant_section = data['sections'].most_common(1)
            if dominant_section:
                f_out.write(f"  Dominant Section: {dominant_section[0][0]} ({dominant_section[0][1]} times)\n")
            else:
                f_out.write("  Dominant Section: N/A (Appears only outside mapped sections?)\n")

            # Context Words
            before_context = [f"'{w}' ({c})" for w, c in data['before'].most_common(5) if c >= MIN_FREQ]
            f_out.write(f"  Most Common Preceding ({CONTEXT_WINDOW} words, min freq {MIN_FREQ}): "
                        + (", ".join(before_context) or "None frequent enough") + "\n")

            after_context = [f"'{w}' ({c})" for w, c in data['after'].most_common(5) if c >= MIN_FREQ]
            f_out.write(f"  Most Common Succeeding ({CONTEXT_WINDOW} words, min freq {MIN_FREQ}): "
                        + (", ".join(after_context) or "None frequent enough") + "\n")

        f_out.write("\n\n" + "="*80 + "\n")
        f_out.write("                         END OF REPORT\n")
        f_out.write("="*80 + "\n")

    print(f"✅ Context analysis report saved to '{OUTPUT_REPORT_FILE}'.")

if __name__ == "__main__":
    analyze_compound_context()