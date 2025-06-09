'''
Develop a program to implement k-Nearest Neighbour algorithm to 
classify the randomly generated 100 values of x in the range of 
[0,1]. Perform the following based on dataset generated. 
a. Label the first 50 points {x1,……,x50} as follows: if (xi ≤ 0.5), 
then xi ∊ Class1, else xi ∊ Class1 
b. Classify the remaining points, x51,……,x100 using KNN. 
Perform this for k=1,2,3,4,5,20,30
'''

import numpy as np
import matplotlib.pyplot as plt

def knn_classify(train_x, train_y, test_x, k):
    """
    Classifies test_x using k-Nearest Neighbors algorithm.

    Args:
        train_x: Training data features (1D array).
        train_y: Training data labels (1D array).
        test_x: Test data features (1D array).
        k: Number of neighbors to consider.

    Returns:
        Predicted labels for test_x (1D array).
    """

    predictions = []
    for test_point in test_x:
        distances = np.abs(train_x - test_point)  # Calculate absolute distances
        nearest_indices = np.argsort(distances)[:k]  # Find indices of k nearest neighbors
        nearest_labels = train_y[nearest_indices]

        # Determine the most frequent label among the k neighbors
        unique_labels, counts = np.unique(nearest_labels, return_counts=True)
        predicted_label = unique_labels[np.argmax(counts)]
        predictions.append(predicted_label)

    return np.array(predictions)

# Generate 100 random values in the range [0, 1]
np.random.seed(42)  # For reproducibility
x = np.random.rand(100)

# Label the first 50 points
y = np.zeros(100)
# Classification happens here, classified into 2 classes
y[:50] = (x[:50] <= 0.5).astype(int) + 1 #Class 1 if <= 0.5, Class 2 otherwise
y[50:] = -1 # initialize test values to -1, they will be overriden by knn prediction

# Split data into training and test sets
train_x, train_y = x[:50], y[:50]
test_x = x[50:]

# Classify the remaining points using KNN for different values of k
k_values = [1, 2, 3, 4, 5, 20, 30]
predictions = {}

for k in k_values:
    predictions[k] = knn_classify(train_x, train_y, test_x, k)
    y[50:] = predictions[k]
    print(f"Predictions for k={k}: {predictions[k]}")

    # Plot the results for each k
    plt.figure(figsize=(8, 6))
    plt.scatter(train_x, np.zeros_like(train_x), c=train_y, marker='o', label='Training Data')
    plt.scatter(test_x, np.zeros_like(test_x), c=predictions[k], marker='x', label=f'Test Data (k={k})')
    plt.xlabel('x')
    plt.ylabel('Class')
    plt.title(f'KNN Classification (k={k})')
    plt.legend()
    plt.yticks([]) #remove y axis ticks
    plt.show()
