import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score

print("\n---LinearRegressiononCaliforniaHousing---")
housing=fetch_california_housing()
df=pd.DataFrame(housing.data,columns=housing.feature_names)
df['MedHouseVal'] =housing.target

X=df[['MedInc']]
y=df['MedHouseVal']

X_train, X_test,y_train,y_test=train_test_split(X, y, test_size=0.2,random_state=42)

lr_model=LinearRegression()
lr_model.fit(X_train,y_train)
y_pred= lr_model.predict(X_test)

print("MSE:",mean_squared_error(y_test,y_pred))
print("R2Score:",r2_score(y_test,y_pred))

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_test['MedInc'],y=y_test, label="Actual")
sns.lineplot(x=X_test['MedInc'],y=y_pred, color='red',label="Predicted")
plt.title("Linear Regression:MedIncvsMedHouseVal")
plt.xlabel("MedianIncome")
plt.ylabel("MedianHouseValue")
plt.legend()
plt.tight_layout()
plt.show()

print("\n---Polynomial RegressiononAuto MPG---")

url= "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
columns=["mpg", "cylinders","displacement","horsepower", "weight",
"acceleration", "model_year","origin","car_name"]

auto_df=pd.read_csv(url, delim_whitespace=True,names=columns,na_values='?')
auto_df.dropna(inplace=True)

X_auto= auto_df[['horsepower']].astype(float)
y_auto= auto_df['mpg']

X_train, X_test,y_train,y_test=train_test_split(X_auto,y_auto,test_size=0.2,
random_state=42)

poly=PolynomialFeatures(degree=2)
X_poly_train= poly.fit_transform(X_train)
X_poly_test=poly.transform(X_test)

poly_model=LinearRegression()
poly_model.fit(X_poly_train,y_train)
y_poly_pred=poly_model.predict(X_poly_test)

print("MSE:",mean_squared_error(y_test,y_poly_pred))
print("R2Score:",r2_score(y_test,y_poly_pred))

X_range=np.linspace(X_auto.min(),X_auto.max(),100).reshape(-1,1)
X_range_poly= poly.transform(X_range)
y_range_pred= poly_model.predict(X_range_poly)

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_test['horsepower'],y=y_test,label="Actual")
sns.lineplot(x=X_range.flatten(),y=y_range_pred,color='green',label="PolynomialFit")
plt.title("PolynomialRegression:HorsepowervsMPG")
plt.xlabel("Horsepower")
plt.ylabel("MilesperGallon(MPG)")
plt.legend()
plt.tight_layout()
plt.show()