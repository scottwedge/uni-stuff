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

#Best combination of 5 from 68  Too slow, but works
'''def best_regression(data):
    #the first column in the data set is ALWAYS the dependant variable
    companies_list = getCompanies(data)
    data_dict = formatDataIntoDict(data)
    dependant_variable = {companies_list[0]:dict_data[companies_list[0]]} #separate dependant and explanatory variables 
    for key in dependant_variable.keys():
        if key in list_companies:
            companies_list.remove(key)
        else:
            pass
        if key in data_dict.keys():
            del data_dict[key]
        else:
            pass
    #create all possible combinations 5 of 68
    comb_companies = []
    for item in itertools.combinations(list_companies, 5):
        comb_companies.append(item)

    #formating combinations into dictionary 
    test_combination_indexed = {}
    for item in comb_companies:
        test_combination_indexed = {i: comb_companies[i] for i in range(0, len(comb_companies))}

    r_square = {i: [] for i in range(0, len(test_combination_indexed.keys()))}  #create dict with R² as the key and combination as value, initiating the dictionary 
    final = {} #final dict is the resulting dictionary with r² as the key and corresponding combination as value
    combination_array_dict = {} #for every combination the dictionary will be overwritten to save memory
    combination_array_list = [] #formating the combination_array_dict to list to use LinearRegression
    #get R² for all combinations
    for key_index in test_combination_indexed.keys():
        for i in range(0, len(dict_data['Intel'])):
            combination_array_dict[i] = [value[i] for key, value in dict_data.items() if key in test_combination_indexed[key_index]] 
            combination_array_list = [value for key, value in sorted(combination_array_dict.items())]
        reg = lm.LinearRegression()
        test = reg.fit(combination_array_list, y)
        r = test.score(combination_array_list, y)
        r_square[key_index].append(r) 

    #final_dict getting values from the previous step
    for key1 in test_combination_indexed.keys():
        for key2 in r_square.keys():
            if key1 == key2:
                final[float(r_square[key2][0])] = list(test_combination_indexed[key1]) 
            else:
                pass

    #choose "best match" by taking combination with the highest R²
    best_r = max(dinal.keys())
    best_match = "The best combination of 5 companies from 68 given is: " + str(final(best_r)) + " with R²: " + str(best_r)

    return best_match'''