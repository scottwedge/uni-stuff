import numpy as np
from sklearn import datasets
from sklearn import linear_model


iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target
np.unique(iris_y)
diabetes = datasets.load_diabetes()
diabetes_X_train = diabetes.data[:-20]
diabetes_X_test  = diabetes.data[-20:]
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test  = diabetes.target[-20:]

regr = linear_model.LinearRegression()
b = regr.fit(diabetes_X_train, diabetes_y_train)
c = b.predict(diabetes_X_test)
d = b.score(diabetes_X_train, diabetes_y_train)
print(d)