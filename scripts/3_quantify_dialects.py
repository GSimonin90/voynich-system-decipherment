import re
from collections import Counter
import sys
import csv

def load_roots(filename="roots.txt"):
    """Loads roots from a text file, cleaning comments and parsing morphemes."""
    roots = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or '===' in line or not line.strip():
                    continue
                morpheme = line.split('|')[0].strip()
                if morpheme:
                    roots.append(morpheme)
        return roots
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        sys.exit(1)

def get_corpus_text(corpus_file):
    """Loads a corpus file and returns its raw text content."""
    try:
        with open(corpus_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return re.sub(r'<f[0-9a-zA-Zvr]+>', ' ', content)
    except FileNotFoundError:
        print(f"Error: Input file '{corpus_file}' not found.")
        sys.exit(1)

def find_longest_root_in_word(word, sorted_roots):
    """Finds the longest root from the pre-sorted list that is a substring of the word."""
    for root in sorted_roots:
        if root in word:
            return root
    return None

def get_root_sequence(text, sorted_roots):
    """Converts a text string into a sequence of roots."""
    words = text.split()
    return [root for word in words if (root := find_longest_root_in_word(word, sorted_roots)) is not None]

def quantify_concepts_in_dialects(roots, concepts_to_quantify):
    """
    Calculates and compares the relative frequency of key concepts in Dialect A and B.
    """
    print("Starting dialect quantification...")
    sorted_roots = sorted(roots, key=len, reverse=True)

    # Process Corpus A
    print("   - Processing Corpus A...")
    text_A = get_corpus_text("corpus_A.txt")
    sequence_A = get_root_sequence(text_A, sorted_roots)
    counts_A = Counter(sequence_A)
    total_roots_A = len(sequence_A)
    print(f"     Corpus A contains {total_roots_A} roots.")

    # Process Corpus B
    print("   - Processing Corpus B...")
    text_B = get_corpus_text("corpus_B.txt")
    sequence_B = get_root_sequence(text_B, sorted_roots)
    counts_B = Counter(sequence_B)
    total_roots_B = len(sequence_B)
    print(f"     Corpus B contains {total_roots_B} roots.")

    results = []
    for concept in concepts_to_quantify:
        # Calculate normalized frequency (per 1,000 roots) for Dialect A
        freq_A = (counts_A.get(concept, 0) / total_roots_A) * 1000 if total_roots_A > 0 else 0
        # Calculate normalized frequency for Dialect B
        freq_B = (counts_B.get(concept, 0) / total_roots_B) * 1000 if total_roots_B > 0 else 0
        
        results.append({
            'concept': concept,
            'freq_A_per_1000': round(freq_A, 2),
            'freq_B_per_1000': round(freq_B, 2)
        })

    print("Quantification complete.\n")
    return results

def save_quantification_to_csv(results, filename="dialect_quantification.csv"):
    """Saves the quantification results to a CSV file."""
    if not results:
        print("No results to save.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    print(f"Successfully saved dialect quantification to '{filename}'.")

if __name__ == "__main__":
    ROOTS_FILE = "roots.txt"
    OUTPUT_FILE = "dialect_quantification.csv"

    # Define the key concepts whose frequency will create the "fingerprint"
    KEY_CONCEPTS = [
        # Universals
        'aii', 'che', 'cho',
        # "Quality" concepts (predicted higher in B)
        'ol', 'kch', 'teo',
        # "Physical/Process" concepts (predicted higher in A)
        'f', 'et', 'yk',
        # Other interesting concepts
        'ro', 'tai', 'ek'
    ]
    
    print("===== Dialect Fingerprinting Engine =====\n")
    
    print("1. Loading root dictionary...")
    roots = load_roots(ROOTS_FILE)
    
    # 2. Quantify concepts in both dialects
    quantification_results = quantify_concepts_in_dialects(roots, KEY_CONCEPTS)
    
    # 3. Save results
    print(f"3. Saving fingerprint analysis to '{OUTPUT_FILE}'...")
    save_quantification_to_csv(quantification_results, OUTPUT_FILE)

    print("\n===== Analysis complete. =====")
    print(f"Check '{OUTPUT_FILE}' for the quantitative fingerprint of each dialect.")