import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import defaultdict

# --- CONFIGURATION ---
INPUT_FILE = "process_finder_v5_output.txt"
OUTPUT_CHART = "process_by_section_barchart.png"

def parse_summary_and_plot_v2():
    """
    Reads the 'Statistical Summary' from the v5 output file,
    parses it using the CORRECT (Section-first) logic,
    and generates a grouped bar chart.
    """
    print(f"Reading summary from '{INPUT_FILE}'...")
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Input file '{INPUT_FILE}' not found.")
        return

    # --- Step 1: Parse the Summary Section (Corrected v2 Logic) ---
    results_list = []
    in_summary_section = False
    current_section = None
    
    # Regex to find the Section header
    section_regex = re.compile(r"^Section:\s*(.*)$")
    # Regex to find the process data line
    data_regex = re.compile(r"^\s*-\s*(.*?):\s*(\d+)\s*matches$")

    print("Parsing 'Statistical Summary' (v2 Section-first logic)...")
    for line in lines:
        stripped_line = line.strip()
        
        if "Statistical Summary" in stripped_line:
            in_summary_section = True
            continue
            
        # Stop parsing if we hit the "Partial Matches" section
        if "Partial Matches" in stripped_line:
            in_summary_section = False
            break
            
        if in_summary_section:
            # Check for a new Section header
            section_match = section_regex.match(stripped_line)
            if section_match:
                current_section = section_match.group(1).strip()
                # print(f"DEBUG: Found section '{current_section}'") # Debug line
                continue
                
            # Check for data line
            data_match = data_regex.match(stripped_line)
            if data_match and current_section:
                process_name = data_match.group(1).strip()
                count = int(data_match.group(2))
                
                # Add to our results
                results_list.append({
                    "ProcessName": process_name,
                    "Section": current_section,
                    "Count": count
                })
                # print(f"DEBUG: Logged '{process_name}' in '{current_section}' with count {count}") # Debug line

    if not results_list:
        print("ERROR: Could not parse any data from the 'Statistical Summary'.")
        print("Please check the format of 'process_finder_v5_output.txt'.")
        return

    print(f"Successfully parsed {len(results_list)} data points from summary.")

    # --- Step 2: Create DataFrame ---
    df = pd.DataFrame(results_list)

    # --- Step 3: Plot the Grouped Chart (Unchanged) ---
    print(f"Generating grouped bar chart...")

    sns.set(style="whitegrid")
    
    # Sort the chart categories by total count
    total_counts = df.groupby('ProcessName')['Count'].sum()
    sorted_processes = total_counts.sort_values(ascending=False).index
    
    num_processes = len(sorted_processes)
    fig_height = max(6, num_processes * 1.2)
    
    plt.figure(figsize=(12, fig_height))
    
    ax = sns.barplot(
        x='Count',
        y='ProcessName',
        hue='Section',
        data=df,
        order=sorted_processes,
        palette="viridis"
    )
    
    ax.set_title(
        'Process Signatures by Section (Herbal vs. Balneological)',
        fontsize=16,
        fontweight='bold'
    )
    ax.set_xlabel('Number of Paragraphs (Matches)', fontsize=12)
    ax.set_ylabel('Process Signature', fontsize=12)
    
    sns.move_legend(ax, "lower right")
    
    # Add data labels
    for p in ax.patches:
        width = p.get_width()
        if width > 0:
            ax.annotate(
                f'{int(width)}',
                (width, p.get_y() + p.get_height() / 2),
                ha='left',
                va='center',
                xytext=(5, 0),
                textcoords='offset points',
                fontsize=9
            )

    plt.tight_layout()
    
    try:
        plt.savefig(OUTPUT_CHART)
        print(f"✅ Grouped bar chart successfully saved to '{OUTPUT_CHART}'")
    except Exception as e:
        print(f"ERROR: Could not save the chart image: {e}")

if __name__ == "__main__":
    parse_summary_and_plot_v2()