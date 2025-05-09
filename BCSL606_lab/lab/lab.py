import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import fetch_california_housing

# Fetching or calling the California Housing Dataset
california = fetch_california_housing(as_frame=True)
df = california.frame

numerical_features = df.select_dtypes(include=['number']).columns

# Creating and plotting Histogram for all Numerical features
plt.figure(figsize=(15, 10))
for i, feature in enumerate(numerical_features):
    plt.subplot(3, 3, i + 1)
    sns.histplot(df[feature], kde=True)
    plt.title(f'Histogram of {feature}')
plt.tight_layout()
plt.show()

# Creating Box plot and outliers analysis
plt.figure(figsize=(15, 10))
for i, feature in enumerate(numerical_features):
    plt.subplot(3, 3, i + 1)
    sns.boxplot(y=df[feature])
    plt.title(f'Boxplot of {feature}')
plt.tight_layout()
plt.show()

# Finding outliers Inter Quartile Range
def detect_outliers_iqr(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    return outliers

print("Outlier Analysis:")
for feature in numerical_features:
    outliers = detect_outliers_iqr(df[feature])
    print(f"\nFeature: {feature}")
    print(f"Number of outliers: {len(outliers)}")
    if len(outliers) > 0 and len(outliers) < 20 :
      print(f"Outlier values: {outliers.values}")
    elif len(outliers) >= 20:
        print("Too many outliers to display.")
    else:
        print("No outliers detected.")

