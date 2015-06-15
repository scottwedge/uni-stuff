import csv
import statistics
import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import numpy as np
import itertools
import scipy as sp
import statsmodels.api as sm
import statsmodels.formula.api as smf

'''data_dict = {}
helper_list = []
average = 0;
learningSet = open('data/LearningSet.csv')
read_it = csv.DictReader(learningSet, delimiter=',')
#getting list of companies for keys in our data_dict 
for row in read_it:
	for company_key in row.keys():
		if company_key not in data_dict:
			data_dict[company_key] = []

		data_dict[company_key].append(float(row[company_key]))
#print(data_dict)
learningSet.close()
#companies correlated with intel
companies = []
correlation_list = []
correlation_dict = {}
correlationMatrix = open('data/CorrelationMatrix.csv')
read_matrix = csv.reader(correlationMatrix, delimiter=',')
for row in read_matrix:
	companies.append(row[0])
	correlation_list.append(row[1])
correlation_list.remove('Intel')
for i in range(0,len(correlation_list)):
	correlation_list[i] = float(correlation_list[i])
companies.remove('')
#get the final dictionary to work with
correlation_dict = dict(zip(correlation_list, companies))
#clean our correlation_list - first-order cut-off
for coefficient in correlation_list:
	if (coefficient < -(0.25)) or (coefficient > 0.25):
		pass
	else:
		correlation_list.remove(coefficient)
#now we only get the names of the company that stayed for further analysis
difference = []
for key in correlation_dict.keys():
	if key not in correlation_list:
		companies.remove(correlation_dict[key])
		difference.append(correlation_dict[key])
	else:
		pass
correlationMatrix.close()


#processing data
temp_list = []
temp_dict_2 = {}
temp_dict = {}
smoothed_data = open('data/HelperData.csv')
helper_file = csv.DictReader(smoothed_data, delimiter=',')
for row in helper_file:
	for key in row.keys():
		temp_list.append(str(key))

for item in temp_list:
	if item not in temp_dict:
		temp_dict[item] = []
	else:
		pass
smoothed_data.seek(0)

second_helper = csv.reader(smoothed_data, delimiter=',')
for line in second_helper:
	#print(line[0])
	pass

smoothed_data.close()

#print(temp_dict) 

'''

"""#checking the AIC value for linera regresion from one explanatory variable
def build_reression(dict_data, list_data):
    #first company in the csv is ALWAYS! our dependent variable 
    result_dict = {}
    dependant = list_companies[0]
    dependent_variable = {list_companies[0]:dict_data[list_companies[0]]}
    del dict_data[dependant]
    #Preprocessing data into usable format for scikit.LinearRegression = sci_dict
    sci_dict = {}
    for key in dict_data.keys():
        sci_dict[key] = []
        for item in dict_data[key]:
            sci_dict[key].append([item])
    #first we will build the regression with 1 dexplanatory variable
    #count AIC, R² and regression's parameters
    #assume the regression y = ß0 + ß1*x
    for key in sci_dict.keys():
        regression = lm.LassoLarsIC()
        FitRegr = regression.fit(sci_dict[key], dependent_variable[list(dependent_variable.keys())[0]])
        RSquare = FitRegr.score(sci_dict[key], dependent_variable[list(dependent_variable.keys())[0]])
        result_dict["y=ß0+ß1*{}".format(key)] = [RSquare, FitRegr.criterion_[1]]
    #evaluation of the best regression based on min AIC value
    helper_list = []
    for k, v in result_dict.items():
        helper_list.append(v[0])
        best_r = max(helper_list)
        best_aic = min(helper_list)
    for key in result_dict.keys():
        if result_dict[key][0] == best_r:
            best = str(key) + " Is the best regression with R²: " + str(result_dict[key][0])
        else:
            pass
    #at this point we have chosen "best" variant among 1-variable-regressions
    
    return best


"""
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

list_test = []
dict_test = {}
#trying to do everything with pandas
data = pd.read_csv('data/LearningSet.csv')
for key in data.keys():
	dict_test[key] = []

#smoothing the data over MA(10)
def formatDataIntoDict(data):
	dict_data = {}
	for key in data.keys():
		dict_data[key] = []
	for key in dict_data.keys():
		for i in range(0,len(data[key])):
			dict_data[key].append(float(data[key][i]))
	return dict_data

dict_data = formatDataIntoDict(data)
#print(data_dict)
y = dict_data['Intel']
dict_test = {'AMD': dict_data['AMD'], 'VW': dict_data['VW'], 'Olympus': dict_data['Olympus']}
X = []
#explanatory data is AMD. VW, Olympus whithout interscept
for i in range(0, len(dict_test['AMD'])):
	X.append([dict_test['AMD'][i]])
for key in dict_test.keys():
	if key != 'AMD':
		for i in range(0, len(dict_test[key])):
			X[i].append(dict_test[key][i])
dict_test2 =  {'VW': dict_data['VW'], 'Olympus': dict_data['Olympus']}
Z = []
for i in range(0, len(dict_test2['VW'])):
	Z.append([dict_test2['VW'][i]])
for key in dict_test2.keys():
	if key != 'VW':
		for i in range(0, len(dict_test2[key])):
			Z[i].append(dict_test2[key][i])
#smaller model
model2 = sm.OLS(y,Z)
regression2 = model2.fit()
#bigger model
model1 = sm.OLS(y,X)
regression1 = model1.fit()
#llr = regression.compare_lr_test(restricted)
print(regression1.compare_lr_test(regression2)[0])
'''# Generate artificial data (2 regressors + constant)
nobs = 100
X = np.random.random((nobs, 2))
X = sm.add_constant(X)
beta = [1, .1, .5]
e = np.random.random(nobs)
y = np.dot(X, beta) + e

# Fit regression model
results = sm.OLS(y, X).fit()

print(len(y))
print(len(X), len(X[0]))
#print (results.summary())'''