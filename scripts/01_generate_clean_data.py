import re
import json

# --- CONFIGURATION ---
VOYNICH_SOURCE_FILE = "voynich.txt"  # The single source of truth

# --- OUTPUT FILES ---
OUTPUT_CLEAN_NLP = "voynich_ready_nlp.txt"      # Clean file for NLP
OUTPUT_MAP_JSON = "section_map.json"           # Map for repetition_analyzer
OUTPUT_FORMATTED_TXT = "voynich_final_formatted_complete.txt"  # Formatted file for thematic_analyzer

# Section map
SECTION_MAP = {
    "Herbal": (1, 66),
    "Astrological": (67, 73),
    "Balneological": (75, 84),
    "Pharmacological": (87, 102),
    "Recipes": (103, 116),
}

# --- HELPER FUNCTIONS ---

def get_folio_id(line):
    """
    Detects folio tags (e.g., '<f1r>', '## <f2v>')
    It looks for any <f...> tag without a dot in the middle.
    """
    match = re.search(r'<(f\d+[rv]\d*)>', line)
    return match.group(1) if match else None

def get_section_from_folio(folio_str):
    """Determines the thematic section from the folio ID string."""
    if not folio_str:
        return "Unknown"
    match = re.search(r'(\d+)', folio_str)
    if not match:
        return "Unknown"
    try:
        folio_num = int(match.group(1))
        for section, (start, end) in SECTION_MAP.items():
            if start <= folio_num <= end:
                return section
    except ValueError:
        pass
    return "Unknown"

def clean_paragraph_text_from_source(line):
    """
    Extracts and cleans the text from a Takahashi format paragraph line.
    Input: '<f1r.P.1;H> fachys.ykal.ar.ataiin... ='
    Output: 'fachys ykal ar ataiin...'
    """
    # Remove the tag at the beginning (e.g., <f1r.P.1;H>)
    text = re.sub(r"^<f\d+[rv]\..*?>\s*", "", line.strip())
    
    # Replace all EVA dots with spaces
    text = text.replace('.', ' ')
    
    # Remove filler characters and special chars (=!*)
    text = re.sub(r"[=!%*]", "", text)
    
    # Return the cleaned, stripped text
    return text.strip()

# --- MAIN ---
def main():
    print(f"Starting file generation from single source: '{VOYNICH_SOURCE_FILE}'")
    
    try:
        with open(VOYNICH_SOURCE_FILE, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Source file '{VOYNICH_SOURCE_FILE}' not found.")
        return

    all_clean_lines = []         # For voynich_ready_nlp.txt
    section_map_json = {}        # For section_map.json
    formatted_text_lines = []    # For voynich_final_formatted.txt

    current_folio = None
    current_section = "Unknown"
    paragraph_index = 0

    print("Parsing source file and generating outputs...")
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue  # Skip empty lines and comments

        # Detect folio marker
        folio_id = get_folio_id(stripped)
        if folio_id and "." not in folio_id:
            current_folio = folio_id
            current_section = get_section_from_folio(current_folio)
            formatted_text_lines.append(f"<{current_folio}>")
            continue

        # Detect and process paragraph lines with ;H> (Takahashi transcription)
        if re.match(r"<f\d+[rv]\..*?;H>", stripped):
            if current_folio is None:
                print(f"WARNING: Found paragraph line before any folio tag. Skipping: {stripped}")
                continue
                
            # Extract and clean the text
            clean_text = clean_paragraph_text_from_source(stripped)
            
            if clean_text:
                # Add to the clean lines list
                all_clean_lines.append(clean_text)
                
                # Add to the formatted text list
                formatted_text_lines.append(clean_text)
                
                # Add to the JSON map (using string key)
                section_map_json[str(paragraph_index)] = current_section
                
                paragraph_index += 1

    total_paras = len(all_clean_lines)
    if total_paras == 0:
        print("ERROR: No paragraphs were extracted. Check parsing logic and file.")
        return
        
    print(f"✅ Success! Extracted and cleaned {total_paras} paragraphs.")

    # Save File 1: voynich_ready_nlp.txt
    try:
        with open(OUTPUT_CLEAN_NLP, "w", encoding="utf-8") as f:
            f.write("\n".join(all_clean_lines))
        print(f"💾 Saved corrected clean file to '{OUTPUT_CLEAN_NLP}'")
    except Exception as e:
        print(f"ERROR saving {OUTPUT_CLEAN_NLP}: {e}")

    # Save File 2: section_map.json
    try:
        with open(OUTPUT_MAP_JSON, "w", encoding="utf-8") as f:
            json.dump(section_map_json, f, indent=2)
        print(f"💾 Saved section map to '{OUTPUT_MAP_JSON}'")
    except Exception as e:
        print(f"ERROR saving {OUTPUT_MAP_JSON}: {e}")

    # Save File 3: voynich_final_formatted_complete.txt
    try:
        with open(OUTPUT_FORMATTED_TXT, "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_text_lines))
        print(f"💾 Saved formatted text to '{OUTPUT_FORMATTED_TXT}'")
    except Exception as e:
        print(f"ERROR saving {OUTPUT_FORMATTED_TXT}: {e}")

if __name__ == "__main__":
    main()