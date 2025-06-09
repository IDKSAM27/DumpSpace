'''
For a given set of training data examples stores in a .csv file, implement and demonstrate the Find-S algo to output a description of the set of all hypotheses consistent with the training examples
'''

import pandas as pd

def find_s_algorithm():
    # Define the dataset directly instead of reading from a CSV file
    data = pd.DataFrame({
        'Sky': ['Sunny', 'Sunny', 'Cloudy', 'Rainy', 'Sunny'],
        'Temperature': ['Warm', 'Hot', 'Warm', 'Cold', 'Warm'],
        'Humidity': ['Normal', 'High', 'High', 'Normal', 'Normal'],
        'Wind': ['Strong', 'Weak', 'Strong', 'Strong', 'Weak'],
        'PlayTennis': ['Yes', 'No', 'Yes', 'No', 'Yes']  # Target column
    })

    print("Training data:")
    print(data)

    attributes = data.columns[:-1]  # All columns except the last one
    class_label = data.columns[-1]  # The last column is the target variable

    hypothesis = ['?' for _ in attributes]  # Initialize with the most general hypothesis

    for index, row in data.iterrows():
        if row[class_label] == 'Yes':  # Process only positive examples
            for i, value in enumerate(row[attributes]):
                if hypothesis[i] == '?' or hypothesis[i] == value:
                    hypothesis[i] = value  # Retain attribute value if it matches
                else:
                    hypothesis[i] = '?'  # Generalize otherwise

    return hypothesis


# Run the algorithm without worrying about file paths
hypothesis = find_s_algorithm()
print("\nThe final hypothesis is:", hypothesis)