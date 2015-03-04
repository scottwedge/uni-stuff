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

def formatDataIntoReturns(data):
	financial_returns = {}
	for key in data.keys():
		financial_returns[key] =  []
		for i in range(1, len(data[key])):
			financial_returns[key].append((data[key][i]-data[key][i-1])/data[key][i-1])
	return financial_returns

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

#autocorrelation check (for chosen regression)
def autodorrelation(dict_data):
	pass

#a bunch of distribution-test for the data
#kolmogorov: 1-sample test H0 = Data has hoemal distribution with estimated mean and variation
def kolmogorov_test(dict_data):
	result_dict = {}
	for key in dict_data.keys():
		if stat.kstest(dict_data[key], 'norm', args=(num.average(dict_data[key]), num.std(dict_data[key])), N=1238)[0] >= 0.9750:
			result_dict[key] = True
		else:
			result_dict[key] = False
	return result_dict

#normality test
def normality_test(dict_data):
	result_dict = {}
	kolmogorov_check = kolmogorov_test(dict_data)
	for key in kolmogorov_check.keys():
		if kolmogorov_check[key] == True:
			pass
		else:
			for key in dict_data.keys():
				if stat.normaltest(dict_data[key])[1] < 5.991:
					result_dict[key] = True
				else:
					result_dict[key] = False
	return result_dict

def anderson_darling_test(dict_data):
	result_dict = {}
	for key in dict_data.keys():
		if stat.anderson(dict_data[key])[0] >= 0.787:
			result_dict[key] = False
		else:
			result_dict[key] = True
	return result_dict

#different helper functions and tests:
def checkDictionary(dictionary,listCheck):
	result_value = False
	check_list = [False for i in range(0,len(listCheck))]
	for i in range(0, len(listCheck)):
		for key in dictionary.keys():
			if key in listCheck:
				check_list[i] = True
			else:
				check_list[i] = False
	for item in check_list:
		if False in check_list:
			result_value = False
		else:
			result_value = True
	return result

#Akaike criterion for choosing maximum number of the companies for regression


if __name__ == "__main__":
	'''Resulting outputs'''
	f = 'data/LearningSet.csv'
	data = getData(f)
	list_companies = getCompanies(data)
	dict_data = formatDataIntoDict(data)
	dict_returns = formatDataIntoReturns(data)
	#stationary = stationarity(dict_returns)
	#print(stationary)
	#normality = normality_test(dict_data)
	#ad = anderson_darling_test(dict_data)
	
	#print(stationary)
	plt.plot(num.log(dict_data['Intel']))
	plt.show()
