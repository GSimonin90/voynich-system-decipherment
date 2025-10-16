import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io

# --- Data from dialect_quantification.csv ---
# We embed the data directly into the script for simplicity.
csv_data = """
concept,freq_A_per_1000,freq_B_per_1000
aii,131.39,83.01
che,71.56,82.73
cho,53.33,29.57
ol,30.39,70.61
kch,35.19,17.56
teo,6.21,9.66
f,0.43,0.36
et,0.33,0.26
yk,1.28,0.57
ro,0.29,0.28
tai,6.45,5.16
ek,0.24,0.62
"""

# Read the data into a pandas DataFrame
data = pd.read_csv(io.StringIO(csv_data))

# --- Combine 'et' and 'yk' into a single "Root Concepts" category ---
et_yk_a = data[data['concept'].isin(['et', 'yk'])]['freq_A_per_1000'].sum()
et_yk_b = data[data['concept'].isin(['et', 'yk'])]['freq_B_per_1000'].sum()

# Remove old rows and add the new combined row
data = data[~data['concept'].isin(['et', 'yk'])]
new_row = pd.DataFrame([{'concept': 'et/yk (Root)', 'freq_A_per_1000': et_yk_a, 'freq_B_per_1000': et_yk_b}])
data = pd.concat([new_row, data]).reset_index(drop=True)


# --- Select and reorder concepts for the chart for better storytelling ---
concepts_to_plot = [
    'aii', 'ol', 'kch', 'teo',  # Planetary/Abstract
    'f', 'et/yk (Root)',       # Physical/Botanical
    'che', 'cho'               # Material
]
plot_data = data[data['concept'].isin(concepts_to_plot)].set_index('concept').reindex(concepts_to_plot)


# --- Chart Generation ---
labels = plot_data.index
freq_a = plot_data['freq_A_per_1000']
freq_b = plot_data['freq_B_per_1000']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

# Create the plot
fig, ax = plt.subplots(figsize=(12, 7))
rects1 = ax.bar(x - width/2, freq_a, width, label='Dialect A (Fundamental)', color='#00796b')
rects2 = ax.bar(x + width/2, freq_b, width, label='Dialect B (Applied)', color='#80cbc4')

# Add some text for labels, title and axes ticks
ax.set_ylabel('Frequency per 1,000 Roots')
ax.set_title('Dialect Fingerprint: Quantitative Comparison of Key Concepts', fontsize=16, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.legend()

# Add value labels on top of the bars
ax.bar_label(rects1, padding=3, fmt='%.2f')
ax.bar_label(rects2, padding=3, fmt='%.2f')

# Improve layout and save the file
fig.tight_layout()
plt.savefig('appendix_C_chart.png', dpi=300)

print("Chart 'appendix_C_chart.png' has been successfully generated.")