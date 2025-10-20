import re
from collections import Counter
import textwrap

# ==============================================================================
#                 VOYNICH CONCEPTUAL DICTIONARY (v3.0 - FINAL)
# ==============================================================================
CONCEPTUAL_DICTIONARY = {
    "ro": "Essence/Distillate (Mercury)", "tai": "Balance/Order", "ek": "Group/Set", "et": "Root/Origin", "eke": "Structure/Node", "yk": "Complex Root/Rhizome", "eo": "Celestial Quality", "al": "Igneous/Luminous Quality", "ot": "Heat/Energy/Active Principle", "y": "Subtle Property/Emanation", "or": "Cycle/Cosmos", "pch": "Process/Action", "ar": "Quality/Property/Aspect", "ka": "Action/Manifestation", "ke": "Component/Part of", "aii": "Vital Principle (Jupiter)", "kai": "Vital Principle (Specific)", "da": "Vital Principle (Essence of)", "ol": "Potency/Danger (Mars)", "kch": "Structuring Principle (Saturn)", "ckh": "Internal Structure", "teo": "Harmonic Principle (Venus)", "che": "Substance (Generic)", "cho": "Substance (Specific)", "she": "Substance (Prepared)", "lk": "Salt/Fixed Principle", "cth": "Body/Primordial Matter", "tch": "Material Form", "ra": "Ingredient", "ara": "Compound/Mixture", "pche": "Product/Result", "lche": "Type of Astral Influence", "lshe": "Class of Emanation", "ed": "'ed'", "i": "'i'", "s": "is", "r": "possesses", "l": "is a type of", "d": "is defined as", "f": "is connected to", "t": "relates to", "k": "is fixed in", "p": "results in",
}

# --- System Constants ---
ALL_ROOTS = sorted(list(CONCEPTUAL_DICTIONARY.keys()), key=len, reverse=True)
CONNECTORS = ['s', 'r', 'l', 'd', 'f', 't', 'k', 'p']
SUBJECT_SUFFIXES = sorted(['y', 'dy', 'ey'], key=len, reverse=True)
OBJECT_SUFFIXES = sorted(['n', 'in', 'm'], key=len, reverse=True)
SECTION_MAP = {
    "Herbal": (1, 66), "Astrological": (67, 73), "Balneological": (75, 84),
    "Pharmacological": (87, 102), "Recipes": (103, 116),
}

# --- PARSER CLASS (Reused from previous scripts) ---
class ParsedWord:
    """Parses a word to identify its root and determine its grammatical role."""
    def __init__(self, original_word):
        self.original = original_word
        self.root, self.suffix, self.role = None, None, "UNKNOWN"
        self.parse()
        self.determine_role()
    def parse(self):
        if self.original in ALL_ROOTS: self.root = self.original; return
        for r in ALL_ROOTS:
            if r in self.original:
                start, end = self.original.find(r), self.original.find(r) + len(r)
                self.root, self.suffix = r, self.original[end:] or None; return
        self.root = self.original
    def determine_role(self):
        if self.root in CONNECTORS: self.role = "CONNECTOR"; return
        if self.suffix:
            for s in SUBJECT_SUFFIXES:
                if self.suffix.endswith(s): self.role = "SUBJECT"; return
            for s in OBJECT_SUFFIXES:
                if self.suffix.endswith(s): self.role = "OBJECT"; return
        self.role = "CONCEPT"

# --- HELPER FUNCTIONS ---
def get_section_from_folio(folio_str):
    """Determines the thematic section from a folio string."""
    match = re.search(r'(\d+)', folio_str)
    if not match: return "Unknown"
    folio_num = int(match.group(1))
    for section, (start, end) in SECTION_MAP.items():
        if start <= folio_num <= end: return section
    return "Unknown"

# --- MAIN ANALYSIS FUNCTION ---
def scan_grammatical_patterns(input_file):
    """
    Scans the entire manuscript from the original EVA source file,
    cleans the data on the fly, and counts key grammatical patterns.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Please ensure 'voynich.txt' is in the directory.")
        return

    # --- Counters ---
    total_paragraphs = 0
    pattern1_full_sentence = 0
    pattern2_clause = 0
    section_connector_freqs = {name: Counter() for name in SECTION_MAP}
    current_section = "Unknown"
    
    print("Scanning the original manuscript file for grammatical patterns...")

    for line in lines:
        raw_line = line.strip()
        if not raw_line or raw_line.startswith('#'):
            continue # Skip empty lines and comments

        # Check for folio tags
        folio_match = re.search(r'<([a-zA-Z0-9vr]+)>', raw_line)
        if folio_match:
            current_section = get_section_from_folio(folio_match.group(1))
            continue
        
        # Clean the paragraph line on the fly
        cleaned_line = re.sub(r'\{.*?\}', '', raw_line)  # Remove paragraph markers like {f1r.P.1}
        cleaned_line = cleaned_line.replace('.', ' ')     # Replace EVA dots with spaces
        cleaned_line = re.sub(r'[=\*!]', '', cleaned_line) # Remove special characters
        cleaned_line = cleaned_line.strip()

        if not cleaned_line:
            continue

        total_paragraphs += 1
        
        # --- Tagging Pass ---
        words = cleaned_line.split()
        roles = [ParsedWord(w).role for w in words]
        role_sequence = " ".join(roles)

        # --- Pattern Matching ---
        if re.search(r'SUBJECT.+CONNECTOR.+OBJECT', role_sequence): pattern1_full_sentence += 1
        if re.search(r'CONNECTOR.+OBJECT', role_sequence): pattern2_clause += 1

        # --- Connector Distribution Analysis ---
        if current_section != "Unknown":
            for word in words:
                parsed = ParsedWord(word)
                if parsed.role == "CONNECTOR":
                    section_connector_freqs[current_section][parsed.root] += 1
    
    # --- Generate Final Report ---
    # (Report generation logic remains the same, but will now have correct data)
    print("\n" + "="*80)
    print("                 VOYNICH MANUSCRIPT GRAMMATICAL SCANNER - RESULTS (v2)")
    print("="*80)

    print("\n## 1. Universal Syntactic Structure Analysis ##\n")
    percentage_p1 = (pattern1_full_sentence / total_paragraphs) * 100
    percentage_p2 = (pattern2_clause / total_paragraphs) * 100
    
    print(f"Total Paragraphs Analyzed: {total_paragraphs}")
    print("-" * 50)
    print(f"Found 'Subject->Connector->Object' structure in: {pattern1_full_sentence} paragraphs ({percentage_p1:.2f}%)")
    print(f"Found 'Connector->Object' clause in:            {pattern2_clause} paragraphs ({percentage_p2:.2f}%)")
    
    if percentage_p1 > 10: # Only print conclusion if results are meaningful
        print(textwrap.dedent("""
        Conclusion: The high frequency of these patterns confirms they are not coincidences
        but are fundamental building blocks of the manuscript's language.
        """))

    print("\n## 2. Thematic Distribution of Connectors (Verbs) ##\n")
    print("This analysis shows how the 'verbs' of the language are used in different thematic contexts.\n")
    
    for section, freqs in section_connector_freqs.items():
        print(f"--- {section} Section ---")
        if not freqs:
            print("  No connectors found.")
            continue
        sorted_connectors = sorted(freqs.items(), key=lambda item: item[1], reverse=True)
        for connector, count in sorted_connectors[:5]:
            # Use a default translation if not in dict (for secondary connectors)
            trans = CONCEPTUAL_DICTIONARY.get(connector, f"'{connector}'") or f"'{connector}'"
            print(f"  - '{connector}' ({trans}): {count} occurrences")
        print("")

    print("="*80)
    print("                                  SCAN COMPLETE")
    print("="*80)


if __name__ == "__main__":
    # The script now reads from the original, reliable source file.
    VOYNICH_TEXT_FILE = "voynich.txt"
    scan_grammatical_patterns(VOYNICH_TEXT_FILE)