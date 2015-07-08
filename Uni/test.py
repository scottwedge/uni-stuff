import numpy as np
from sklearn import datasets
from sklearn import linear_model
import numpy as np
import itertools
import scipy as sp
import statsmodels.api as sm


clf = linear_model.LinearRegression()
x = [[0, 0], [1, 1], [2, 2]]
y =  [0, 1, 2]
a = clf.fit (x, y)
r_sq = a.score(x, y)
print(len(y), "x 1")
print(len(x), "x", len(x[0]))
print(r_sq)
print("_________________________")
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

# Generate artificial data (2 regressors + constant)
nobs = 100
X = [[0, 0], [1, 1], [2, 2]]
Y =  [0, 1, 2]

# Fit regression model
mod = sm.OLS(Y, X)
regr = mod.fit()
r_sqr = regr.rsquared

print(len(Y), " y: ", Y)
print(len(X), "x", len(X[0]), " X: ", X)
print(r_sqr)
#print (results.summary())