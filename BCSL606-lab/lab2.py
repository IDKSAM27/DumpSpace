# Develop a program to compute the correlation matrix to understand the relationships between pairs of features. Visualize
# the correlation matrix using a heatmap to know which variables have strong +ve/-ve correlations.
# Create a pair plot to visualize pairwise relationships between features. Use California Housing dataset.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing

def analyze_california_housing():
    """
    Computes and visualizes the correlation matrix and pair plot for the California Housing dataset.
    """
    try:
        # Load the California Housing dataset
        california = fetch_california_housing(as_frame=True)
        df = california.frame

        # Compute the correlation matrix
        correlation_matrix = df.corr()

        # Visualize the correlation matrix using a heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix of California Housing Features')
        plt.show()

        # Create a pair plot to visualize pairwise relationships between features
        sns.pairplot(df)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_california_housing()
