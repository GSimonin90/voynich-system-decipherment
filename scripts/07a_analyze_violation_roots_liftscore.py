import re
from collections import Counter, defaultdict
import os
import csv
import math # Not strictly needed for lift, but good practice
import json

# --- CONFIGURATION ---
VOYNICH_FILE = "voynich_ready_nlp.txt"
SECTION_MAP_FILE = "section_map.json"
OUTPUT_REPORT_CSV = "violation_lift_score_report.csv" # This is the file it generates

# --- System Constants (from translate_refined_affixes_v5.py / previous analyses) ---
CONNECTORS = ['s', 'r', 'l', 'd', 'f', 't', 'k', 'p']
SIGNIFICANT_PREFIXES = ['qo', 'ok', 'ch', 'sh', 'ot']
# Base roots needed to identify violations correctly
ALL_ROOTS_SET = set([ # Using a set for faster lookup in parser
    "ro", "tai", "ek", "et", "eke", "yk", "eo", "al", "ot", "y", "or", "pch",
    "ar", "ka", "ke", "aii", "kai", "da", "ol", "kch", "ckh", "teo", "che",
    "cho", "she", "lk", "cth", "tch", "ra", "ara", "pche", "lche", "lshe",
    "ed", "i", "s", "r", "l", "d", "f", "t", "k", "p"
])
# Need sorted list for parsing logic if not using set directly in complex checks
ALL_ROOTS_SORTED = sorted(list(ALL_ROOTS_SET), key=len, reverse=True)

# --- Parser Class (Simplified for violation detection) ---
class WordParser:
    """
    Parses a word to identify prefix and potential root,
    then checks if it's a violation (Prefix + Connector).
    """
    def __init__(self, original_word):
        self.original = original_word
        self.prefix = None
        self.potential_root = None # What remains after stripping prefix
        self.is_violation = False
        self.parse_and_check()

    def parse_and_check(self):
        temp_word = self.original
        prefix_found = None
        remainder = temp_word # Start with the full word

        # 1. Attempt to strip a known prefix
        for p in SIGNIFICANT_PREFIXES:
            if temp_word.startswith(p):
                current_remainder = temp_word[len(p):]
                # A prefix is only valid if the remainder is not itself a known root
                # AND the remainder actually exists
                if len(current_remainder) > 0 and current_remainder not in ALL_ROOTS_SET:
                    prefix_found = p
                    remainder = current_remainder
                    break # Found the longest matching prefix

        # 2. Store the prefix and the remaining part
        self.prefix = prefix_found
        self.potential_root = remainder

        # 3. Check for violation: Was a prefix found AND is the remainder a connector?
        if self.prefix is not None and self.potential_root in CONNECTORS:
            self.is_violation = True


def analyze_violation_roots():
    """
    Finds all unique "violation words" and then performs a
    thematic lift score analysis on them.
    """
    print(f"Starting Violation Root Analysis on '{VOYNICH_FILE}'...")

    # --- Step 1: Read clean file ---
    try:
        with open(VOYNICH_FILE, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"ERROR: Clean file '{VOYNICH_FILE}' not found.")
        return
    all_words = text.split()
    unique_words = set(all_words)
    total_word_count = len(all_words)

    # --- Step 2: Identify all "Violation Words" ---
    violation_words = set()
    for word_str in unique_words:
        parsed = WordParser(word_str)
        if parsed.is_violation:
            # Add the original word string that caused the violation
            violation_words.add(word_str)

    if not violation_words:
        print("No violation words found matching the Prefix+Connector pattern.")
        return

    violation_words_list = sorted(list(violation_words))
    print(f" -> Identified {len(violation_words_list)} unique 'violation words' to analyze.")

    # --- Step 3: Load Section Map ---
    try:
        with open(SECTION_MAP_FILE, 'r', encoding='utf-8') as f:
            section_map = json.load(f) # keys are "0", "1", ...
    except FileNotFoundError:
        print(f"ERROR: Section map file '{SECTION_MAP_FILE}' not found.")
        return

    # --- Step 4: Count Frequencies (Globally and by Section) ---
    print("Counting frequencies for violation words...")
    section_word_counts = defaultdict(int)      # Total words per section
    section_root_freqs = defaultdict(Counter) # Freq of each violation word per section
    total_root_freqs = Counter()                # Global freq of each violation word

    # Re-read the file line by line to map words to sections accurately
    try:
        with open(VOYNICH_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("ERROR: Could not re-read clean file.")
        return

    paragraph_index = 0
    for line in lines:
        words_in_line = line.strip().split()
        if not words_in_line:
            continue

        # Get section for this line (paragraph index)
        current_section = section_map.get(str(paragraph_index), "Unknown")
        if current_section == "Unknown":
            paragraph_index += 1
            continue # Skip paragraphs not in a known section

        # Count total words in this section
        section_word_counts[current_section] += len(words_in_line)

        # Count occurrences of violation words in this section
        for word in words_in_line:
            if word in violation_words_list: # Check if the word is one of our targets
                total_root_freqs[word] += 1
                section_root_freqs[current_section][word] += 1

        paragraph_index += 1

    # --- Step 5: Calculate Lift and Save CSV ---
    print("Calculating Lift Scores...")
    results = []
    # Define header based on known sections + Root + Freq
    sections = sorted([s for s in section_word_counts.keys() if s != "Unknown"])
    header = ["ViolationRoot", "TotalFreq"] + [f"Lift_{section}" for section in sections]

    for root, total_freq in total_root_freqs.items():
        # Optional: Filter out very rare words for cleaner results
        if total_freq < 2: continue

        # Calculate P(Root) globally
        prob_root_total = total_freq / total_word_count if total_word_count > 0 else 0

        row = {
            "ViolationRoot": root,
            "TotalFreq": total_freq
        }

        # Calculate Lift for each section
        for section in sections:
            section_total_words = section_word_counts[section]
            if section_total_words > 0:
                # Calculate P(Root | Section)
                prob_root_in_section = section_root_freqs[section][root] / section_total_words
            else:
                prob_root_in_section = 0

            # Calculate Lift = P(Root | Section) / P(Root)
            if prob_root_total > 0:
                lift = prob_root_in_section / prob_root_total
            else:
                lift = 0 # Avoid division by zero if root probability is somehow zero

            row[f"Lift_{section}"] = f"{lift:.2f}" # Format to 2 decimal places

        results.append(row)

    # Sort results by the most frequent violation words
    results.sort(key=lambda x: x["TotalFreq"], reverse=True)

    print(f"Saving lift score report to '{OUTPUT_REPORT_CSV}'...")
    try:
        with open(OUTPUT_REPORT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(results)
    except Exception as e:
        print(f"ERROR writing CSV file: {e}")
        return

    print("✅ Violation root analysis complete.")

if __name__ == "__main__":
    analyze_violation_roots()