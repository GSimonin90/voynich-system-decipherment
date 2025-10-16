import re
from collections import Counter
import sys

def load_roots(filename="roots.txt"):
    """
    Loads roots from a text file, cleaning comments and parsing morphemes.
    """
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

def load_prefixes(filename="prefixes.txt"):
    """
    Loads a list of prefixes, cleaning comments and parsing morphemes.
    """
    prefixes = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or '===' in line or not line.strip():
                    continue
                # Extract the morpheme part before '|' and clean it
                morpheme = line.split('|')[0].strip()
                if morpheme:
                    prefixes.append(morpheme)
        return prefixes
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found. Please create it.")
        sys.exit(1)

def get_all_words(corpus_file="voynich_super_clean_with_pages.txt"):
    """
    Loads the entire corpus and returns a flat list of all words.
    """
    try:
        with open(corpus_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Remove folio markers before splitting into words
        content_no_folios = re.sub(r'<f[0-9a-zA-Zvr]+>', '', content)
        return content_no_folios.split()
    except FileNotFoundError:
        print(f"Error: Input file '{corpus_file}' not found.")
        sys.exit(1)

def find_longest_root_in_word(word, sorted_roots):
    """
    Finds the longest root from the pre-sorted list that is a substring of the word.
    """
    for root in sorted_roots:
        if root in word:
            return root
    return None

def analyze_prefix_associations(all_words, roots, prefixes_to_analyze):
    """
    Calculates the statistical lift for root associations with specific prefixes.
    """
    print("Starting prefix association analysis...")
    sorted_roots = sorted(roots, key=len, reverse=True)
    
    # 1. Calculate baseline frequency of all roots in the entire corpus
    all_roots_in_corpus = [root for word in all_words if (root := find_longest_root_in_word(word, sorted_roots)) is not None]
    total_root_count = len(all_roots_in_corpus)
    baseline_root_counts = Counter(all_roots_in_corpus)
    print(f"   - Calculated baseline frequencies for {len(baseline_root_counts)} unique roots.")

    results = {}
    
    # 2. For each prefix, analyze its associated roots
    for prefix in prefixes_to_analyze:
        print(f"   - Analyzing prefix '{prefix}-'...")
        # Find all words starting with this prefix
        prefix_words = [word for word in all_words if word.startswith(prefix)]
        if not prefix_words:
            continue
            
        # Find all roots within that subset of words
        roots_in_prefix_context = [root for word in prefix_words if (root := find_longest_root_in_word(word, sorted_roots)) is not None]
        if not roots_in_prefix_context:
            continue

        context_total_roots = len(roots_in_prefix_context)
        context_root_counts = Counter(roots_in_prefix_context)
        
        prefix_results = []
        for root, context_count in context_root_counts.items():
            context_freq = context_count / context_total_roots
            baseline_freq = baseline_root_counts.get(root, 0) / total_root_count
            
            if baseline_freq > 0:
                lift_score = context_freq / baseline_freq
                if lift_score > 1.5: # Only record significant associations
                    prefix_results.append({
                        'root': root,
                        'lift_score': round(lift_score, 2),
                        'context_count': context_count,
                        'context_freq_%': round(context_freq * 100, 2)
                    })
        
        # Sort results for this prefix by lift score
        prefix_results.sort(key=lambda x: x['lift_score'], reverse=True)
        results[prefix] = prefix_results
        
    print("Analysis complete.\n")
    return results

def save_prefix_analysis_to_file(analysis_results, filename="prefix_analysis.txt"):
    """
    Saves the prefix analysis to a readable text file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("===== Morphological Engine: Prefix Function Analysis =====\n")
        
        for prefix, results in analysis_results.items():
            f.write("\n\n" + "="*50 + "\n")
            f.write(f"   Analysis for Prefix: '{prefix}-'\n")
            f.write("="*50 + "\n\n")
            
            if not results:
                f.write("No significant root associations found.\n")
                continue

            f.write("Lift Score | Associated Root | Occurrences in Context | Frequency in Context\n")
            f.write("--------------------------------------------------------------------------\n")
            
            for res in results[:10]: # Show top 10 associations for each prefix
                f.write(f"{str(res['lift_score']).ljust(11)}| {res['root'].ljust(17)} | {str(res['context_count']).ljust(22)} | {res['context_freq_%']}%\n")
                
    print(f"Successfully saved prefix analysis to '{filename}'.")

if __name__ == "__main__":
    CORPUS_FILE = "voynich_super_clean_with_pages.txt"
    ROOTS_FILE = "roots.txt"
    PREFIXES_FILE = "prefixes.txt"
    OUTPUT_FILE = "prefix_analysis.txt"
    
    print("===== Morphological Engine: Analyzing Prefix Functions =====\n")
    
    # 1. Load data
    print("1. Loading data files...")
    roots = load_roots(ROOTS_FILE)
    prefixes = load_prefixes(PREFIXES_FILE)
    all_words = get_all_words(CORPUS_FILE)
    print(f"   - Loaded {len(roots)} roots, {len(prefixes)} prefixes, and {len(all_words)} words.\n")
    
    # 2. Analyze associations
    prefix_associations = analyze_prefix_associations(all_words, roots, prefixes)
    
    # 3. Save results
    print(f"3. Saving analysis to '{OUTPUT_FILE}'...")
    save_prefix_analysis_to_file(prefix_associations, OUTPUT_FILE)

    print("\n===== Analysis complete. =====")