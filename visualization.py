import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

def generate_plot(dates, values, metric, output_path):
    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker="o")
    plt.title(f"{metric} Trend Over Time")
    plt.xlabel("Time")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
