'''
10. Develop a program to implement k-means clustering using Wisconsin Breast Cancer 
data set and visualize the clustering result.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

data=load_breast_cancer()
X=pd.DataFrame(data.data,columns=data.feature_names)
y=pd.Series(data.target)

kmeans= KMeans(n_clusters=2, random_state=42,n_init=10)
clusters=kmeans.fit_predict(X)

if accuracy_score(y, clusters)<0.5:
    clusters= 1-clusters

print("Clustering Accuracy:", accuracy_score(y,clusters))
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=clusters, palette='Set1')
plt.title("K-Means Clustering Result (k=2)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title='Cluster')

plt.subplot(1, 2, 2)
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y, palette='Set2')
plt.title("Actual Labels (Malignant/Benign)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title='Actual')
plt.tight_layout()
plt.show()