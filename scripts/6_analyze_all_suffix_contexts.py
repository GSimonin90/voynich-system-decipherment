import re
from collections import Counter
import sys

def load_morphemes(filename):
    """Loads a list of morphemes (roots, prefixes, or suffixes) from a text file, cleaning comments."""
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

def get_corpus_text(corpus_file="voynich_super_clean_with_pages.txt"):
    """Loads the entire corpus as a single string."""
    try:
        with open(corpus_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Remove folio markers to treat the text as a continuous stream
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

def analyze_all_suffixes(all_words, roots, suffixes_to_analyze):
    """
    Performs a contextual analysis for a list of suffixes.
    """
    print("Starting suffix context analysis...")
    sorted_roots = sorted(roots, key=len, reverse=True)
    
    # Create a list of (word, root) tuples for the entire corpus
    word_root_pairs = []
    for word in all_words:
        root = find_longest_root_in_word(word, sorted_roots)
        if root:
            word_root_pairs.append((word, root))
    
    print(f"   - Corpus processed into {len(word_root_pairs)} word-root pairs.")

    analysis_results = {}
    
    for suffix in suffixes_to_analyze:
        print(f"   - Analyzing context for suffix '...{suffix}'")
        
        # Data containers for this suffix
        associated_roots = []
        preceding_roots = []
        following_roots = []
        
        for i in range(len(word_root_pairs)):
            current_word, current_root = word_root_pairs[i]
            
            if current_word.endswith(suffix):
                # 1. This root is associated with the suffix
                associated_roots.append(current_root)
                
                # 2. Find the preceding root
                if i > 0:
                    preceding_roots.append(word_root_pairs[i-1][1])
                
                # 3. Find the following root
                if i < len(word_root_pairs) - 1:
                    following_roots.append(word_root_pairs[i+1][1])

        analysis_results[suffix] = {
            "associations": Counter(associated_roots),
            "preceded_by": Counter(preceding_roots),
            "followed_by": Counter(following_roots)
        }
        
    print("Analysis complete.\n")
    return analysis_results

def save_suffix_analysis_to_file(analysis_results, filename="all_suffix_contexts.txt"):
    """Saves the suffix analysis to a readable text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("===== Morphological Engine: Suffix Context Analysis =====\n")
        
        for suffix, results in analysis_results.items():
            f.write("\n\n" + "="*60 + "\n")
            f.write(f"   Context Analysis for Suffix: '...{suffix}'\n")
            f.write("="*60 + "\n")
            
            # Top Associated Roots
            f.write("\n--- Top 10 Associated Roots ---\n")
            if results["associations"]:
                for root, count in results["associations"].most_common(10):
                    f.write(f"  {root.ljust(15)} ({count} occurrences)\n")
            else:
                f.write("  None\n")

            # Top Preceding Roots
            f.write("\n--- Top 10 Preceding Roots ---\n")
            if results["preceded_by"]:
                for root, count in results["preceded_by"].most_common(10):
                    f.write(f"  {root.ljust(15)} ({count} occurrences)\n")
            else:
                f.write("  None\n")

            # Top Following Roots
            f.write("\n--- Top 10 Following Roots ---\n")
            if results["followed_by"]:
                for root, count in results["followed_by"].most_common(10):
                    f.write(f"  {root.ljust(15)} ({count} occurrences)\n")
            else:
                f.write("  None\n")
                
    print(f"Successfully saved suffix analysis to '{filename}'.")


if __name__ == "__main__":
    CORPUS_FILE = "voynich_super_clean_with_pages.txt"
    ROOTS_FILE = "roots.txt"
    SUFFIXES_FILE = "suffixes.txt" # New input file
    OUTPUT_FILE = "all_suffix_contexts.txt"
    
    print("===== Morphological Engine: Analyzing Suffix Contexts =====\n")
    
    # 1. Load data
    print("1. Loading data files...")
    roots = load_morphemes(ROOTS_FILE)
    suffixes = load_morphemes(SUFFIXES_FILE)
    corpus_text = get_corpus_text(CORPUS_FILE)
    all_words = corpus_text.split()
    print(f"   - Loaded {len(roots)} roots, {len(suffixes)} suffixes, and {len(all_words)} words.\n")
    
    # 2. Analyze suffix contexts
    suffix_contexts = analyze_all_suffixes(all_words, roots, suffixes)
    
    # 3. Save results
    print(f"3. Saving analysis to '{OUTPUT_FILE}'...")
    save_suffix_analysis_to_file(suffix_contexts, OUTPUT_FILE)

    print("\n===== Analysis complete. =====")