import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Configuration ---
INPUT_CSV_FILE = "thematic_analysis_results.csv"
OUTPUT_IMAGE_FILE = "thematic_heatmap.png"

def create_thematic_heatmap(csv_path, output_path):
    """
    Loads the thematic analysis results from a CSV file and generates
    a heatmap visualization of the lift scores.
    """
    print(f"Reading data from '{csv_path}'...")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Input file '{csv_path}' not found. Please ensure the file is in the same directory.")
        return

    # Prepare the data for the heatmap.
    # We set the 'Root' column as the index for the rows.
    heatmap_data = df.set_index('Root')
    
    # Select only the columns containing the lift scores.
    lift_columns = [col for col in heatmap_data.columns if 'Lift_' in col]
    heatmap_data = heatmap_data[lift_columns]
    
    # Clean up column names for better readability on the chart's x-axis.
    heatmap_data.columns = [col.replace('Lift_', '') for col in heatmap_data.columns]
    
    # Ensure all data is numeric, converting any non-numeric values to NaN.
    heatmap_data = heatmap_data.apply(pd.to_numeric, errors='coerce')

    print("Generating heatmap...")
    # Set the figure size to ensure all labels are readable.
    plt.figure(figsize=(12, 18))
    
    # Create the heatmap using the seaborn library.
    sns.heatmap(
        heatmap_data,
        annot=True,         # Display the lift scores on each cell.
        cmap="viridis",     # Use a color scheme that clearly shows high (yellow) and low (purple) values.
        linewidths=.5,      # Add thin lines between cells.
        fmt=".2f"           # Format the annotation numbers to two decimal places.
    )
    
    # Set titles and labels for clarity.
    plt.title('Thematic Lift Score Analysis of Voynich Manuscript Roots', fontsize=16)
    plt.xlabel('Thematic Sections', fontsize=12)
    plt.ylabel('Conceptual Roots', fontsize=12)
    
    # Rotate labels to prevent them from overlapping.
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Adjust layout to fit everything neatly.
    plt.tight_layout()

    # Save the generated plot to an image file.
    plt.savefig(output_path)
    print(f"Success! Heatmap has been saved as '{output_path}'.")


if __name__ == "__main__":
    create_thematic_heatmap(INPUT_CSV_FILE, OUTPUT_IMAGE_FILE)