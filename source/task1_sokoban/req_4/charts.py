import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(CURRENT_DIR, "results")
CSV_PATH = os.path.join(RESULTS_DIR, "heuristic_results.csv")
PROPERTIES = ("GoalZero", "Admissibility", "Consistency")
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]


def load_rows(path=CSV_PATH):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def is_pass(row):
    return row["Pass"] == "True"


def short(map_name):
    return map_name.replace(".txt", "")


def map_names(rows):
    names = []
    for row in rows:
        if row["Map"] not in names:
            names.append(row["Map"])
    return names


def plot_pass_counts(ax, rows):
    """Số mẫu đạt / không đạt cho từng tính chất."""
    totals = {p: [0, 0] for p in PROPERTIES}
    for row in rows:
        totals[row["Property"]][0 if is_pass(row) else 1] += 1

    passed = [totals[p][0] for p in PROPERTIES]
    failed = [totals[p][1] for p in PROPERTIES]

    ax.bar(PROPERTIES, passed, label="Đạt", color="#55A868")
    ax.bar(PROPERTIES, failed, bottom=passed, label="Không đạt", color="#C44E52")
    for i in range(len(PROPERTIES)):
        total = passed[i] + failed[i]
        ax.annotate(f"{passed[i]}/{total}", (i, total), ha="center", va="bottom",
                    xytext=(0, 3), textcoords="offset points", fontsize=10)
    ax.set_ylabel("Số mẫu kiểm tra")
    ax.set_title("Kết quả kiểm tra GoalZero / Admissibility / Consistency")
    ax.set_ylim(0, max(p + f for p, f in zip(passed, failed)) * 1.12)
    ax.legend()
    ax.grid(axis="y", linestyle=":", alpha=0.5)


def plot_h_vs_hstar(ax, rows):
    """Scatter h(s) và h*(s); admissible nghĩa là mọi điểm nằm dưới y = x."""
    adm = [r for r in rows if r["Property"] == "Admissibility"]
    top = 0
    for color, m in zip(PALETTE, map_names(adm)):
        pts = [(float(r["h_star"]), float(r["h_s"])) for r in adm if r["Map"] == m]
        ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=28, alpha=0.7,
                   color=color, label=f"{short(m)} (n={len(pts)})")
        top = max(top, max(max(p) for p in pts))

    top += 2
    ax.plot([0, top], [0, top], "k--", linewidth=1, label="h = h*")
    ax.fill_between([0, top], [0, top], top, color="#C44E52", alpha=0.08)
    ax.text(top * 0.05, top * 0.88, "Vùng vi phạm (h > h*)", color="#C44E52", fontsize=9)
    ax.set_xlim(0, top)
    ax.set_ylim(0, top)
    ax.set_xlabel("h*(s) – chi phí tối ưu thật (UCS)")
    ax.set_ylabel("h(s) – giá trị heuristic")
    ax.set_title("Admissibility: h(s) so với h*(s)")
    ax.legend(loc="center left", fontsize=8)
    ax.grid(linestyle=":", alpha=0.5)


def plot_tightness(ax, rows):
    """Trung bình h so với trung bình h* theo map (đánh giá độ chặt)."""
    adm = [r for r in rows if r["Property"] == "Admissibility"]
    maps = map_names(adm)
    mean_h = []
    mean_hstar = []
    for m in maps:
        sub = [r for r in adm if r["Map"] == m]
        mean_h.append(sum(float(r["h_s"]) for r in sub) / len(sub))
        mean_hstar.append(sum(float(r["h_star"]) for r in sub) / len(sub))

    width = 0.38
    xs = list(range(len(maps)))
    b1 = ax.bar([x - width / 2 for x in xs], mean_h, width,
                label="h(s) trung bình", color="#4C72B0")
    b2 = ax.bar([x + width / 2 for x in xs], mean_hstar, width,
                label="h*(s) trung bình", color="#DD8452")
    for bars in (b1, b2):
        for bar in bars:
            ax.annotate(f"{bar.get_height():.1f}",
                        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        ha="center", va="bottom", fontsize=8,
                        xytext=(0, 2), textcoords="offset points")
    ax.set_xticks(xs)
    ax.set_xticklabels([short(m) for m in maps], rotation=15, ha="right")
    ax.set_ylabel("Chi phí")
    ax.set_title("Độ chặt: h trung bình so với h* trung bình")
    ax.legend()
    ax.grid(axis="y", linestyle=":", alpha=0.5)


def plot_consistency_slack(ax, rows):
    """Phân bố slack = cost + h(s') - h(s); consistent khi slack >= 0."""
    cons = [r for r in rows if r["Property"] == "Consistency"]
    slack = [float(r["cost"]) + float(r["h_next"]) - float(r["h_s"]) for r in cons]
    lo, hi = int(min(slack)), int(max(slack))

    ax.hist(slack, bins=range(lo, hi + 2), align="left", rwidth=0.85, color="#55A868")
    ax.axvline(-0.5, color="#C44E52", linestyle="--", label="Ngưỡng vi phạm (slack < 0)")
    ax.set_xlabel("slack = cost(s, s') + h(s') − h(s)")
    ax.set_ylabel("Số cạnh chuyển trạng thái")
    ax.set_title(f"Consistency: phân bố slack trên {len(slack)} cạnh (min = {min(slack):.0f})")
    ax.set_xticks(range(lo, hi + 1))
    ax.legend()
    ax.grid(axis="y", linestyle=":", alpha=0.5)


def make_charts(rows=None, out_dir=RESULTS_DIR):
    if rows is None:
        rows = load_rows()
    os.makedirs(out_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plot_pass_counts(axes[0][0], rows)
    plot_h_vs_hstar(axes[0][1], rows)
    plot_tightness(axes[1][0], rows)
    plot_consistency_slack(axes[1][1], rows)
    fig.suptitle("Req 4 – Phân tích heuristic (admissible & consistent)", fontsize=14)
    fig.tight_layout()
    path = os.path.join(out_dir, "req4_overview.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return [path]


if __name__ == "__main__":
    for p in make_charts():
        print("Saved:", p)
