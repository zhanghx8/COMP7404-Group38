import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

plt.style.use('seaborn-v0_8-muted')  # 更现代的 seaborn 样式

def parse_alpha(param_str):
    param_str = str(param_str)
    match = re.search(r"Error\s+([\d.]+)", param_str)
    if match:
        return float(match.group(1))
    return None

# 加载 CSV 文件
dataset_name = 'phy'
df = pd.read_csv(f"{dataset_name}KmeansResult.csv")

# 提取横轴：错误率 α
alphas = df["Params"].apply(parse_alpha)

# 提取算法名称
method_names = ["Predictor", "Sampling", "Ergun, Jon, et al.", "Ours"]
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']  # 自动配色

plt.figure(figsize=(10, 6))
print(df.columns)
# 绘制每种算法的均值曲线 + 误差带
for idx, method in enumerate(method_names):
    if method not in df.columns or method + "EB" not in df.columns:
        print(method)
        continue

    y = df[method]
    yerr = df[method + "EB"]

    # 排除 alpha 为 None 的数据点
    valid = alphas.notnull()
    alpha_vals = alphas[valid]
    y = y[valid]
    yerr = yerr[valid]

    # 排序（以防数据顺序混乱）
    sorted_idx = np.argsort(alpha_vals)
    alpha_vals = np.array(alpha_vals)[sorted_idx]
    y = np.array(y)[sorted_idx]
    yerr = np.array(yerr)[sorted_idx]

    # 绘制主曲线（带 marker）
    plt.plot(alpha_vals, y, label=method, color=colors[idx % len(colors)],
             marker='o', linewidth=2)

    # 绘制误差带
    plt.fill_between(alpha_vals, y - yerr, y + yerr, alpha=0.2,
                     color=colors[idx % len(colors)])

# 可选：绘制 OPT 水平线
if "OPT" in df.columns:
    opt_val = df["OPT"].mean()
    plt.axhline(y=opt_val, linestyle='--', color='gray', label='OPT')

# 图形美化
plt.xlabel("Error rate α", fontsize=12)
plt.ylabel("K-means cost", fontsize=12)
plt.title(f"K-means Clustering Results on {dataset_name}", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(f'{dataset_name}.png')

# 展示图像
plt.show()
