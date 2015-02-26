import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import numpy as num
from scipy import stats as stat

def getData(file_name):
	data = pd.read_csv(str(file_name))
	return data
def formatDataIntoDict(data):
	dict_data = {}
	for key in data.keys():
		dict_data[key] = []
	for key in dict_data.keys():
		for i in range(0,len(data[key])):
			dict_data[key].append(float(data[key][i]))
	return dict_data
def getCompanies(data):
	list_companies = []
	for key in data.keys():
		list_companies.append(key)
	return list_companies


#Kolmogorov test 
def kolmogorovTest(dict_data, distribution):
	result_dict = {}
	for key in dict_data:
		result_dict[key] = [stat.kstest(dict_data[key], distribution)]
	return result_dict

#different helper functions and tests:
def checkDictionary(dictionary,listCheck):
	result = False
	check_list = [False for i in range(0,len(listCheck))]
	for i in range(0, len(listCheck)):
		for key in dictionary.keys():
			if key in listCheck:
				check_list[i] = True
			else:
				check_list[i] = False
	for item in check_list:
		if False in check_list:
			result = False
		else:
			result = True
	return result


'''Resulting outputs'''
f = 'data/LearningSet.csv'
data = getData(f)
dict_data = formatDataIntoDict(data)
list_companies = getCompanies(data)
kolmogorov = kolmogorovTest(dict_data, 'norm')
print(kolmogorov)

#test kolmogorov 
test_data = dict_data['Intel']
for item in test_data:
	item = (item - num.mean(test_data))/num.std(test_data)
print(stat.chisquare(dict_data['Intel']))
print(stat.kstest(dict_data['Intel'], 'norm'))