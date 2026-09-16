import os
import re
import matplotlib.pyplot as plt
import numpy as np

def parse_logs_for_envelope(file_path):
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    runs = re.split(r'Run \d+', content)[1:]
    hop_data_map = {}

    for run in runs:
        for line in run.strip().split('\n'):
            match = re.search(r'^\s*(\d+)\s+(.+)$', line)
            if match:
                hop_num = int(match.group(1))
                ms_values = [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*ms', match.group(2))]
                if ms_values:
                    hop_data_map.setdefault(hop_num, []).extend(ms_values)

    sorted_hops = sorted(hop_data_map.keys())
    avgs = [np.mean(hop_data_map[h]) for h in sorted_hops]
    mins = [np.min(hop_data_map[h]) for h in sorted_hops]
    maxs = [np.max(hop_data_map[h]) for h in sorted_hops]
    jitters = [np.std(hop_data_map[h]) for h in sorted_hops]
    
    return {
        'hops': sorted_hops, 'avg': avgs, 'min': mins, 'max': maxs, 'jitter': np.mean(jitters) if jitters else 0.0
    }

# Data ingestion config
report_files = {
    'GitHub': 'github_report.txt', 'YouTube': 'youtube_report.txt',
    'Instagram': 'instagram_report.txt', 'Amazon': 'amazon_report.txt'
}

processed_metrics = {}
for target, file_name in report_files.items():
    metrics = parse_logs_for_envelope(file_name)
    if metrics:
        processed_metrics[target] = metrics

# Setup high-clarity canvas
plt.figure(figsize=(14, 8), facecolor='#f8f9fa')
ax = plt.axes()
ax.set_facecolor('#ffffff')

colors = {'GitHub': '#1f77b4', 'YouTube': '#d62728', 'Instagram': '#e1306c', 'Amazon': '#ff9900'}
markers = {'GitHub': 'o', 'YouTube': 's', 'Instagram': '^', 'Amazon': 'd'}
styles = {'GitHub': '-', 'YouTube': '--', 'Instagram': '-.', 'Amazon': ':'}

for target, metrics in processed_metrics.items():
    # Plot core average lines
    plt.plot(metrics['hops'], metrics['avg'], marker=markers[target], linestyle=styles[target], 
             color=colors[target], linewidth=2.5, markersize=7,
             label=f"{target} (Avg Jitter: {metrics['jitter']:.2f} ms)")
    
    # Clean transparent stability shaded bands
    plt.fill_between(metrics['hops'], metrics['min'], metrics['max'], color=colors[target], alpha=0.08)

# CRITICAL ENHANCEMENT: Symmetrical Logarithmic Scale for the Latency Axis
# Spreads out low latency values (1-40ms) while cleanly capturing the 220ms global threshold
ax.set_yscale('symlog', linthresh=10)

# Format axes and grid profiles cleanly
plt.title("High-Clarity Latency & Stability Topology", fontsize=16, pad=20, weight='bold', color='#212529')
plt.xlabel("Network Hop Number (Router Chain Index)", fontsize=12, labelpad=10, weight='bold')
plt.ylabel("Round-Trip Time Latency (ms) [Log Scaled]", fontsize=12, labelpad=10, weight='bold')

# Customize specific manual axis tick overrides to read log scale easily
ax.set_yticks([1, 2, 5, 10, 20, 50, 100, 220, 300])
ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())
plt.xticks(range(1, 21))

plt.grid(True, which="both", linestyle=':', alpha=0.4, color='#6c757d')
plt.legend(loc='upper left', fontsize=11, frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', shadow=True)

# Save chart automatically to project root folder as image asset
plt.savefig('enhanced_network_profile.png', dpi=300, bbox_inches='tight')
plt.tight_layout()
plt.show()
