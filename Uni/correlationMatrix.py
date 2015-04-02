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
print(regression1.compare_lr_test(regression2))
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