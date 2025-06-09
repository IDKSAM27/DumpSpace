'''
8. Develop a program to demonstrate the working of the decision tree algorithm. 
Use Breast Cancer Data set for building the decision tree and apply this knowledge to classify a new sample
'''

from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
import matplotlib.pyplot as plt
import pandas as pd

data=load_breast_cancer()
X=pd.DataFrame(data.data,columns=data.feature_names)
y=pd.Series(data.target,name='target')

X_train, X_test,y_train,y_test=train_test_split(X, y, test_size=0.2,random_state=42)

clf= DecisionTreeClassifier(random_state=42)
clf.fit(X_train,y_train)

y_pred= clf.predict(X_test)
print("Accuracy:",accuracy_score(y_test,y_pred))
print("\nClassification Report:\n",classification_report(y_test,y_pred,target_names=data.target_names))

plt.figure(figsize=(16, 8))
plot_tree(clf, filled=True,feature_names=data.feature_names,class_names=data.target_names,max_depth=3)
plt.title("Decision Tree(Truncated at Depth3)")
plt.show()

new_sample=X_test.iloc[0].values.reshape(1,-1)
prediction=clf.predict(new_sample)
print("\nNew Sample Prediction:")
print("Features:\n", X_test.iloc[0])

print("Predicted Class:",data.target_names[prediction[0]])