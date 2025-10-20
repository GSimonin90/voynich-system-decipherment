import re
from collections import Counter
import sys

# --- CONFIGURATION ---
VOYNICH_FILE = "voynich_ready_nlp.txt" # The clean source file
OUTPUT_REPORT_FILE = "unknown_word_report_v2_DICT_COMPARE.txt" # New report file
TOP_N = 50 # How many top unknown words to report

# --- DICTIONARY v3.1 (To get the list of KNOWN roots) ---
CONCEPTUAL_DICTIONARY = {
    # Original Roots (v3.0)
    "ro": "Essence/Distillate (Mercury)", "tai": "Balance/Order", "ek": "Group/Set", "et": "Root/Origin", "eke": "Structure/Node", "yk": "Complex Root/Rhizome", "eo": "Celestial Quality", "al": "Igneous/Luminous Quality", "ot": "Heat/Energy/Active Principle", "y": "Subtle Property/Emanation", "or": "Cycle/Cosmos", "pch": "Process/Action", "ar": "Quality/Property/Aspect", "ka": "Action/Manifestation", "ke": "Component/Part of", "aii": "Vital Principle (Jupiter)", "kai": "Vital Principle (Specific)", "da": "Vital Principle (Essence of)", "ol": "Potency/Danger (Mars)", "kch": "Structuring Principle (Saturn)", "ckh": "Internal Structure", "teo": "Harmonic Principle (Venus)", "che": "Substance (Generic)", "cho": "Substance (Specific)", "she": "Substance (Prepared)", "lk": "Salt/Fixed Principle", "cth": "Body/Primordial Matter", "tch": "Material Form", "ra": "Ingredient", "ara": "Compound/Mixture", "pche": "Product/Result", "lche": "Type of Astral Influence", "lshe": "Class of Emanation",
    "ed": "[particle]", "i": "[particle]",
    "s": "is", "r": "possesses", "l": "is a type of", "d": "is defined as", "f": "is connected to", "t": "relates to", "k": "is fixed in", "p": "results in",
    # --- NEW COMPOUND ROOTS (v1.0) ---
    "qoky": "Specific Fixation/Process", "chdy": "Defined Component/Aspect", "qoty": "Specific Relation/Aspect (Proc)", "chody": "Defined Substance/Type", "shody": "Defined Prepared Substance", "qoteey": "Specific Property (Recipe)", "choky": "Fixed Substance (Herbal)", "chos": "Substantial Essence", "okody": "Defined Celestial State", "qotam": "Specific Influence (Object)", "okees": "Current Celestial State", "qotody": "Specific Defined Class (Pharm)", "qokl": "Specific Type of Solid", "qokody": "Specific Defined Fixed Element", "shos": "Prepared Essence", "otody": "Defined Active State (Astro)", "shoky": "Prepared Fixed Element", "okchd": "Defined Structural State", "shok": "Fixed Prepared Substance", "qoly": "Specific Potency/Agent",
}
KNOWN_ROOTS = set(CONCEPTUAL_DICTIONARY.keys()) # Set for faster lookup

# --- Helper to check if a word contains a known root ---
# This helps filter out words that are just known roots + unknown affixes
ALL_ROOTS_SORTED = sorted(list(KNOWN_ROOTS), key=len, reverse=True)
def contains_known_root(word):
    """Checks if a word contains any known root."""
    for root in ALL_ROOTS_SORTED:
        if root in word:
            # Make sure it's not just the root itself if the word IS a root
            if word == root:
                return True # It IS a known root
            # If a known root is INSIDE a longer word, assume it's root+affix for now
            return True
    return False


def analyze_unknowns_v2():
    """
    Scans the source file and identifies words NOT present
    as keys in the current dictionary (v3.1).
    """
    print(f"Starting analysis of unknown words by comparing '{VOYNICH_FILE}' to Dictionary v3.1...")

    try:
        with open(VOYNICH_FILE, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"ERROR: Source file '{VOYNICH_FILE}' not found.")
        return

    all_words = text.split()
    if not all_words:
        print("ERROR: No words found in the source file.")
        return

    unknown_counts = Counter()
    total_unknown_tokens = 0

    print(f" -> Comparing {len(all_words)} total word tokens against {len(KNOWN_ROOTS)} known roots...")

    # Iterate through all words in the text
    for word in all_words:
        # Check 1: Is the word itself a known root?
        if word not in KNOWN_ROOTS:
             # Check 2: Does it contain a known root (likely root+affix)?
             # We want words that are *completely* unknown
             if not contains_known_root(word):
                unknown_counts[word] += 1
                total_unknown_tokens += 1

    total_unique_unknowns = len(unknown_counts)

    print(f" -> Found {total_unknown_tokens} total truly unknown word tokens.")
    print(f" -> Found {total_unique_unknowns} unique truly unknown word types.")

    # --- Generate Report ---
    print(f"Generating report file '{OUTPUT_REPORT_FILE}'...")
    with open(OUTPUT_REPORT_FILE, 'w', encoding='utf-8') as f_out:
        f_out.write("="*80 + "\n")
        f_out.write("     ANALYSIS OF UNKNOWN WORDS (v2 - Dictionary Comparison)\n")
        f_out.write("="*80 + "\n\n")
        f_out.write(f"Scanned file: '{VOYNICH_FILE}'\n")
        f_out.write(f"Compared against: Dictionary v3.1 ({len(KNOWN_ROOTS)} known roots)\n")
        f_out.write(f"Total 'truly unknown' tokens found: {total_unknown_tokens}\n")
        f_out.write(f"Unique 'truly unknown' word types: {total_unique_unknowns}\n\n")

        f_out.write(f"--- Top {TOP_N} Most Frequent Truly Unknown Words ---\n")
        f_out.write("(Words containing known roots, likely root+affix, are excluded)\n\n")

        if not unknown_counts:
             f_out.write("  No truly unknown words found.\n")
        else:
            # Report the top N unknown words and their counts
            for word, count in unknown_counts.most_common(TOP_N):
                f_out.write(f"  - {word} : {count} occurrences\n")

        f_out.write("\n\n" + "="*80 + "\n")
        f_out.write("                         END OF REPORT\n")
        f_out.write("="*80 + "\n")

    print(f"✅ Report on truly unknown words saved to '{OUTPUT_REPORT_FILE}'.")

if __name__ == "__main__":
    analyze_unknowns_v2()