import re
import sys

# Standard academic classification of Voynich folios into Currier Languages A and B.
DIALECT_MAP = {
    'A': [
        '1v', '2r', '2v', '3r', '3v', '4r', '4v', '5r', '5v', '6r', '6v', '7r', '7v', '8r', '8v',
        '9r', '9v', '10r', '10v', '11r', '11v', '12r', '13r', '13v', '14r', '14v', '15r', '15v',
        '16r', '16v', '17r', '18r', '18v', '19r', '19v', '20r', '20v', '21r', '21v', '22r',
        '22v', '23r', '23v', '24r', '24v', '25r', '25v', '33r', '33v', '34r', '34v', '35r',
        '35v', '36r', '36v', '37r', '37v', '38r', '38v', '39r', '39v', '40r', '40v', '41r',
        '41v', '42r', '42v', '43r', '43v', '44r', '44v', '45r', '45v', '46r', '46v', '47r',
        '47v', '48r', '48v', '49r', '49v', '50r', '50v', '51r', '51v', '52r', '52v', '53r',
        '53v', '54r', '54v', '55r', '55v', '56r', '56v', '57r', '57v', '58r', '58v', '94r',
        '94v', '95r1', '95r2', '95v1', '95v2', '96r', '96v', '103r', '103v', '104r', '104v',
        '105r', '105v', '106r', '106v', '107r', '107v', '108r', '108v', '111r', '111v', '112r',
        '112v', '113r', '113v', '114r', '114v', '115r', '115v', '116r'
    ],
    'B': [
        '1r', '26r', '26v', '27r', '27v', '28r', '28v', '29r', '29v', '30r', '30v', '31r', '31v',
        '32r', '32v', '65r', '65v', '66r', '66v', '67r1', '67r2', '67v1', '67v2', '68r1', '68r2',
        '68r3', '68v1', '68v2', '68v3', '69r', '69v', '70r1', '70r2', '70v1', '70v2', '71r',
        '71v', '72r1', '72r2', '72r3', '72v1', '72v2', '72v3', '73r', '73v', '75r', '75v',
        '76r', '76v', '77r', '77v', '78r', '78v', '79r', '79v', '80r', '80v', '81r', '81v',
        '82r', '82v', '83r', '83v', '84r', '84v', '85r1', '85r2', '86v1', '86v2', '86v3',
        '86v4', '86v5', '86v6', '87r', '87v', '88r', '88v', '89r1', '89r2', '89v1', '89v2',
        '90r1', '90r2', '90v1', '90v2', '93r', '93v', '99r', '99v', '100r', '100v', '101r',
        '101v', '102r1', '102r2', '102v1', '102v2'
    ]
}

def segment_corpus_by_dialect(input_file="voynich_super_clean_with_pages.txt"):
    """
    Reads the main corpus and splits it into two separate files based on
    Currier's Language A and Language B classifications.
    """
    print(f"Starting segmentation of '{input_file}' by dialect...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Main corpus file '{input_file}' not found.")
        sys.exit(1)

    segments = re.split(r'(<f[0-9a-zA-Zvr]+>)', content)
    
    corpus_A = []
    corpus_B = []
    
    count_A = 0
    count_B = 0
    
    if len(segments) > 1:
        for i in range(1, len(segments), 2):
            folio_marker = segments[i]
            # --- THIS IS THE FIX ---
            # Correctly strip '<', '>', and the leading 'f' to match the map keys
            folio_id = folio_marker.strip('<>f')
            text_content = segments[i+1].strip()

            if not text_content:
                continue

            if folio_id in DIALECT_MAP['A']:
                corpus_A.append(f"{folio_marker}\n{text_content}\n")
                count_A += 1
            elif folio_id in DIALECT_MAP['B']:
                corpus_B.append(f"{folio_marker}\n{text_content}\n")
                count_B += 1

    try:
        with open("corpus_A.txt", 'w', encoding='utf-8') as f_A:
            f_A.write("".join(corpus_A))
        print(f"Successfully created 'corpus_A.txt' with {count_A} folio sections.")
    except IOError as e:
        print(f"Error writing 'corpus_A.txt': {e}")
        
    try:
        with open("corpus_B.txt", 'w', encoding='utf-8') as f_B:
            f_B.write("".join(corpus_B))
        print(f"Successfully created 'corpus_B.txt' with {count_B} folio sections.")
    except IOError as e:
        print(f"Error writing 'corpus_B.txt': {e}")

if __name__ == "__main__":
    segment_corpus_by_dialect()
    print("\nSegmentation complete. You can now run the analysis scripts on each corpus.")