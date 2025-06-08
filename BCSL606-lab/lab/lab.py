import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

def pca(X, n_components):
    X_meaned = X - np.mean(X, axis = 0)

    cov_mat = np.cov(X_meaned, rowvar=False)

    eigen_values, eigen_vectors = np.linalg.eigh(cov_mat)

    sorted_index = np.argsort(eigen_values)[::-1]
    sorted_eigenvectors = eigen_vectors[:, sorted_index]

    principal_components = sorted_eigenvectors[:,:n_components]

    X_transformed = np.dot(X_meaned, principal_components)

    return X_transformed

iris = load_iris()
X = iris.data
y = iris.target

X_pca = pca(X, 2)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Iris Dataset')
plt.colorbar(ticks=np.unique(y), label='Species')
plt.show()