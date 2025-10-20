import re
from collections import Counter
import csv

# ==============================================================================
#                 VOYNICH CONCEPTUAL DICTIONARY (v3.0 - FINAL)
# ==============================================================================
CONCEPTUAL_DICTIONARY = {
    "ro": "Essence/Distillate (Mercury)", "tai": "Balance/Order", "ek": "Group/Set", "et": "Root/Origin", "eke": "Structure/Node", "yk": "Complex Root/Rhizome", "eo": "Celestial Quality", "al": "Igneous/Luminous Quality", "ot": "Heat/Energy/Active Principle", "y": "Subtle Property/Emanation", "or": "Cycle/Cosmos", "pch": "Process/Action", "ar": "Quality/Property/Aspect", "ka": "Action/Manifestation", "ke": "Component/Part of", "aii": "Vital Principle (Jupiter)", "kai": "Vital Principle (Specific)", "da": "Vital Principle (Essence of)", "ol": "Potency/Danger (Mars)", "kch": "Structuring Principle (Saturn)", "ckh": "Internal Structure", "teo": "Harmonic Principle (Venus)", "che": "Substance (Generic)", "cho": "Substance (Specific)", "she": "Substance (Prepared)", "lk": "Salt/Fixed Principle", "cth": "Body/Primordial Matter", "tch": "Material Form", "ra": "Ingredient", "ara": "Compound/Mixture", "pche": "Product/Result", "lche": "Type of Astral Influence", "lshe": "Class of Emanation",
}

# --- System Constants ---
ALL_ROOTS = sorted(list(CONCEPTUAL_DICTIONARY.keys()), key=len, reverse=True)
# Define the folio ranges for each thematic section
SECTION_MAP = {
    "Herbal": (1, 66),
    "Astrological": (67, 73),
    "Balneological": (75, 84),
    "Pharmacological": (87, 102),
    "Recipes": (103, 116),
}

def get_section_from_folio(folio_str):
    """Determines the thematic section from a folio string like 'f73r'."""
    match = re.search(r'(\d+)', folio_str)
    if not match:
        return "Unknown"
    
    folio_num = int(match.group(1))
    for section, (start, end) in SECTION_MAP.items():
        if start <= folio_num <= end:
            return section
    return "Unknown"

def parse_word_for_root(word):
    """Extracts the longest possible root from a given word."""
    for root in ALL_ROOTS:
        if root in word:
            return root
    return None

def analyze_thematic_lift(input_file, output_csv_file):
    """
    Performs a full thematic analysis of the Voynich manuscript, calculating lift scores
    for each key root in each section and saving the results to a CSV file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Data storage
    section_word_counts = {name: 0 for name in SECTION_MAP}
    section_root_freqs = {name: Counter() for name in SECTION_MAP}
    total_word_count = 0
    total_root_freqs = Counter()

    current_folio = ""
    current_section = "Unknown"

    print("Step 1: Reading manuscript and counting frequencies...")
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line: continue

        # Check for folio tags
        if cleaned_line.startswith("<") and cleaned_line.endswith(">"):
            current_folio = cleaned_line.strip("<>")
            current_section = get_section_from_folio(current_folio)
            continue
        
        if current_section != "Unknown":
            words = cleaned_line.split()
            for word in words:
                total_word_count += 1
                section_word_counts[current_section] += 1
                root = parse_word_for_root(word)
                if root:
                    total_root_freqs[root] += 1
                    section_root_freqs[current_section][root] += 1
    
    print("Step 2: Calculating lift scores...")
    results = []
    header = ["Root", "Concept", "Total_Freq"] + [f"Lift_{section}" for section in SECTION_MAP]

    for root, total_freq in total_root_freqs.items():
        if total_freq < 10: continue # Ignore very rare roots for cleaner results

        # Overall probability of the root
        prob_root_total = total_freq / total_word_count
        
        row = {
            "Root": root,
            "Concept": CONCEPTUAL_DICTIONARY.get(root, "N/A"),
            "Total_Freq": total_freq
        }

        for section in SECTION_MAP:
            # Probability of the root within this specific section
            if section_word_counts[section] > 0:
                prob_root_in_section = section_root_freqs[section][root] / section_word_counts[section]
            else:
                prob_root_in_section = 0

            # Lift score calculation
            if prob_root_total > 0:
                lift = prob_root_in_section / prob_root_total
            else:
                lift = 0
            
            row[f"Lift_{section}"] = f"{lift:.2f}"
        
        results.append(row)

    # Sort results by the most frequent roots
    results.sort(key=lambda x: x["Total_Freq"], reverse=True)

    print(f"Step 3: Saving results to '{output_csv_file}'...")
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(results)

    print("\nAnalysis complete. The results are ready for review.")


if __name__ == "__main__":
    VOYNICH_TEXT_FILE = "voynich_final_formatted_complete.txt"
    ANALYSIS_OUTPUT_FILE = "thematic_analysis_results.csv"
    
    analyze_thematic_lift(VOYNICH_TEXT_FILE, ANALYSIS_OUTPUT_FILE)
    
    print(f"\nThematic analysis has been saved to '{ANALYSIS_OUTPUT_FILE}'.")
    print("You can open this file with any spreadsheet program (like Excel, Google Sheets) to view the results.")