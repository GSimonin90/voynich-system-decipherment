import re
from collections import Counter
import sys

def load_morphemes(filename):
    """Loads a list of morphemes (roots) from a text file, cleaning comments."""
    morphemes = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or '===' in line or not line.strip():
                    continue
                morpheme = line.split('|')[0].strip()
                if morpheme:
                    morphemes.append(morpheme)
        return morphemes
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        sys.exit(1)

def load_and_segment_corpus(filename="voynich_super_clean_with_pages.txt"):
    """Loads the corpus and segments it into a dictionary based on folio markers."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        sys.exit(1)
    
    segments = re.split(r'(<f[0-9a-zA-Zvr]+>)', content)
    
    segmented_corpus = {}
    if len(segments) > 1:
        for i in range(1, len(segments), 2):
            folio_id = segments[i].strip('<>')
            text = segments[i+1].strip()
            if text:
                segmented_corpus[folio_id] = text
            
    return segmented_corpus

def find_longest_root_in_word(word, sorted_roots):
    """Finds the longest root from the pre-sorted list that is a substring of the word."""
    for root in sorted_roots:
        if root in word:
            return root
    return None

def tag_corpus_to_sequence(segmented_corpus, roots):
    """Converts the entire word-based corpus into a single flat list of roots."""
    print("Tagging corpus and creating a flat root sequence...")
    sorted_roots = sorted(roots, key=len, reverse=True)
    full_sequence = []
    for folio_id in sorted(segmented_corpus.keys()):
        text = segmented_corpus[folio_id]
        words = text.split()
        tagged_roots = [root for word in words if (root := find_longest_root_in_word(word, sorted_roots)) is not None]
        full_sequence.extend(tagged_roots)
    print("Tagging complete.\n")
    return full_sequence

def find_trigram_patterns(sequence, target_root):
    """Finds and counts all trigram patterns centered around a target root."""
    trigrams = []
    for i in range(len(sequence) - 2):
        if sequence[i+1] == target_root:
            trigram = (sequence[i], sequence[i+1], sequence[i+2])
            trigrams.append(trigram)
    
    return Counter(trigrams)

def save_stress_test_results(all_results, filename="connector_stress_test.txt"):
    """Saves the stress test results to a single text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("===== Syntactic Engine: Connector Stress Test =====\n")
        f.write("This analysis tests if ambiguous single-letter roots behave like connectors.\n")
        
        for target_root, pattern_counts in all_results.items():
            f.write("\n\n" + "="*50 + "\n")
            f.write(f"   Analysis for Potential Connector: '{target_root}'\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Found {len(pattern_counts)} unique '[Concept] -> {target_root} -> [Concept]' patterns.\n\n")

            if not pattern_counts:
                f.write("Conclusion: This root does NOT behave like a connector.\n")
                continue
            
            f.write("Top 5 Patterns:\n")
            f.write("--------------------------------------------------\n")
            f.write("Frequency | Pattern\n")
            f.write("--------------------------------------------------\n")
            
            for pattern, count in pattern_counts.most_common(5):
                f.write(f"{str(count).ljust(9)} | {' -> '.join(pattern)}\n")

            if len(pattern_counts) > 5:
                f.write("...\n")
            
            f.write("\nConclusion: This root shows connector-like behavior.\n")
            
    print(f"\nSuccessfully saved stress test results to '{filename}'.")

if __name__ == "__main__":
    CORPUS_FILE = "voynich_super_clean_with_pages.txt"
    ROOTS_FILE = "roots.txt"
    OUTPUT_FILE = "connector_stress_test.txt"
    
    # Define the ambiguous roots to test
    AMBIGUOUS_ROOTS = ['t', 'k', 'p']
    
    print("===== Syntactic Engine: Stress-Testing Connectors =====\n")
    
    # --- This part runs only once ---
    print("1. Loading and tagging corpus...")
    roots = load_morphemes(ROOTS_FILE)
    segmented_corpus = load_and_segment_corpus(CORPUS_FILE)
    full_root_sequence = tag_corpus_to_sequence(segmented_corpus, roots)
    print(f"   - Corpus converted to a sequence of {len(full_root_sequence)} roots.\n")
    # ------------------------------------

    all_results = {}
    
    for root in AMBIGUOUS_ROOTS:
        print(f"2. Searching for trigram patterns centered on '{root}'...")
        found_patterns = find_trigram_patterns(full_root_sequence, root)
        all_results[root] = found_patterns

    # 3. Save all results to a single file
    print(f"\n3. Saving all results to '{OUTPUT_FILE}'...")
    save_stress_test_results(all_results, OUTPUT_FILE)

    print("\n===== Stress test complete. =====")