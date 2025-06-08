import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing

def analyze_california_housing():
    try:
        california = fetch_california_housing(as_frame=True)
        df = california.frame

        correlation_matrix = df.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix of California Housing Features')
        plt.show()

        sns.pairplot(df)
        plt.show()

    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    analyze_california_housing()