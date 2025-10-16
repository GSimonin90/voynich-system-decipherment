import re
import sys

# ==============================================================================
#                 VOYNICH CONCEPTUAL DICTIONARY (v1.1 - COMPLETE)
# ==============================================================================
# This dictionary is the core of the translator, mapping roots to their functions.
CONCEPTUAL_DICTIONARY = {
    # Abstract Concepts (from root_hotspots analysis)
    "ro":  {"type": "Concept", "translation": "Essence/Distillate (Mercury)"},
    "tai": {"type": "Concept", "translation": "Balance/Order"},
    "ek":  {"type": "Concept", "translation": "Group/Set/Cluster"},
    "et":  {"type": "Concept", "translation": "Root/Origin"},
    "eke": {"type": "Concept", "translation": "Structure/Node"},
    "yk":  {"type": "Concept", "translation": "Complex Root/Rhizome"},
    "eo":  {"type": "Concept", "translation": "Celestial Quality"},
    "al":  {"type": "Concept", "translation": "Igneous/Luminous Quality (Sun?)"},

    # Planetary Concepts (from Paper 2)
    "aii": {"type": "Concept", "translation": "Vital Principle (Jupiter)"},
    "da":  {"type": "Concept", "translation": "Vital Principle (Jupiter)"}, # 'da' is a strong associate/synonym
    "ol":  {"type": "Concept", "translation": "Potency/Danger (Mars)"},
    "kch": {"type": "Concept", "translation": "Structuring Principle (Saturn)"},
    "teo": {"type": "Concept", "translation": "Harmonic Principle (Venus)"},

    # Material Concepts (from syntactic analysis)
    "che": {"type": "Concept", "translation": "Substance (Generic)"},
    "cho": {"type": "Concept", "translation": "Substance (Specific)"},
    "she": {"type": "Concept", "translation": "Substance (Prepared)"},

    # Connectors (from syntactic analysis)
    "s":   {"type": "Connector", "translation": "is / is of the nature of"},
    "r":   {"type": "Connector", "translation": "has / possesses the quality of"},
    "l":   {"type": "Connector", "translation": "is a type of / is composed of"},
    "d":   {"type": "Connector", "translation": "is defined as"},
    "f":   {"type": "Connector", "translation": "is connected to / flows into"},
}
# ==============================================================================

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

def get_tagged_folio(segmented_corpus, roots, folio_id):
    """Gets the sequence of roots for a specific folio."""
    if folio_id not in segmented_corpus:
        return None
        
    print(f"Tagging folio '{folio_id}'...")
    sorted_roots = sorted(roots, key=len, reverse=True)
    text = segmented_corpus[folio_id]
    words = text.split()
    tagged_roots = [root for word in words if (root := find_longest_root_in_word(word, sorted_roots)) is not None]
    return tagged_roots

def translate_sequence(sequence):
    """Translates a sequence of roots using the conceptual dictionary."""
    print("Generating functional translation...")
    translation = []
    for root in sequence:
        if root in CONCEPTUAL_DICTIONARY:
            entry = CONCEPTUAL_DICTIONARY[root]
            if entry["type"] == "Connector":
                translation.append(f"\n  └── {entry['translation'].upper()}...")
            else: # Concept
                translation.append(f"-> [{entry['translation']}]")
        else:
            # For unknown roots, show the root itself as a placeholder
            translation.append(f"-> (concept:{root})")
    
    # Clean up formatting for readability
    return " ".join(translation).replace('\n ', '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python translate_folio.py <folio_id>")
        print("Example: python translate_folio.py f65r")
        sys.exit(1)

    FOLIO_TO_TRANSLATE = sys.argv[1].lower()
    CORPUS_FILE = "voynich_super_clean_with_pages.txt"
    ROOTS_FILE = "roots.txt"
    
    print(f"===== Syntactic Translator: Generating Functional Translation for Folio '{FOLIO_TO_TRANSLATE}' =====\n")
    
    # 1. Load data
    print("1. Loading data files...")
    roots = load_roots(ROOTS_FILE)
    segmented_corpus = load_and_segment_corpus(CORPUS_FILE)
    
    # 2. Get the tagged sequence for the target folio
    folio_sequence = get_tagged_folio(segmented_corpus, roots, FOLIO_TO_TRANSLATE)
    
    if folio_sequence is None:
        print(f"Error: Folio '{FOLIO_TO_TRANSLATE}' not found in the corpus.")
        sys.exit(1)
        
    print(f"   - Found {len(folio_sequence)} roots in folio '{FOLIO_TO_TRANSLATE}'.\n")
    
    # 3. Translate the sequence
    functional_translation = translate_sequence(folio_sequence)
    
    # 4. Print the final result
    print("\n" + "="*80)
    print(f"                FUNCTIONAL TRANSLATION FOR FOLIO '{FOLIO_TO_TRANSLATE}'")
    print("="*80 + "\n")
    print("NOTE: This is a 'pseudo-translation' that displays the logical structure of the text.\n")
    print(functional_translation)
    print("\n" + "="*80)

    print("\n===== Translation complete. =====")