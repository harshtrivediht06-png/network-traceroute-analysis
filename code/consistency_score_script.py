import os
import re
import matplotlib.pyplot as plt
import numpy as np

def parse_report_file(file_path):
    """
    Reads a multi-run traceroute file, extracts all numerical RTTs,
    and returns a clean list of all measured probes.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: File '{file_path}' not found. Skipping...")
        return None

    all_probes = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the file by the "Run X" headers we injected
    runs = re.split(r'Run \d+', content)[1:]
    
    for run in runs:
        for line in run.strip().split('\n'):
            # Look for lines starting with a hop number followed by latency text
            match = re.search(r'^\s*(\d+)\s+(.+)$', line)
            if match:
                # Find all numbers followed immediately by 'ms'
                ms_values = [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*ms', match.group(2))]
                all_probes.extend(ms_values)
                
    return all_probes

# 1. Target files to scan (Amazon added)
report_files = {
    'GitHub': 'github_report.txt',
    'YouTube': 'youtube_report.txt',
    'Instagram': 'instagram_report.txt',
    'Amazon': 'amazon_report.txt'
}

# 2. Process metrics dynamically from the text files
labels = []
average_rtts = []
consistency_scores = []
colors = []

# Mapping styles for consistency matching (Amazon official brand color added)
color_map = {
    'GitHub': '#1f77b4', 
    'YouTube': '#d62728', 
    'Instagram': '#e1306c',
    'Amazon': '#ff9900'
}

print("=== AUTOMATED FILE PROCESSING & CONSISTENCY REPORT ===")
print(f"{'Target Website':<18}{'Total Probes Extracted':<24}{'Mean RTT (ms)':<16}{'Consistency / Jitter (ms)':<20}")
print("-" * 80)

for target, file_name in report_files.items():
    probe_data = parse_report_file(file_name)
    
    if probe_data:
        mean_rtt = np.mean(probe_data)
        # Calculate consistency score via standard deviation formula
        jitter_score = np.std(probe_data)
        
        labels.append(target)
        average_rtts.append(mean_rtt)
        consistency_scores.append(jitter_score)
        colors.append(color_map[target])
        
        print(f"{target:<18}{len(probe_data):<24}{mean_rtt:<16.2f}{jitter_score:<20.2f}")

# 3. Present the Data Visually if files were parsed successfully
if consistency_scores:
    fig, ax = plt.subplots(figsize=(11, 6))
    
    # Generate bar layout (Lower score indicates superior, more tightly bound consistency)
    bars = ax.bar(labels, consistency_scores, color=colors, alpha=0.85, width=0.4)
    
    # Place numeric data labels perfectly on top of each bar structure
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f} ms',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', weight='bold')

    # UI design and grid scaling
    ax.set_title("Long-Term Network Consistency Score (From Log Files)", fontsize=14, pad=15, weight='bold')
    ax.set_ylabel("Consistency Score / Jitter Standard Deviation (ms)", fontsize=12)
    ax.set_xlabel("Monitored Target Website Environments", fontsize=12, labelpad=10)
    ax.grid(True, linestyle=':', alpha=0.5, axis='y')
    ax.set_ylim(0, max(consistency_scores) + 5)
    
    plt.tight_layout()
    plt.show()
else:
    print("\n❌ Error: No data could be compiled. Please ensure you ran your loop scripts first.")
