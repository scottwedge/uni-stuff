import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import numpy as num
from scipy import stats as stat
import statsmodels.tsa.stattools as statmodel
from multiprocessing import Pool

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

def passes_dftest(data):
	print("Processing {}".format(data[0]))
	if statmodel.adfuller(data[1], 250, 'ctt', 't-stat', False, False)[0] < 1:
		return (data[0], True)
	else:
		return (data[0], False)

#check week stationarity and stationary with Deakey-Fuller Test
def stationarity(dict_data):
	stationary = {}
	#initiate output dictionary
	for key in dict_data.keys():
		stationary[key] = False
	print(stationary.keys())
	with Pool() as p:
		print("Starting parallel map")
		p.map(passes_dftest, dict_data.items())
	return stationary

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

if __name__ == "__main__":
	'''Resulting outputs'''
	f = 'data/LearningSet.csv'
	data = getData(f)
	dict_data = formatDataIntoDict(data)
	list_companies = getCompanies(data)
	first = stat.moment(dict_data['Intel'], 1,0)
	second = stat.moment(dict_data['Intel'], 2, 0)
	#print(len(dict_data))
	stationary = stationarity(dict_data)
	print(stationary)
	#kolmogorov = kolmogorovTest(dict_data['Intel'], 'norm')
	#print("kolmogorov: "+str(kolmogorov), "first momentt: "+str(first), "second moment: "+str(second))

	#test kolmogorov 
