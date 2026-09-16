import matplotlib.pyplot as plt
import numpy as np

# Total calculated average end-to-end RTT (ms) per run iteration from your data
runs = [1, 2, 3, 4, 5]
github_run_rtt = [22.1, 21.4, 21.8, 20.9, 21.6]
youtube_run_rtt = [24.3, 21.0, 23.8, 22.1, 23.5]
instagram_run_rtt = [48.2, 44.1, 46.5, 47.0, 45.8]
amazon_run_rtt = [226.4, 207.1, 227.0, 215.3, 221.9]

plt.figure(figsize=(11, 6), facecolor='#f8f9fa')
ax = plt.axes()
ax.set_facecolor('#ffffff')

# Plot variations across runs
plt.plot(runs, github_run_rtt, marker='o', linewidth=2, color='#1f77b4', label='GitHub (Mumbai)')
plt.plot(runs, youtube_run_rtt, marker='s', linewidth=2, color='#d62728', label='YouTube (Mumbai)')
plt.plot(runs, instagram_run_rtt, marker='^', linewidth=2, color='#e1306c', label='Instagram (Delhi)')
plt.plot(runs, amazon_run_rtt, marker='d', linewidth=2.5, color='#ff9900', label='Amazon (International)')

# Emphasize Amazon's trans-oceanic axis shift nicely with a break or log label if desired
plt.yscale('log')
ax.set_yticks([10, 20, 30, 50, 100, 230])
ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())

plt.title("RTT Latency Variation Across Repeated Runs", fontsize=14, pad=15, weight='bold')
plt.xlabel("Repeated Run Execution Number", fontsize=12, labelpad=10)
plt.ylabel("Total End-to-End Latency (ms) [Log Scaled]", fontsize=12)
plt.xticks(runs)
plt.grid(True, which="both", linestyle=':', alpha=0.5)
plt.legend(loc='center left', frameon=True, shadow=True)

plt.savefig('rtt_variation_across_runs.png', dpi=300, bbox_inches='tight')
plt.tight_layout()
plt.show()
