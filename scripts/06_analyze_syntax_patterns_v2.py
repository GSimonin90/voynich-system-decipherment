import re
from collections import Counter
import os
import sys

# --- CONFIGURATION ---
VOYNICH_FILE = "voynich_ready_nlp.txt"
OUTPUT_REPORT_FILE = "syntax_pattern_report_v2_with_violations.txt" # New output file

# --- System Constants (from your grammar) ---
CONNECTORS = ['s', 'r', 'l', 'd', 'f', 't', 'k', 'p']
SUBJECT_SUFFIXES = sorted(['y', 'dy', 'ey'], key=len, reverse=True)
OBJECT_SUFFIXES = sorted(['n', 'in', 'm'], key=len, reverse=True)
SIGNIFICANT_PREFIXES = ['qo', 'ok', 'ch', 'sh', 'ot'] # Needed for violation check
ALL_ROOTS = set([
    "ro", "tai", "ek", "et", "eke", "yk", "eo", "al", "ot", "y", "or", "pch",
    "ar", "ka", "ke", "aii", "kai", "da", "ol", "kch", "ckh", "teo", "che",
    "cho", "she", "lk", "cth", "tch", "ra", "ara", "pche", "lche", "lshe",
    "ed", "i", "s", "r", "l", "d", "f", "t", "k", "p"
])
ALL_ROOTS_SORTED = sorted(list(ALL_ROOTS), key=len, reverse=True) # Need sorted list for parser

# --- Simple Parser to check for violations ---
def check_violation(word):
    """Checks if a word matches the Prefix+Connector violation pattern."""
    temp_word = word
    prefix_found = None
    root_found = None

    # Check for prefix
    for p in SIGNIFICANT_PREFIXES:
        if temp_word.startswith(p):
            remainder = temp_word[len(p):]
            if len(remainder) > 0 and remainder not in ALL_ROOTS:
                prefix_found = p
                temp_word = remainder
                break

    # Check if remainder is a connector
    if temp_word in CONNECTORS:
        root_found = temp_word

    return prefix_found is not None and root_found is not None

# --- Updated Role Function ---
def get_grammatical_role_v2(word):
    """
    Assigns a grammatical role, adding a specific 'VIOLATION' category.
    """
    # 0. Check for Violation FIRST
    if check_violation(word):
        return "VIOLATION"

    # 1. Check if it's a Verb (Connector)
    if word in CONNECTORS:
        return "VERB"

    # 2. Check if it's a root that *looks* like a suffix (e.g., 'y')
    if word in ALL_ROOTS:
        return "CONCEPT" # Treat standalone roots like y, s, r as concepts if not violations

    # 3. Check for Subject Suffixes
    for s in SUBJECT_SUFFIXES:
        if word.endswith(s):
            base = word[:-len(s)]
            # Ensure base exists and is not just a root itself
            if base and base not in ALL_ROOTS:
                return "SUBJECT"

    # 4. Check for Object Suffixes
    for s in OBJECT_SUFFIXES:
        if word.endswith(s):
            base = word[:-len(s)]
            if base and base not in ALL_ROOTS:
                return "OBJECT"

    # 5. Default: It's a standard concept word
    return "CONCEPT"


def syntax_pattern_test_v2():
    """
    Analyzes syntax patterns including the 'VIOLATION' role.
    """
    print(f"Starting Syntax Pattern Analysis v2 (with Violations) on '{VOYNICH_FILE}'...")

    # --- Step 1: Read words ---
    try:
        with open(VOYNICH_FILE, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"ERROR: Clean file '{VOYNICH_FILE}' not found.")
        return
    all_words = text.split()
    if len(all_words) < 3: return

    print(f" -> Analyzing {len(all_words)} total words...")

    # --- Step 2: Get roles (using v2 function) ---
    roles = [get_grammatical_role_v2(w) for w in all_words]

    # --- Step 3: Count Patterns ---
    bigram_patterns = Counter(zip(roles[:-1], roles[1:]))
    trigram_patterns = Counter(zip(roles[:-2], roles[1:-1], roles[2:]))
    total_trigrams = sum(trigram_patterns.values())
    total_bigrams = sum(bigram_patterns.values())

    print(" -> Analysis complete. Generating report...")

    # --- Step 4: Generate Report ---
    with open(OUTPUT_REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("       VOYNICH SYNTAX PATTERN ANALYSIS - V2 (with VIOLATION role)\n")
        f.write("="*80 + "\n\n")
        f.write(f"Analyzed {len(all_words)} words, {total_bigrams} bigrams, {total_trigrams} trigrams.\n")
        f.write("Focus: How do 'VIOLATION' words (potential compound roots) behave syntactically?\n\n")

        # --- Trigram Report ---
        f.write("-" * 40 + "\n")
        f.write("  Top 20 Most Frequent Trigram Patterns:\n")
        f.write("-" * 40 + "\n")
        for (r1, r2, r3), count in trigram_patterns.most_common(20):
            pattern = f"{r1}-{r2}-{r3}"
            percent = (count / total_trigrams) * 100
            f.write(f"  {pattern:<30} : {count:<6} occurrences ({percent:.2f}%)\n")

        # --- Bigram Report ---
        f.write("\n" + "-" * 40 + "\n")
        f.write("  Top 20 Most Frequent Bigram Patterns:\n")
        f.write("-" * 40 + "\n")
        for (r1, r2), count in bigram_patterns.most_common(20):
            pattern = f"{r1}-{r2}"
            percent = (count / total_bigrams) * 100
            f.write(f"  {pattern:<30} : {count:<6} occurrences ({percent:.2f}%)\n")

        # --- Specific check for VIOLATION words ---
        f.write("\n\n" + "="*80 + "\n")
        f.write("       BEHAVIOR OF 'VIOLATION' WORDS\n")
        f.write("="*80 + "\n\n")
        
        f.write("Common patterns involving VIOLATION words:\n")
        violation_bigrams = {p: c for p, c in bigram_patterns.items() if "VIOLATION" in p}
        violation_trigrams = {p: c for p, c in trigram_patterns.items() if "VIOLATION" in p}

        f.write("\n--- Bigrams with VIOLATION (Top 10) ---\n")
        for (r1, r2), count in sorted(violation_bigrams.items(), key=lambda item: item[1], reverse=True)[:10]:
             pattern = f"{r1}-{r2}"
             percent = (count / total_bigrams) * 100
             f.write(f"  {pattern:<30} : {count:<6} occurrences ({percent:.2f}%)\n")

        f.write("\n--- Trigrams with VIOLATION (Top 10) ---\n")
        for (r1, r2, r3), count in sorted(violation_trigrams.items(), key=lambda item: item[1], reverse=True)[:10]:
             pattern = f"{r1}-{r2}-{r3}"
             percent = (count / total_trigrams) * 100
             f.write(f"  {pattern:<30} : {count:<6} occurrences ({percent:.2f}%)\n")

        f.write("\nAnalysis: Examine if 'VIOLATION' words appear primarily in positions typical of CONCEPTs (e.g., before VERBs, after VERBs, alongside other CONCEPTs) rather than behaving like VERBs or SUBJECTs/OBJECTs themselves.\n")

        f.write("\n" + "="*80 + "\n")
        f.write("                         END OF REPORT\n")
        f.write("="*80 + "\n")

    print(f"✅ Report successfully saved to '{OUTPUT_REPORT_FILE}'")

if __name__ == "__main__":
    syntax_pattern_test_v2()