import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import numpy as num
from scipy import stats as stat
import statsmodels.tsa.stattools as statmodel
from multiprocessing import Pool
import itertools
import math
import sklearn as sk
from sklearn import linear_model  as lm
from sklearn.tree import DecisionTreeRegressor
import operator


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

'''Here we build CDF and PDF for our data, save it to img/,
compute 1, 2, 3 moments, variation'''
def built_cdf(dict_data):
	#build CDF and save it under "CDF_of_copany"
	pdf_dict = dict_data
	num_bins = 100
	plt.figure()
	for key in pdf_dict.keys():
		counts, bin_edges = num.histogram(pdf_dict[key], bins = num_bins, normed=True)
		cdf = num.cumsum(counts)
		pdf_dict[key] = [cdf, bin_edges]
		plt.title(key)
		plt.plot(bin_edges[1:], cdf)
		plt.savefig("img/CDF/CDF_of_{}.png".format(key))
		plt.clf()

#build smoothed with gaussian kernel PDF and save it under "KDE_of_company"
def build_kde(dict_data):
	plt.figure()
	kde_dict = dict_data
	for key in kde_dict.keys():
		kde = stat.gaussian_kde(kde_dict[key])
		xgrid = num.linspace(min(kde_dict[key]), max(kde_dict[key]), 100)
		plt.title(key)
		plt.hist(kde_dict[key], bins=100, normed=True, color="b")
		plt.plot(xgrid, kde(xgrid), color="r", linewidth=3.0)
		plt.savefig("img/KDE/KDE_of_{}.png".format(key))
		plt.clf()
	
	return pdf_dict, kde_dict 

#find skew and kurtosis
def findMoments(dict_data):
	#for every company find mean, var, skew, kurtosis
	result_dict = {}
	for key in dict_data.keys():
		result_dict[key] = [num.sum(dict_data[key])/len(dict_data[key]), num.std(dict_data[key]), stat.skew(dict_data[key]), stat.kurtosis(dict_data[key], fisher=True)]
	return result_dict

'''Test for distributions, 
Hypothesis(0)=empirical DF is from tested distribution'''
#Kolmogorov, distribution = normal, 15% error
def kolmogorov_normal(dict_data):
	result_dict = {}
	for key in dict_data.keys():
		if stat.kstest(dict_data[key], 'norm', args=(num.average(dict_data[key]), num.std(dict_data[key])), N=1239)[0] < 0.032331:
			result_dict[key] = True
		else:
			result_dict[key] = False
	return result_dict

#Kolmogorov, distribution = lognormal, 5% error
def kolmogorov_lognormal(dict_data):
	result_dict = {}
	for key in dict_data.keys():
		if stat.kstest(dict_data[key], 'lognorm', args=(num.average(dict_data[key]), num.std(dict_data[key])), N=1239)[0] < 1.039:
			result_dict[key] = True
		else:
			result_dict[key] = False
	return result_dict

#AD, distribution = Pareto, 5% error
def ad_gumbel(dict_data):
	result_dict = {}
	for key in dict_data.keys():
		if stat.anderson(dict_data[key], dist='gumbel') < 3.791:
			result_dict[key] = True
		else:
			result_dict[key] = False
	return result_dict

#AD test, for logistic and gumbel, 85% confidence
def anderson_darling_multiple(dict_data):
	result_dict = {}
	distribution = {}
	#check for logistic first
	for key in dict_data.keys():
		distribution[key] = []
		if stat.anderson(dict_data[key], dist="logistic")[0] < 0.787:
			result_dict[key] = True
		else:
			result_dict[key] = False
	for key in result_dict.keys():
		if result_dict[key] == True:
			distribution[key].append("is logistic")
		else:
			for key in dict_data.keys():
				if stat.anderson(dict_data[key], dist="gumbel")[0] < 0.787:
					result_dict[key] = True
					distribution[key].append("is gumble")
				else:
					result_dict[key] = False
	return distribution, result_dict
'''Heteroscedasticity Tests'''
#null hypothesis is that all observations have the same error variance
def constant_variance(dict_data):
	pass

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

#bring the data to the normal distribution
def log_data(dict_data):
	log_data = {}
	for key in dict_data.keys():
		log_data[key] = []
		for item in dict_data[key]:
			new_item = math.log(item)
			log_data[key].append(new_item)
	return log_data

#Akaike criterion for choosing maximum number of the companies for regression
'''Algorithm 1'''
#checking the AIC value for linera regresion from one explanatory variable
def build_reression(dict_data, list_data):
	#first company in the csv is our dependent variable ALWAYS!
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
	best_regression = {}
	best_aic = 0
	for key in result_dict.keys():
		pass

	return result_dict
		

		
	#!!!Here, we agree on some model error, because the weights for WLS are functions from the data
	# We agree on error because as the output we need companies (names), that are included into regression
	# also we agreed on "bad model", so the error up to 25% is accaptable



if __name__ == "__main__":
	'''Resulting outputs'''
	f = 'data/LearningSet.csv'
	data = getData(f)
	list_companies = getCompanies(data)
	dict_data = formatDataIntoDict(data)
	regression_one = build_reression(dict_data, list_companies)
	#print(regression_one)
	print(regression_one)
	best = ""				
	helper_list = []
	for k, v in regression_one.items():
		helper_list.append(v[1])
		best_aic = min(helper_list)
	for key in regression_one.keys():
		if regression_one[key][1] == best_aic:
			best = str(key) + "Is the bset regression with " + str(regression_one[key][0])
	print(best)

	
