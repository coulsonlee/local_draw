import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- 用户可配置 ----------
save_path = "figure.pdf"
# -----------------------------------

# Style
sns.set_theme(
    style="whitegrid",
    rc={
        "legend.framealpha": 1,
        "legend.facecolor": "white"
    }
)
plt.rcParams['font.size'] = 15

# Data —— 横坐标每 5 一点，数据稍微扰动，不完全直线
concepts = np.arange(5, 55, 5)
ft_acc = np.array([28.5, 26.8, 25.2, 23.1, 21.5, 19.9, 17.4, 15.8, 13.3, 10.9])
esd_acc = np.array([75.2, 70.4, 62.0, 56.0, 51.9, 49.3, 48.7, 46.3, 43.2, 42.1])
ft_time = np.array([60, 117, 180, 234, 287, 351, 414, 468, 525, 585])
esd_time = np.array([90, 108, 150, 200.6, 250, 299.2, 350, 398.7, 450, 493.9])

# 使用 colorblind 调色板的前两个颜色
palette = sns.color_palette("colorblind", 2)
color_acc, color_time = palette[1], palette[0]  # acc 用第二色，time 用第一色
lw = 2.5

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

# Plot Acc (solid circles)
ax1.plot(
    concepts, esd_acc, 'o-',
    lw=lw, color=color_acc,
    markeredgecolor='black', markeredgewidth=1.2,
    label='ESD Acc (%)'
)
ax1.plot(
    concepts, ft_acc, 'o-',
    lw=lw, color=color_acc,
    markeredgecolor='black', markeredgewidth=1.2,
    label='MACE Acc (%)'
)
ax1.set_ylabel('Forgetting Accuracy (%)', color=color_acc)

# Plot Time (dashed triangles)
ax2.plot(
    concepts, esd_time, '^--',
    lw=lw, color=color_time,
    markeredgecolor='black', markeredgewidth=1.2,
    label='ESD Time (min)'
)
ax2.plot(
    concepts, ft_time, '^--',
    lw=lw, color=color_time,
    markeredgecolor='black', markeredgewidth=1.2,
    label='MACE Time (min)'
)
ax2.set_ylabel('Running Time (min)', color=color_time)

# 统一设置坐标轴刻度颜色
ax1.tick_params(axis='y', colors=color_acc)
ax2.tick_params(axis='y', colors=color_time)

# 左轴：0–100，每 20 刻度
ax1.set_ylim(0, 100)
ax1.set_yticks(np.arange(0, 101, 20))

# 右轴：1–600，刻度 [1,120,...,600]
ax2.set_ylim(1, 600)
ax2.set_yticks([1] + list(range(120, 601, 120)))

# X 轴：每 5 一刻度
ax1.set_xlabel('Number of Concepts')
ax1.set_xticks(concepts)

# Legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
leg = ax1.legend(
    h1 + h2, l1 + l2,
    loc='upper left',
    frameon=True, fontsize=10
)
leg.get_frame().set_facecolor('white')
leg.get_frame().set_alpha(1)

# 网格 & 边框
ax1.grid(axis='y', linestyle='--', alpha=0.9)
ax1.grid(False, axis='x')
ax2.grid(False)
for spine in ['top', 'right']:
    ax1.spines[spine].set_visible(False)

fig.tight_layout()
fig.savefig(save_path, format="pdf", bbox_inches="tight")
plt.show()
