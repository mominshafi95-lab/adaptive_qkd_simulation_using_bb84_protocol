import numpy as np
import sys
import os
import matplotlib.pyplot as plt

def plot_line(x, y, xlabel, ylabel, title):
    try:
        print("\n" + "="*70)
        print("[LINE PLOT] " + str(title))
        print("="*70)
        print("X-axis (" + str(xlabel) + "): " + str(len(x)) + " data points")
        print("Y-axis (" + str(ylabel) + "): " + str(len(y)) + " data points")
        print("\nStatistics for " + str(ylabel) + ":")
        y_array = np.asarray(y)
        print("  Min:    {:.6f}".format(float(np.min(y_array))))
        print("  Max:    {:.6f}".format(float(np.max(y_array))))
        print("  Mean:   {:.6f}".format(float(np.mean(y_array))))
        print("  Median: {:.6f}".format(float(np.median(y_array))))
        print("  StdDev: {:.6f}".format(float(np.std(y_array))))
        print("\nData Points:")
        for i in range(min(5, len(x))):
            print("  {0}={1:.6f}  ->  {2}={3:.6f}".format(str(xlabel), float(x[i]), str(ylabel), float(y[i])))
        if len(x) > 5:
            print("  ... ({} more points)".format(len(x)-5))
        print("="*70 + "\n")
        sys.stdout.flush()
    except Exception as e:
        print("[ERROR in plot_line]: " + str(e))
        sys.stdout.flush()

def plot_histogram(data, xlabel, ylabel, title):
    try:
        print("\n" + "="*70)
        print("[HISTOGRAM] " + str(title))
        print("="*70)
        data_array = np.asarray(data)
        print("Total samples: " + str(len(data)))
        print("\nStatistics:")
        print("  Min:    {:.6f}".format(float(np.min(data_array))))
        print("  Max:    {:.6f}".format(float(np.max(data_array))))
        print("  Mean:   {:.6f}".format(float(np.mean(data_array))))
        print("  Median: {:.6f}".format(float(np.median(data_array))))
        print("  StdDev: {:.6f}".format(float(np.std(data_array))))
        print("="*70 + "\n")
        sys.stdout.flush()
    except Exception as e:
        print("[ERROR in plot_histogram]: " + str(e))
        sys.stdout.flush()

def plot_bar(labels, values, xlabel, ylabel, title):
    try:
        print("\n" + "="*70)
        print("[BAR CHART] " + str(title))
        print("="*70)
        print("Categories: " + str(len(labels)))
        print("\nBar Chart Data:")
        values_array = np.asarray(values)
        max_val = float(np.max(values_array)) if len(values_array) > 0 else 1
        for label, value in zip(labels, values):
            bar_length = int((float(value) / max_val) * 40) if max_val > 0 else 0
            bar = "#" * bar_length
            print("  {0:<15}: {1:<40} {2:>10.6f}".format(str(label), bar, float(value)))
        print("\nStatistics:")
        print("  Sum:  {:.6f}".format(float(np.sum(values_array))))
        print("  Mean: {:.6f}".format(float(np.mean(values_array))))
        print("  Max:  {:.6f}".format(float(np.max(values_array))))
        print("  Min:  {:.6f}".format(float(np.min(values_array))))
        print("="*70 + "\n")
        sys.stdout.flush()
    except Exception as e:
        print("[ERROR in plot_bar]: " + str(e))
        sys.stdout.flush()


def _ensure_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass


def save_line_plot(x, y, xlabel, ylabel, title, filename, dpi=300, figsize=(8,4)):
    """Save a publication-quality line plot to disk and return the file path.

    Parameters
    - x, y: data sequences
    - xlabel, ylabel, title: labels
    - filename: full output path (including extension)
    - dpi: resolution
    - figsize: figure size in inches
    """
    try:
        _ensure_dir(os.path.dirname(filename) or '.')
        plt.style.use('seaborn-v0_8')
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(x, y, marker='o', linewidth=2, markersize=5)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, linestyle='--', alpha=0.6)
        fig.tight_layout()
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved plot: {filename}")
        return filename
    except Exception as e:
        print(f"[ERROR in save_line_plot]: {e}")
        return None


def save_performance_plots(noise_levels, qbers, key_rates, outdir='output/plots', prefix='performance'):
    """Generate and save QBER, Key Rate, and combined performance plots.

    Returns a dict of created file paths.
    """
    _ensure_dir(outdir)
    results = {}
    try:
        qber_file = os.path.join(outdir, f"{prefix}_qber.png")
        kr_file = os.path.join(outdir, f"{prefix}_keyrate.png")
        combo_file = os.path.join(outdir, f"{prefix}_combined.png")

        save_line_plot(noise_levels, qbers, 'Noise Probability', 'QBER', 'QBER vs Noise', qber_file)
        save_line_plot(noise_levels, key_rates, 'Noise Probability', 'Secure Key Rate', 'Secure Key Rate vs Noise', kr_file)

        # Combined figure with twin y-axis
        plt.style.use('seaborn-v0_8')
        fig, ax1 = plt.subplots(figsize=(9,5))
        ax1.plot(noise_levels, qbers, 'C0-o', label='QBER')
        ax1.set_xlabel('Noise Probability')
        ax1.set_ylabel('QBER', color='C0')
        ax1.tick_params(axis='y', labelcolor='C0')
        ax2 = ax1.twinx()
        ax2.plot(noise_levels, key_rates, 'C1-s', label='Secure Key Rate')
        ax2.set_ylabel('Secure Key Rate', color='C1')
        ax2.tick_params(axis='y', labelcolor='C1')
        ax1.grid(True, linestyle='--', alpha=0.4)
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='best')
        fig.tight_layout()
        fig.savefig(combo_file, dpi=300, bbox_inches='tight')
        plt.close(fig)

        results['qber'] = qber_file
        results['key_rate'] = kr_file
        results['combined'] = combo_file
        print(f"Saved performance plots to: {outdir}")
    except Exception as e:
        print(f"[ERROR in save_performance_plots]: {e}")
    return results


def save_histogram(data, xlabel, ylabel, title, filename, bins=30, dpi=300, figsize=(6,4)):
    try:
        _ensure_dir(os.path.dirname(filename) or '.')
        plt.style.use('seaborn-v0_8')
        fig, ax = plt.subplots(figsize=figsize)
        ax.hist(data, bins=bins, color='C0', edgecolor='black', alpha=0.7)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(False)
        fig.tight_layout()
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved histogram: {filename}")
        return filename
    except Exception as e:
        print(f"[ERROR in save_histogram]: {e}")
        return None


def save_bar_chart(labels, values, xlabel, ylabel, title, filename, dpi=300, figsize=(8,4)):
    try:
        _ensure_dir(os.path.dirname(filename) or '.')
        plt.style.use('seaborn-v0_8')
        fig, ax = plt.subplots(figsize=figsize)
        ax.bar(labels, values, color='C2', edgecolor='black', alpha=0.8)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        fig.tight_layout()
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved bar chart: {filename}")
        return filename
    except Exception as e:
        print(f"[ERROR in save_bar_chart]: {e}")
        return None



