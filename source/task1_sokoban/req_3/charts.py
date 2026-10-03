import csv
import os
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(CURRENT_DIR, "results")
CSV_PATH = os.path.join(RESULTS_DIR, "sokoban_results.csv")

ALGORITHMS = ("UCS", "A*")
COLORS = {"UCS": "#4C72B0", "A*": "#DD8452"}


def load_rows(path=CSV_PATH):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def aggregate(rows, column):
    """Trả về {(map, algo): (trung bình, min, max)} của một cột số."""
    grouped = {}
    for row in rows:
        grouped.setdefault((row["Map"], row["Algorithm"]), []).append(float(row[column]))
    return {
        key: (statistics.mean(v), min(v), max(v))
        for key, v in grouped.items()
    }


def map_names(rows):
    names = []
    for row in rows:
        if row["Map"] not in names:
            names.append(row["Map"])
    return names


def draw_grouped_bars(ax, rows, column, title, ylabel, with_range=False):
    maps = map_names(rows)
    stats = aggregate(rows, column)
    width = 0.38

    for i, algo in enumerate(ALGORITHMS):
        xs = [j + (i - 0.5) * width for j in range(len(maps))]
        means = [stats[(m, algo)][0] for m in maps]
        bars = ax.bar(xs, means, width, label=algo, color=COLORS[algo])

        if with_range:
            lows = [means[k] - stats[(m, algo)][1] for k, m in enumerate(maps)]
            highs = [stats[(m, algo)][2] - means[k] for k, m in enumerate(maps)]
            ax.errorbar(xs, means, yerr=[lows, highs], fmt="none",
                        ecolor="black", capsize=3, linewidth=1)

        for bar, value in zip(bars, means):
            label = f"{value:,.0f}" if value >= 10 else f"{value:.1f}"
            ax.annotate(label, (bar.get_x() + bar.get_width() / 2, value),
                        ha="center", va="bottom", fontsize=8,
                        xytext=(0, 2), textcoords="offset points")

    ax.set_yscale("symlog", linthresh=1)
    ax.set_ylim(bottom=0)
    ax.set_xticks(range(len(maps)))
    ax.set_xticklabels([m.replace(".txt", "") for m in maps], rotation=15, ha="right")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.legend()


CHARTS = [
    ("req3_expanded_nodes.png", "Expanded_Nodes",
     "Số node được mở rộng (UCS vs A*)", "Expanded nodes (thang symlog)", False),
    ("req3_generated_nodes.png", "Generated_Nodes",
     "Số node được sinh ra (UCS vs A*)", "Generated nodes (thang symlog)", False),
    ("req3_time.png", "Time_ms",
     "Thời gian tìm kiếm trung bình (thanh sai số = min–max)", "Time (ms, thang symlog)", True),
    ("req3_max_frontier.png", "Max_Frontier_Size",
     "Kích thước frontier lớn nhất (UCS vs A*)", "Max frontier size (thang symlog)", False),
]


def make_charts(rows=None, out_dir=RESULTS_DIR):
    if rows is None:
        rows = load_rows()
    os.makedirs(out_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    for ax, (_, column, title, ylabel, with_range) in zip(axes.flat, CHARTS):
        draw_grouped_bars(ax, rows, column, title, ylabel, with_range)
    fig.suptitle("Req 3 – So sánh UCS và A*", fontsize=14)
    fig.tight_layout()
    path = os.path.join(out_dir, "req3_overview.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return [path]


if __name__ == "__main__":
    for p in make_charts():
        print("Saved:", p)
