import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURATION ---
FILES_TO_ANALYZE = {
    "Voynich": "voynich_ready_nlp.txt",
    "Copiale_Eng": "copiale_english_translation.txt",
    "Sefer_Yetzirah_Eng": "sefer_yetzirah_english.txt"
}
OUTPUT_PREFIX = "zipf_plot" # Files will be zipf_plot_Voynich.png, etc.

# --- HELPER: Text Cleaning (same as entropy script) ---
def clean_text(text, language='english'):
    """Cleans text for Zipf analysis."""
    text = text.lower()
    start_marker = "*** start of this project gutenberg ebook"
    end_marker = "*** end of this project gutenberg ebook"
    start_idx = text.find(start_marker)
    if start_idx != -1: text = text[start_idx + len(start_marker):]
    end_idx = text.find(end_marker)
    if end_idx != -1: text = text[:end_idx]
    if language == 'german':
         text = re.sub(r'[^a-zäöüß\s]', '', text)
    else:
         text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def analyze_and_plot_zipf(file_key, filename):
    """
    Reads a file, calculates word frequencies, and plots Zipf's Law.
    """
    print(f"\n--- Analyzing Zipf's Law for: {file_key} ({filename}) ---")

    # --- Step 1: Read and Count ---
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
        # Determine language for cleaning based on key/filename (simple heuristic)
        lang = 'german' if 'german' in filename else 'english'
        if file_key == "Voynich": lang = 'voynich' # Special case for Voynich cleaning

        text = clean_text(raw_text, language=lang if lang != 'voynich' else 'english') # Use basic cleaning for Voynich

    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found. Skipping.")
        return

    words = text.split()
    if not words:
        print("ERROR: No words found after cleaning. Skipping.")
        return

    word_counts = Counter(words)
    print(f" -> Found {len(words)} total words, {len(word_counts)} unique types.")

    # --- Step 2: Get Ranks and Frequencies ---
    frequencies = sorted(word_counts.values(), reverse=True)
    ranks = list(range(1, len(frequencies) + 1))

    # --- Step 3: Plot on Log-Log Scale ---
    print("Generating log-log plot...")
    plt.figure(figsize=(10, 6))
    plt.plot(np.log10(ranks), np.log10(frequencies), marker='.', linestyle='None', markersize=4) # Smaller markers

    # Add trend line
    try:
        m, c = np.polyfit(np.log10(ranks), np.log10(frequencies), 1)
        y_fit = m * np.log10(ranks) + c
        plt.plot(np.log10(ranks), y_fit, color='red', linestyle='--', label=f'Trend (slope={m:.2f})')
        plt.legend()
    except Exception as e:
        print(f"Warning: Could not fit trend line: {e}")

    plt.title(f"Zipf's Law Plot for {file_key} (Log-Log Scale)", fontsize=16)
    plt.xlabel("Log10(Rank)", fontsize=12)
    plt.ylabel("Log10(Frequency)", fontsize=12)
    plt.grid(True, which="both", ls="--", linewidth=0.5)

    # Save the chart
    output_filename = f"{OUTPUT_PREFIX}_{file_key}.png"
    try:
        plt.savefig(output_filename)
        print(f"✅ Chart successfully saved to '{output_filename}'")
    except Exception as e:
        print(f"ERROR: Could not save chart '{output_filename}': {e}")
    plt.close() # Close the figure to free memory

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("Starting Comparative Zipf's Law Analysis...")
    for key, filename in FILES_TO_ANALYZE.items():
        analyze_and_plot_zipf(key, filename)
    print("\nComparative analysis complete.")