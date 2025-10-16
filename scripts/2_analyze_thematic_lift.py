import re
from collections import Counter
import sys
import csv

# Thematic classification of Voynich folios based on standard academic consensus.
THEME_MAP = {
    'BOTANICAL': (1, 66),
    'ASTROLOGICAL': (67, 84),
    'RECIPES': (85, 116)
}

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

def create_thematic_corpora(segmented_corpus, roots):
    """Creates three separate corpora based on thematic sections."""
    print("Creating thematic corpora (Botanical, Astrological, Recipes)...")
    sorted_roots = sorted(roots, key=len, reverse=True)
    
    thematic_roots = {
        'BOTANICAL': [],
        'ASTROLOGICAL': [],
        'RECIPES': []
    }
    
    for folio_id, text in segmented_corpus.items():
        folio_num_match = re.search(r'(\d+)', folio_id)
        if not folio_num_match:
            continue
        folio_num = int(folio_num_match.group(1))
        
        words = text.split()
        tagged_roots = [root for word in words if (root := find_longest_root_in_word(word, sorted_roots)) is not None]
        
        for theme, (start, end) in THEME_MAP.items():
            if start <= folio_num <= end:
                thematic_roots[theme].extend(tagged_roots)
                break
    
    print("Thematic corpora created successfully.\n")
    return thematic_roots

def analyze_thematic_lift(thematic_roots, all_roots):
    """Calculates the statistical lift of each root in each thematic corpus."""
    print("Calculating thematic lift scores...")
    
    full_corpus_roots = [root for theme_roots in thematic_roots.values() for root in theme_roots]
    total_root_count = len(full_corpus_roots)
    baseline_counts = Counter(full_corpus_roots)
    
    results = []
    
    for root in all_roots:
        baseline_freq = baseline_counts.get(root, 0) / total_root_count
        if baseline_freq == 0:
            continue
            
        root_results = {'root': root}
        for theme, theme_roots in thematic_roots.items():
            context_total_roots = len(theme_roots)
            if context_total_roots == 0:
                root_results[f'lift_{theme}'] = 0
                continue
            
            context_count = theme_roots.count(root)
            context_freq = context_count / context_total_roots
            lift_score = context_freq / baseline_freq
            root_results[f'lift_{theme}'] = round(lift_score, 2)
        
        results.append(root_results)
        
    print("Lift score calculation complete.\n")
    return results

def save_thematic_analysis_to_csv(analysis_results, filename="thematic_analysis.csv"):
    """Saves the thematic analysis to a CSV file."""
    if not analysis_results:
        print("No results to save.")
        return

    headers = ['root', 'lift_BOTANICAL', 'lift_ASTROLOGICAL', 'lift_RECIPES']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(analysis_results)
        
    print(f"Successfully saved thematic analysis to '{filename}'.")

if __name__ == "__main__":
    CORPUS_FILE = "voynich_super_clean_with_pages.txt"
    ROOTS_FILE = "roots.txt"
    OUTPUT_FILE = "thematic_analysis.csv"
    
    print("===== Thematic Analysis Engine: Validating Concept-Theme Links =====\n")
    
    print("1. Loading data files...")
    roots = load_roots(ROOTS_FILE)
    segmented_corpus = load_and_segment_corpus(CORPUS_FILE)
    
    thematic_corpora_roots = create_thematic_corpora(segmented_corpus, roots)
    
    thematic_lift_results = analyze_thematic_lift(thematic_corpora_roots, roots)
    
    print(f"4. Saving analysis to '{OUTPUT_FILE}'...")
    # --- THIS IS THE FIX ---
    save_thematic_analysis_to_csv(thematic_lift_results, OUTPUT_FILE)
    # -----------------------

    print("\n===== Analysis complete. =====")
    print(f"Check '{OUTPUT_FILE}' to see the thematic distribution of concepts.")