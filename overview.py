import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# 生成距离更加适中的数据，中心点多，过渡和离群点少
np.random.seed(42)
central_points_moderate = np.random.normal(loc=(0, 0), scale=1.0, size=(100, 2))
transition_points_moderate = np.random.normal(loc=(3, 3), scale=0.8, size=(10, 2))
outliers_moderate = np.random.normal(loc=(6, 6), scale=0.5, size=(3, 2))
X_moderate = np.vstack((central_points_moderate, transition_points_moderate, outliers_moderate))

# 传统K-means聚类
kmeans_moderate = KMeans(n_clusters=1, random_state=0)
kmeans_moderate.fit(X_moderate)

# 增强算法：排除最远端10%的点重新聚类
distances_moderate = kmeans_moderate.transform(X_moderate).flatten()
threshold_moderate = np.percentile(distances_moderate, 90)
X_moderate_refined = X_moderate[distances_moderate < threshold_moderate]

kmeans_moderate_refined = KMeans(n_clusters=1, random_state=0)
kmeans_moderate_refined.fit(X_moderate_refined)

# 可视化聚类中心变化
plt.figure(figsize=(10, 8))

# 全部数据点（统一颜色）
plt.scatter(X_moderate[:, 0], X_moderate[:, 1], c='lightgray', edgecolor='k', s=60, label='Data Points')

# 传统聚类中心
plt.scatter(kmeans_moderate.cluster_centers_[0, 0], kmeans_moderate.cluster_centers_[0, 1],
            c='red', s=350, marker='X', label='Traditional Center')

# 增强算法聚类中心
plt.scatter(kmeans_moderate_refined.cluster_centers_[0, 0], kmeans_moderate_refined.cluster_centers_[0, 1],
            c='blue', s=350, marker='P', label='Learning-Augmented Center')

# 聚类中心移动箭头
# plt.arrow(kmeans_moderate.cluster_centers_[0, 0], kmeans_moderate.cluster_centers_[0, 1],
#           kmeans_moderate_refined.cluster_centers_[0, 0] - kmeans_moderate.cluster_centers_[0, 0],
#           kmeans_moderate_refined.cluster_centers_[0, 1] - kmeans_moderate.cluster_centers_[0, 1],
#           color='green', linestyle='-', head_width=0.25, head_length=0.4, linewidth=3)

plt.title('Moderate Cluster Center Shift\n(Traditional vs Learning-Augmented Algorithm)', fontsize=15)
plt.xlabel('Feature 1', fontsize=12)
plt.ylabel('Feature 2', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.savefig('output.png')
plt.show()
