import re
import sys

def create_segmented_file(input_file="voynich.txt", output_file="voynich_super_clean_with_pages.txt"):
    """
    Reads a raw Voynich manuscript transcription, cleans it, and saves a new
    version containing folio markers for segmentation.
    """
    print(f"Starting to process '{input_file}'...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Please ensure it is in the correct directory.")
        sys.exit(1)

    output_content = []
    current_folio = None

    for line in lines:
        if line.startswith('#'):
            continue

        folio_match = re.search(r'<*([fF]\d+[a-zA-ZvrVR_0-9]+)', line)
        if folio_match:
            new_folio = folio_match.group(1).lower()
            if new_folio != current_folio:
                current_folio = new_folio
                if output_content:
                    output_content.append('\n')
                output_content.append(f"<{current_folio}>\n")
        
        text_part = line
        text_part = re.sub(r'\{.*?\}|\[.*?\]', '', text_part)
        text_part = re.sub(r'<.*?>', '', text_part)
        text_part = re.sub(r'^[fF\dvrVRpPlL_\.\d;]+[;]?', '', text_part)
        
        # KEY FIX: Replace all periods with spaces to standardize word separation.
        text_part = text_part.replace('.', ' ')
        
        cleaned_words = re.findall(r'[a-z]+', text_part.lower())
        cleaned_line = ' '.join(cleaned_words)
        
        if cleaned_line:
            output_content.append(cleaned_line + ' ')

    try:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            full_text = ''.join(output_content)
            full_text = re.sub(r' \n', '\n', full_text)
            full_text = re.sub(r' +', ' ', full_text)
            f_out.write(full_text.strip())
        print(f"Successfully created clean and segmented corpus: '{output_file}'")
    except IOError as e:
        print(f"Error writing to file '{output_file}'. Reason: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_segmented_file()