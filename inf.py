import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

# ---------- 用户可配置 ----------
use_smooth = False   # True: 平滑拟合；False: 原始连线
save_dir = 'save'
# -----------------------------------

# 创建保存目录
os.makedirs(save_dir, exist_ok=True)

# X 轴标签及等距位置
def get_positions(labels):
    return np.arange(len(labels))

X_labels = ["20","30","40","50","60","70","80","90"]
positions = get_positions(X_labels)

# Clip Score 数据
clip_data = {
    'No Sparsity ESD': [70.4, 70.4, 70.4, 70.4, 70.4, 70.4, 70.4, 70.4],
    'ESD':            [70.4, 71.3 ,74.10, 72.38,70.2,68.4,67.33, 54.3],
    'No Sparsity SPM':[47.0, 47.0, 47.0, 47.0, 47.0, 47.0, 47.0, 47.0],
    'SPM':            [47.0,48.2 ,50.3, 53.2,46.1,44.4, 41.1, 38.2],
    'No Sparsity MACE':[27.3, 27.3, 27.3, 27.3, 27.3, 27.3, 27.3, 27.3],
    'MACE':           [27.3,28.9, 30.4, 31.1,27.7,25.4,24.3, 20.1],
}
print("data_collecet finished")
# 定义分组及对应属性
groups = {
    'ESD': ['No Sparsity ESD', 'ESD'],
    'SPM': ['No Sparsity SPM', 'SPM'],
    'MACE': ['No Sparsity MACE', 'MACE'],
}
markers = {'ESD': 'o', 'MACE': 's', 'SPM': '^'}
print("group is set to be correct method finished")
# 全局样式
sns.set_theme(style="whitegrid", rc={
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 'small'
})
# 调色板，按组数
palette = sns.color_palette("colorblind", len(groups))

group_colors = dict(zip(groups.keys(), palette))

# 创建画布
fig, ax = plt.subplots(figsize=(6.5, 5))

# 绘制数据
for grp, methods in groups.items():
    color = group_colors[grp]
    marker = markers[grp]
    for name in methods:
        y = clip_data[name]
        linestyle = '--' if name.startswith('No Sparsity') else '-'
        if use_smooth:
            x_np = np.array(positions)
            x_smooth = np.linspace(x_np.min(), x_np.max(), 300)
            coeffs = np.polyfit(x_np, y, 2)
            ax.plot(x_smooth, np.polyval(coeffs, x_smooth), linestyle=linestyle,
                    linewidth=1.75, color=color)
            ax.scatter(positions, y, marker=marker, s=80, color=color,
                       edgecolor='black', linewidth=1.2)
        else:
            ax.plot(positions, y, marker=marker, linestyle=linestyle,
                    linewidth=1.75, markersize=8, color=color,
                    markeredgecolor='black', markeredgewidth=1.2)

# 坐标轴与刻度
ax.set_xlabel('Sparsity (%)')
ax.set_ylabel('Unlearning Accuracy (%)')
ax.set_xticks(positions)
ax.set_xticklabels(X_labels)
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set_fontweight('normal')

# 图例
handles = []
for grp in groups:
    handles.append(
        Line2D([0], [0], color=group_colors[grp], lw=2.5,
               linestyle='-', marker=markers[grp], markeredgecolor='black', markersize=8)
    )
ax.legend(handles, list(groups.keys()), loc='upper right',
          frameon=True, fancybox=False, markerscale=1,
          handlelength=1, handletextpad=0.5, borderpad=0.3)

# 布局 & 保存
plt.tight_layout()
for ext in ('png', 'pdf'):
    out_path = os.path.join(save_dir, f'clip_score.{ext}')
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {out_path}")

plt.show()
print("drawing finished")
print("finshed end")