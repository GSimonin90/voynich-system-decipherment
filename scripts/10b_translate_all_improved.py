# coding: utf-8
import re
from collections import Counter
import sys

# ==============================================================================
#                 *** EXPANDED DICTIONARY (v3.1) ***
# ==============================================================================
# [Dictionary identical to translate_folio_SYNTH_IMPROVED_v1.py]
CONCEPTUAL_DICTIONARY = {
    # Original Roots (v3.0)
    "ro": "Essence/Distillate (Mercury)", "tai": "Balance/Order", "ek": "Group/Set", "et": "Root/Origin", "eke": "Structure/Node", "yk": "Complex Root/Rhizome", "eo": "Celestial Quality", "al": "Igneous/Luminous Quality", "ot": "Heat/Energy/Active Principle", "y": "Subtle Property/Emanation", "or": "Cycle/Cosmos", "pch": "Process/Action", "ar": "Quality/Property/Aspect", "ka": "Action/Manifestation", "ke": "Component/Part of", "aii": "Vital Principle (Jupiter)", "kai": "Vital Principle (Specific)", "da": "Vital Principle (Essence of)", "ol": "Potency/Danger (Mars)", "kch": "Structuring Principle (Saturn)", "ckh": "Internal Structure", "teo": "Harmonic Principle (Venus)", "che": "Substance (Generic)", "cho": "Substance (Specific)", "she": "Substance (Prepared)", "lk": "Salt/Fixed Principle", "cth": "Body/Primordial Matter", "tch": "Material Form", "ra": "Ingredient", "ara": "Compound/Mixture", "pche": "Product/Result", "lche": "Type of Astral Influence", "lshe": "Class of Emanation",
    "ed": "[particle]", "i": "[particle]", # Ignored particles
    "s": "is", "r": "possesses", "l": "is a type of", "d": "is defined as", "f": "is connected to", "t": "relates to", "k": "is fixed in", "p": "results in",
    # --- NEW COMPOUND ROOTS (from violation analysis v1.0) ---
    "qoky": "Specific Fixation/Process", "chdy": "Defined Component/Aspect", "qoty": "Specific Relation/Aspect (Proc)", "chody": "Defined Substance/Type", "shody": "Defined Prepared Substance", "qoteey": "Specific Property (Recipe)", "choky": "Fixed Substance (Herbal)", "chos": "Substantial Essence", "okody": "Defined Celestial State", "qotam": "Specific Influence (Object)", "okees": "Current Celestial State", "qotody": "Specific Defined Class (Pharm)", "qokl": "Specific Type of Solid", "qokody": "Specific Defined Fixed Element", "shos": "Prepared Essence", "otody": "Defined Active State (Astro)", "shoky": "Prepared Fixed Element", "okchd": "Defined Structural State", "shok": "Fixed Prepared Substance", "qoly": "Specific Potency/Agent",
}


# --- System Constants (Updated with new roots) ---
NEW_ROOTS = list(CONCEPTUAL_DICTIONARY.keys())
ALL_ROOTS = sorted(NEW_ROOTS, key=len, reverse=True) # Use the expanded list for parsing
CONNECTORS = ['s', 'r', 'l', 'd', 'f', 't', 'k', 'p'] # Remain the same
SUBJECT_SUFFIXES = sorted(['y', 'dy', 'ey'], key=len, reverse=True)
OBJECT_SUFFIXES = sorted(['n', 'in', 'm'], key=len, reverse=True)
SIGNIFICANT_PREFIXES = ['qo', 'ok', 'ch', 'sh', 'ot']
IGNORE_ROOTS = ['ed', 'i']
EMPHASIS_ROOTS = ['ol', 'al']

# --- CONFIGURATION ---
VOYNICH_SOURCE_FILE = "voynich_ready_nlp.txt" # The correct file (4191 lines)
OUTPUT_TRANSLATION_FILE = "voynich_full_translation_v3_IMPROVED.txt" # New output file name

# --- MODIFIED PARSER (v3 - Ignore EVA, Handle Sequences - Unchanged) ---
class ParsedWord:
    # [Code identical to translate_folio_SYNTH_IMPROVED_v1.py]
    def __init__(self, original_word):
        self.original = original_word
        self.prefix = None
        self.root = None
        self.suffix = None
        self.role = "UNKNOWN"
        self.is_sequence = False # Flag for sequences like o<->l...
        self.parse()
        self.determine_role()

    def parse(self):
        temp_word = self.original
        # NEW: Recognize <-> sequences and treat them as units
        if "<->" in temp_word:
            self.root = f"[Sequence: {temp_word}]"
            self.is_sequence = True
            return # Don't do further parsing on these
        # Standard parsing
        for p in SIGNIFICANT_PREFIXES:
            if temp_word.startswith(p):
                remainder = temp_word[len(p):]
                if len(remainder) > 0 and remainder not in ALL_ROOTS: # Use expanded ALL_ROOTS
                    self.prefix = p
                    temp_word = remainder
                    break
        all_parse_suffixes = sorted(SUBJECT_SUFFIXES + OBJECT_SUFFIXES, key=len, reverse=True)
        for s in all_parse_suffixes:
            if temp_word.endswith(s):
                 remainder = temp_word[:-len(s)]
                 if len(remainder) > 0:
                     self.suffix = s
                     temp_word = remainder
                     break
        if temp_word in ALL_ROOTS: # Use expanded ALL_ROOTS
            self.root = temp_word
            return
        if not self.prefix and not self.suffix:
            for r in ALL_ROOTS: # Use expanded ALL_ROOTS
                if r in self.original:
                    self.root = r
                    start = self.original.find(r)
                    end = start + len(r)
                    if start > 0: self.prefix = self.original[:start]
                    if end < len(self.original): self.suffix = self.original[end:]
                    break
        if not self.root:
            self.root = temp_word # Use the remainder as the root (might be unknown)

    def determine_role(self):
        # Sequences are treated as concepts
        if self.is_sequence:
            self.role = "CONCEPT"
            return
        if self.root in CONNECTORS: self.role = "CONNECTOR"; return
        if self.suffix:
            if self.suffix in SUBJECT_SUFFIXES: self.role = "SUBJECT"; return
            if self.suffix in OBJECT_SUFFIXES: self.role = "OBJECT"; return
        self.role = "CONCEPT"

    def translate(self):
        # If it's a sequence, we already have the 'text'
        if self.is_sequence:
            return self.root
        # Otherwise, standard translation using expanded dictionary
        return CONCEPTUAL_DICTIONARY.get(self.root, f"'{self.root}'").replace("'", "")


# --- IMPROVED SYNTHESIZER (v4 - Handles Incomplete Sentences - Unchanged) ---
def synthesize_interpretation_v4(words):
    # [Code identical to translate_folio_SYNTH_IMPROVED_v1.py]
    components = []
    current_modifiers = []
    main_verb = "relates to" # Default verb if none found
    verb_found = False
    i = 0
    while i < len(words):
        word = words[i]
        if word.root in IGNORE_ROOTS:
            i += 1; continue
        repetition_prefix = ""
        if i + 1 < len(words) and words[i+1].original == word.original:
            if word.root in EMPHASIS_ROOTS: repetition_prefix = "(High) "
            else: repetition_prefix = "(Many/Sequential) "
            i += 1 # Skip the repeated word
        prefix_meaning = ""
        if word.prefix:
            if word.prefix == 'qo': prefix_meaning = "the specific "
            elif word.prefix == 'ok': prefix_meaning = "the current-state "
            elif word.prefix == 'sh': prefix_meaning = "the prepared "
            elif word.prefix == 'ot': prefix_meaning = "the active/heated "
            else: prefix_meaning = f"[{word.prefix.upper()}]-"
        base_translation = word.translate() # Will use expanded dictionary
        full_translation = f"{repetition_prefix}{prefix_meaning}{base_translation}".strip()
        if word.role == "CONCEPT":
             if full_translation: current_modifiers.append(full_translation)
        elif word.role in ["SUBJECT", "OBJECT"]:
             if full_translation:
                components.append({'role': word.role, 'term': full_translation.strip(), 'modifiers': current_modifiers})
                current_modifiers = [] # Reset modifiers for the next component
        elif word.role == "CONNECTOR":
            main_verb = base_translation
            verb_found = True # Mark that we found an explicit verb
        i += 1
    if current_modifiers and components:
        components[-1]['modifiers'].extend(current_modifiers)
    elif current_modifiers and not components:
        pass # Modifiers will be handled below
    subjects = []
    objects = []
    for comp in components:
        mod_str = ""
        if comp['modifiers']:
            mod_counts = Counter(comp['modifiers'])
            mod_parts = [f"{mod} (x{count})" if count > 1 else mod for mod, count in mod_counts.items()]
            mod_str = ", ".join(mod_parts) + " "
        full_phrase = f"the {mod_str}{comp['term']}"
        if comp['role'] == 'SUBJECT': subjects.append(full_phrase)
        else: objects.append(full_phrase)
    subject_phrase = " and ".join(subjects)
    object_phrase = ", ".join(objects)
    if subjects and objects:
        return f"{subject_phrase.capitalize()} {main_verb} {object_phrase}."
    elif subjects and verb_found: # Only Subject + Verb
        return f"{subject_phrase.capitalize()} {main_verb} it."
    elif objects and verb_found: # Only Verb + Object
        return f"It {main_verb} {object_phrase}."
    elif subjects:
         return f"[Subject focus: {subject_phrase.capitalize()}]"
    elif objects:
         return f"[Object focus: {object_phrase}]"
    elif current_modifiers:
        if all(mod.startswith("[Sequence:") for mod in current_modifiers):
             return f"[Sequence Listing: {', '.join(current_modifiers)}]"
        else:
             return f"[Concepts: {', '.join(current_modifiers)}]"
    else:
        return "[Translation failed: No meaningful components found]"

# --- MAIN EXECUTION (MODIFIED TO TRANSLATE ALL) ---
def translate_all_improved(clean_source, output_file):
    """
    Translates the entire clean manuscript using the expanded dictionary (v3.1)
    and the improved synthesizer (v4).
    """
    print(f"Step 1: Reading clean source file '{clean_source}'...")
    try:
        with open(clean_source, 'r', encoding='utf-8') as f:
            all_clean_lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"ERROR: Clean source file '{clean_source}' not found.")
        return

    total_lines = len(all_clean_lines)
    print(f" -> Found {total_lines} paragraphs to translate.")

    print(f"Step 2: Translating all paragraphs (using Dict v3.1, Synth v4)...")
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(f"===== Full Manuscript Translation (Improved v3) =====\n")
        out_f.write(f"Dictionary v3.1 (incl. compound roots), Synthesizer v4 (improved fragments)\n\n")

        for i, line in enumerate(all_clean_lines):
            # Clean EVA tags before splitting
            line_cleaned_eva = re.sub(r'<@[^>]+>', '', line)
            words_list = [w for w in line_cleaned_eva.split() if w]

            if not words_list:
                interpretation = "[Skipped: Line empty after cleaning EVA tags]"
            else:
                words = [ParsedWord(w) for w in words_list]
                interpretation = synthesize_interpretation_v4(words) # Use improved synthesizer

            out_f.write(f"--- Paragraph {i+1} ---\n") # Use 1-based index for paragraph number
            out_f.write(f"Original Cleaned: {line_cleaned_eva}\n")
            out_f.write(f"Translation:      {interpretation}\n")
            out_f.write("-" * 80 + "\n")

            # Print progress update every 100 lines
            if (i + 1) % 100 == 0 or (i + 1) == total_lines:
                progress = (i + 1) / total_lines * 100
                sys.stdout.write(f"\r -> Progress: {i+1}/{total_lines} ({progress:.1f}%)")
                sys.stdout.flush()

    print(f"\n\n✅ Full improved translation complete. Output saved to '{output_file}'.")

if __name__ == "__main__":
    translate_all_improved(
        VOYNICH_SOURCE_FILE,
        OUTPUT_TRANSLATION_FILE
    )