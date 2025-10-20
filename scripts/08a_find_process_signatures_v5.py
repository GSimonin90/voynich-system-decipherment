import re
import json
import sys
from collections import Counter, defaultdict

# --- CONFIGURATION ---
FULL_TRANSLATION_FILE = "voynich_full_translation_v2_FINAL.txt"
SECTION_MAP_FILE = "section_map.json"
TARGET_SECTIONS = ["Balneological", "Herbal"]  # Analyze multiple sections
OUTPUT_FILE = "process_finder_v5_output.txt"  # Output file for results

# --- PROCESS SIGNATURES (Refined based on partial matches) ---
PROCESS_SIGNATURES = {
    "POTENTIAL CALCINATION": [
        r"Heat/Energy.*",  # Matches "Heat/Energy/Active Principle"
        r"Body/Primordial Matter|Component/Part of"  # Relaxed to include frequent term
    ],
    "POTENTIAL CALCINATION (alt)": [
        r"Heat/Energy.*",
        r"Salt/Fixed Principle"
    ],
    "POTENTIAL SUBLIMATION": [
        r"Heat/Energy.*",
        r"Subtle Property/Emanation",
        r"Product/Result|Action/Manifestation"  # Relaxed to include frequent term
    ],
    "POTENTIAL SUBLIMATION (alt)": [
        r"Heat/Energy.*",
        r"Subtle Property/Emanation",
        r"Essence/Distillate"
    ],
    "POTENTIAL COOBATION (Repetition)": [
        r"\(Many/Sequential\)",
        r"Essence/Distillate"
    ],
    "POTENTIAL PREPARATION (General)": [
        r"Heat/Energy.*",
        r"Substance \(Prepared\)"
    ],
    "VITAL PROCESS": [  # Based on frequent concepts
        r"Vital Principle",
        r"Action/Manifestation"
    ],
    "POTENT INFLUENCE": [  # Based on frequent concepts
        r"Potency/Danger",
        r"Action/Manifestation|Cycle/Cosmos"
    ],
    "PREPARATION OF ESSENCES": [  # Refined signature
        r"Substance \(Prepared\)",
        r"Essence/Distillate"
    ],
    "ENERGETIC TRANSFORMATION": [  # Refined signature
        r"Heat/Energy.*",
        r"Cycle/Cosmos"
    ]
}

def find_process_benchmarks():
    """
    Analyzes the full translation to find paragraphs that match
    known iatrochemical process signatures in the target sections.
    Saves results to a text file with statistical summary per section.
    """
    # Initialize output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Starting Process Benchmark Hunt in {', '.join(TARGET_SECTIONS)} sections...\n\n")

    # --- Step 1: Load Section Map ---
    try:
        with open(SECTION_MAP_FILE, 'r', encoding='utf-8') as f:
            section_map = json.load(f)
    except FileNotFoundError:
        error_msg = f"ERROR: Section map file '{SECTION_MAP_FILE}' not found.\n"
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(error_msg)
        print(error_msg)
        return
    except json.JSONDecodeError:
        error_msg = f"ERROR: Invalid JSON in '{SECTION_MAP_FILE}'.\n"
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(error_msg)
        print(error_msg)
        return

    # Debug: Print section map details for each target section
    for section in TARGET_SECTIONS:
        section_paragraphs = [k for k, v in section_map.items() if v == section]
        debug_msg = f"DEBUG: Found {len(section_paragraphs)} paragraphs in '{section}' section: {section_paragraphs[:10]}...\n"
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(debug_msg)
        print(debug_msg)

    # --- Step 2: Load and Analyze Translation File ---
    try:
        with open(FULL_TRANSLATION_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        error_msg = f"ERROR: Translation file '{FULL_TRANSLATION_FILE}' not found.\n"
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(error_msg)
        print(error_msg)
        return
    
    current_paragraph_index = 0
    matches_found = defaultdict(Counter)  # Track matches per signature per section
    current_original = ""
    partial_matches = defaultdict(list)  # Partial matches per section

    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write("Scanning translation file for signatures...\n\n")
    
    for line in lines:
        line = line.strip()
        
        # Store the original line when we see it
        if line.startswith("Original:"):
            current_original = line
            continue
            
        # Process the translation line
        if line.startswith("Translation:"):
            # Get the section for this paragraph
            current_section = section_map.get(str(current_paragraph_index), "Unknown")
            
            # Check if this paragraph is in one of the target sections
            if current_section in TARGET_SECTIONS:
                translation_text = line.lower()  # Case-insensitive matching
                
                # Check this translation against all signatures
                for process_name, keywords in PROCESS_SIGNATURES.items():
                    # Check if ALL keywords for this signature are in the line
                    if all(any(re.search(keyword.lower(), translation_text) for keyword in kw.split("|")) for kw in keywords):
                        match_msg = "="*80 + "\n"
                        match_msg += f"  MATCH FOUND: {process_name} (Section: {current_section})\n"
                        match_msg += f"  Paragraph Index: {current_paragraph_index}\n"
                        match_msg += "="*80 + "\n"
                        match_msg += f"{current_original}\n"
                        match_msg += f"{line}\n\n"
                        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                            f.write(match_msg)
                        matches_found[current_section][process_name] += 1
                    else:
                        # Check for partial matches (at least one keyword)
                        matched_keywords = []
                        for kw in keywords:
                            for keyword in kw.split("|"):
                                if re.search(keyword.lower(), translation_text):
                                    matched_keywords.append(keyword)
                                    break
                        if matched_keywords:
                            partial_matches[current_section].append((current_paragraph_index, process_name, matched_keywords, line))
            
            # Increment paragraph index *after* processing the translation line
            current_paragraph_index += 1
            
    # Write summary and partial matches
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(f"Benchmark Hunt Complete. Found {sum(sum(c.values()) for c in matches_found.values())} potential process descriptions.\n")
        f.write("\nStatistical Summary of Matches by Signature per Section:\n")
        for section in TARGET_SECTIONS:
            if matches_found[section]:
                f.write(f"\nSection: {section}\n")
                for process_name, count in matches_found[section].most_common():
                    f.write(f"  - {process_name}: {count} matches\n")
            else:
                f.write(f"\nSection: {section} - No complete matches found.\n")
            
        if any(partial_matches.values()):
            f.write("\nPartial Matches (paragraphs with at least one keyword, limited to 10 per section):\n")
            for section in TARGET_SECTIONS:
                section_partial_matches = partial_matches[section]
                if section_partial_matches:
                    f.write(f"\nSection: {section}\n")
                    partial_counts = Counter((idx, proc) for idx, proc, _, _ in section_partial_matches)
                    for (idx, proc), count in partial_counts.most_common(10):  # Limit to 10 per section
                        matched_kws = next(mk for i, p, mk, _ in section_partial_matches if i == idx and p == proc)
                        translation = next(t for i, p, _, t in section_partial_matches if i == idx and p == proc)
                        f.write(f"Paragraph {idx}: {proc} - Matched: {', '.join(matched_kws)}\n")
                        f.write(f"Translation: {translation}\n\n")
    
    print(f"✅ Output saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    find_process_benchmarks()