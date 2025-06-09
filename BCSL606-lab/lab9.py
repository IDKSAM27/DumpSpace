'''
9. Develop a program to impelement the Naive Bayesian Classifier considering Olivetti Face Data set for training.
Compute the accuracy of the classifier, considering a few test data sets.
'''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_olivetti_faces
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score,classification_report

faces=fetch_olivetti_faces()
X=faces.data
y=faces.target

X_train, X_test,y_train,y_test=train_test_split(X, y, test_size=0.2,random_state=42,stratify=y)

gnb= GaussianNB()
gnb.fit(X_train,y_train)

y_pred= gnb.predict(X_test)

acc= accuracy_score(y_test,y_pred)
print("Accuracy of Gaussian Naive Bayes on Olivetti Faces:", acc)
print("\nClassificationReport:\n",classification_report(y_test,y_pred))

def show_images(images, labels,preds,n=10):
    plt.figure(figsize=(12,5))
    for i in range(n):
        plt.subplot(2,n//2,i+1)
        plt.imshow(images[i].reshape(64,64),cmap='gray')
        plt.title(f"True:{labels[i]}\nPred:{preds[i]}")
        plt.axis('off')
    plt.tight_layout()
    plt.show()

show_images(X_test,y_test,y_pred,n=10)