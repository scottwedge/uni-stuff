import numpy as np
from sklearn import datasets
from sklearn import linear_model



clf = linear_model.LinearRegression()
x = [[0, 0], [1, 1], [2, 2]]
y =  [0, 1, 2]
a = clf.fit (x, y)
print(x)
print(y)

#tree
'''
clf_1 = DecisionTreeRegressor(max_depth=5)
clf_1.fit(x, y)
X_test = num.arange(0.0, 5.0, 0.01)[:, num.newaxis]
y_1 = clf_1.predict(X_test)
plt.figure()
plt.scatter(x, y, c="k", label="data")
plt.plot(X_test, y_1, c="g", label="max_depth=2", linewidth=2)
plt.xlabel("data")
plt.ylabel("target")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()
print(clf_1)'''