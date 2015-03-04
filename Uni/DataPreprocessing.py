import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import numpy as num
from scipy import stats as stat
import statsmodels.tsa.stattools as statmodel
from multiprocessing import Pool
import itertools

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
		if stat.kstest(dict_data[key], 'norm', args=(num.average(dict_data[key]), num.std(dict_data[key])), N=1240)[0] < 0.034756:
			result_dict[key] = True
		else:
			result_dict[key] = False
	return result_dict
#anderson-darling test of goodness of fit (normal distribution)	
def anderson_darling_test(dict_data):
	result_dict = {}
	for key in dict_data.keys():
		if stat.anderson(dict_data[key])[0] < 0.787:
			result_dict[key] = True
		else:
			result_dict[key] = False
	return result_dict

#pearson chi square test computed
def pearson_chi_square_test(dict_data):
	grouped = {}
	for key in dict_data.keys():
		grouped[key] = dict_data[key]
	for key in grouped.keys():
		grouped[key].sort()
	n = len(grouped[list(grouped.keys())[0]])
	freq = {}
	for key in grouped.keys():
		freq[key] = [(g[0], len(list(g[1]))) for g in itertools.groupby(grouped[key])]
	observed_frequency = {}
	for key in freq.keys():
		observed_frequency[key] = []
		for item in freq[key]:
			observed_frequency[key].append(item[1])
	chi_square_dict = {}
	chi_square = 0
	for key in observed_frequency:
		chi_square_dict[key] = []
		p = float(1/len(observed_frequency[key]))
		for i in range(0, len(observed_frequency[key])):
			chi_square += ((observed_frequency[key][i]-n*p)*(observed_frequency[key][i]-n*p))/n*p
		chi_square_dict[key].append(chi_square)	
	#we have compued the value of the test, now we will compare it with the critical value of 5% error
	final_result = {}
	for key in chi_square_dict.keys():
		if chi_square_dict[key][0] < 0.07:
			final_result[key] = True
		else:
			final_result[key] = False
	return final_result 
#check chi square
'''Here we build CDF and PDF for our data, save it to img/,
compute 1, 2, 3 moments, variation'''
def check_data_charecteristics(dict_data):
	#build CDF and show it
	'''ToDO: save plots to the img/'''
	check_dict = dict_data
	num_bins = 100
	plt.figure()
	for key in check_dict.keys():
		counts, bin_edges = num.histogram(check_dict[key], bins = num_bins, normed=True)
		cdf = num.cumsum(counts)
		check_dict[key] = [cdf, bin_edges]
		plt.title(key)
		plt.plot(bin_edges[1:], cdf)
		plt.savefig("img/CDF_of_{}.png".format(key))
		plt.clf()
	return check_dict

#find skew and kurtosis
def findMoments(dict_data):
	result_dict = {}
	for key in dict_data.keys():
		result_dict[key] = (stat.skewtest(dict_data[key]), stat.kurtosistest(dict_data[key]))
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
	'''check_dict = dict_data['Intel']
	num_bins = 100
	counts, bin_edges = num.histogram(check_dict, bins = num_bins, normed=True)
	cdf = num.cumsum(counts)
	plt.plot(bin_edges[1:], cdf)
	plt.show()'''
	cdf = check_data_charecteristics(dict_data)


