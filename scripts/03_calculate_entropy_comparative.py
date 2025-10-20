import math
from collections import Counter
import re
import random
import os

# --- CONFIGURATION ---
VOYNICH_FILE = "voynich_ready_nlp.txt"
COPIALE_FILE = "copiale_english_translation.txt" # Local file
SEFER_FILE = "sefer_yetzirah_english.txt"     # Local file
RANDOM_FILE = "voynich_random_COMPARATIVE.txt" # New random file name

# --- HELPER FUNCTIONS ---

def clean_text(text, language='english'):
    """
    Cleans text: lowercase, remove Gutenberg headers/footers (basic),
    remove punctuation/numbers, keep only letters and spaces relevant to the language.
    """
    text = text.lower()

    # Basic Gutenberg header/footer removal
    start_marker = "*** start of this project gutenberg ebook"
    end_marker = "*** end of this project gutenberg ebook"
    start_idx = text.find(start_marker)
    if start_idx != -1: text = text[start_idx + len(start_marker):]
    end_idx = text.find(end_marker)
    if end_idx != -1: text = text[:end_idx]

    # Language-specific cleaning (simple version)
    if language == 'german': # Keep umlauts for German if present (Copiale might have them)
         text = re.sub(r'[^a-zäöüß\s]', '', text)
    else: # Default English/Voynich (basic latin alphabet)
         text = re.sub(r'[^a-z\s]', '', text)

    text = re.sub(r'\s+', ' ', text) # Normalize whitespace
    return text.strip()

def calculate_second_order_entropy(text):
    """Calculates H_2 (bigram-based) entropy for a given text string."""
    # [Code identical to previous entropy script]
    if not text: return 0
    words = text.split()
    if len(words) < 2: return 0
    unigram_counts = Counter(words[:-1])
    bigrams = list(zip(words[:-1], words[1:]))
    bigram_counts = Counter(bigrams)
    total_bigrams = len(bigrams)
    if total_bigrams == 0: return 0
    entropy = 0.0
    for bigram, bigram_count in bigram_counts.items():
        preceding_word = bigram[0]
        preceding_count = unigram_counts[preceding_word]
        if preceding_count > 0:
            conditional_prob = bigram_count / preceding_count
            p_bigram = bigram_count / total_bigrams
            if conditional_prob > 0 and p_bigram > 0:
                 entropy -= p_bigram * math.log2(conditional_prob)
    return entropy

# --- MAIN EXECUTION ---
def main():
    print("--- Comparative Entropy Analysis (v1 - Local Files) ---")

    results = {}

    # --- Check for files ---
    required_files = [VOYNICH_FILE, COPIALE_FILE, SEFER_FILE]
    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print(f"ERROR: Missing required file(s): {', '.join(missing)}")
        return

    print("Step 1: All source files found.")

    # --- Step 2: Create Randomized Voynich File ---
    print("Step 2: Creating randomized Voynich file...")
    try:
        with open(VOYNICH_FILE, 'r', encoding='utf-8') as f:
            voynich_text = f.read() # Read original Voynich for randomization
        voynich_words = voynich_text.split()
        random.shuffle(voynich_words)
        voynich_random_text = " ".join(voynich_words)
        with open(RANDOM_FILE, 'w', encoding='utf-8') as f:
            f.write(voynich_random_text)
        print(" -> Randomized file created successfully.")
    except Exception as e:
        print(f"Error creating random file: {e}")
        return

    # --- Step 3: Run Analysis ---
    print("\nStep 3: Calculating entropy values...")

    # 1. Voynich (Original)
    # Text already loaded
    results['Voynich (Original)'] = calculate_second_order_entropy(voynich_text)
    print(f"  Voynich (Original): {results['Voynich (Original)']:.4f} bits/bigram")

    # 2. Voynich (Randomized)
    results['Voynich (Random)'] = calculate_second_order_entropy(voynich_random_text)
    print(f"  Voynich (Random):   {results['Voynich (Random)']:.4f} bits/bigram")

    # 3. Copiale Cipher (English Translation)
    try:
        with open(COPIALE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            copiale_raw = f.read()
        copiale_text = clean_text(copiale_raw, language='english') # Clean as English
        results['Copiale (English)'] = calculate_second_order_entropy(copiale_text)
        print(f"  Copiale (English):  {results['Copiale (English)']:.4f} bits/bigram")
    except Exception as e:
        print(f"Error analyzing {COPIALE_FILE}: {e}")
        results['Copiale (English)'] = None

    # 4. Sefer Yetzirah (English Translation)
    try:
        with open(SEFER_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            sefer_raw = f.read()
        sefer_text = clean_text(sefer_raw, language='english') # Clean as English
        results['Sefer Yetzirah (Eng)'] = calculate_second_order_entropy(sefer_text)
        print(f"  Sefer Yetzirah (Eng):{results['Sefer Yetzirah (Eng)']:.4f} bits/bigram")
    except Exception as e:
        print(f"Error analyzing {SEFER_FILE}: {e}")
        results['Sefer Yetzirah (Eng)'] = None

    print("\n--- Summary ---")
    for name, value in results.items():
        if value is not None:
            print(f"  {name:<20}: {value:.4f}")
        else:
            print(f"  {name:<20}: ERROR")

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()