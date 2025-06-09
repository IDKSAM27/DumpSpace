'''
3. Develop a program to implement Principal component analysis for reducing the dimensionality of the Iris dataset from 4 to 2 features
'''

import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

def pca(X, n_components):
    """
    Performs Principal Component Analysis (PCA).

    Args:
        X (numpy.ndarray): Input data matrix (n_samples, n_features).
        n_components (int): Number of principal components to retain.

    Returns:
        numpy.ndarray: Transformed data matrix (n_samples, n_components).
    """

    # 1. Center the data
    X_meaned = X - np.mean(X, axis=0)

    # 2. Compute the covariance matrix
    cov_mat = np.cov(X_meaned, rowvar=False)

    # 3. Compute eigenvalues and eigenvectors
    eigen_values, eigen_vectors = np.linalg.eigh(cov_mat)

    # 4. Sort eigenvalues and eigenvectors in descending order
    sorted_index = np.argsort(eigen_values)[::-1]
    sorted_eigenvectors = eigen_vectors[:, sorted_index]

    # 5. Select the top n_components eigenvectors
    principal_components = sorted_eigenvectors[:, :n_components]

    # 6. Transform the data
    X_transformed = np.dot(X_meaned, principal_components)

    return X_transformed

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Apply PCA to reduce dimensionality to 2 components
X_pca = pca(X, 2)

# Visualize the results
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Iris Dataset (2 Components)')
plt.colorbar(ticks=np.unique(y), label='Species')
plt.show()