"""Class for statistical tests"""

from DataFormating import *
import sklearn as sk
import matplotlib.pyplot as plt 
import numpy
from scipy import stats as stat
from multiprocessing import Pool
import statsmodels.tsa.stattools as statmodel

class StatisticTests:

	def __init__(self, dict_data):
		self.dict_data = dict_data
		self.stationary = {} 
		self.kolmogorov_dict = {}
		self.logkolmogorov_dict = {}
		self.pdf_dict = {}
		self.kde_dict = {}
		self.moments_dict = {}
		self.log_data = {}
		self.data = None

	# check week stationarity and stationary with Agumented Deakey-Fuller Test
	def stationarity(self):
		for key in self.dict_data.keys():
			self.stationary[key] = False
		for key in self.stationary.keys():
			if statmodel.adfuller(self.dict_data[key], 250, 'ctt', 't-stat', False, False)[0] > -3.43:
				self.stationary[key] = True # the row is stationary
			else:
				self.stationary[key] = False
		return self.stationary

	'''Test for distributions, 
	Hypothesis(0)=empirical DF is from tested distribution'''
	# Kolmogorov, distribution = normal, 15% error -> We know, that it is not normal, just to show
	def kolmogorov_normal(self):
		for key in self.dict_data.keys():
			if stat.kstest(self.dict_data[key], 'norm', args=(numpy.average(self.dict_data[key]), numpy.std(self.dict_data[key])), N=1239)[0] < 0.032331:
				self.kolmogorov_dict[key] = True
			else:
				self.kolmogorov_dict[key] = False
		return self.kolmogorov_dict

	# Kolmogorov, distribution = lognormal, 5% error
	def kolmogorov_lognormal(self):
		for key in self.dict_data.keys():
			if stat.kstest(self.dict_data[key], 'lognorm', args=(numpy.average(self.dict_data[key]), numpy.std(self.dict_data[key])), N=1239)[0] < 1.039:
				self.logkolmogorov_dict[key] = True
			else:
				self.logkolmogorov_dict[key] = False
		return self.logkolmogorov_dict

	'''Here we build CDF and PDF for our data, save it to img/,
	compute 1, 2, 3 moments, variation'''
	# build CDF and save it under "CDF_of_copany"
	def build_cdf(self):
		self.pdf_dict = self.dict_data
		num_bins = 100
		plt.figure()
		for key in self.pdf_dict.keys():
			counts, bin_edges = numpy.histogram(self.pdf_dict[key], bins = num_bins, normed=True)
			cdf = numpy.cumsum(counts)
			self.pdf_dict[key] = [cdf, bin_edges]
			plt.title(key)
			plt.plot(bin_edges[1:], cdf)
			plt.savefig("img/CDF/CDF_of_{}.png".format(key))
			plt.clf()
		return self.pdf_dict	

	# build smoothed with gaussian kernel PDF and save it under "KDE_of_company"
	def build_kde(self):
		plt.figure()
		self.kde_dict = self.dict_data
		for key in self.kde_dict.keys():
			kde = stat.gaussian_kde(self.kde_dict[key])
			xgrid = numpy.linspace(min(self.kde_dict[key]), max(self.kde_dict[key]), 100)
			plt.title(key)
			plt.hist(self.kde_dict[key], bins=100, normed=True, color="b")
			plt.plot(xgrid, self.kde(xgrid), color="r", linewidth=3.0)
			plt.savefig("img/KDE/KDE_of_{}.png".format(key))
			plt.clf()
		
		return self.kde_dict 

	# find skew and kurtosis
	def findMoments(self):
		# for every company find mean, var, skew, kurtosis
		for key in self.dict_data.keys():
			self.moments_dict[key] = [numpy.sum(self.dict_data[key])/len(self.dict_data[key]), numpy.std(self.dict_data[key]), stat.skew(self.dict_data[key]), stat.kurtosis(self.dict_data[key], fisher=True)]
		return self.moments_dict

	# bring the data to the normal distribution
	def log_data(self):
		for key in self.dict_data.keys():
			self.log_data[key] = []
			for item in self.dict_data[key]:
				new_item = numpy.log(item)
				self.log_data[key].append(new_item)
		return self.log_data

if __name__ == '__main__':
	# initiate data to work with
	raw_data = DataFormating("../data/LearningSet.csv")
	data = raw_data.get_data()
	dict_data = raw_data.format_into_dict()
	companies = raw_data.getCompanies()
	dependent_variable, list_companies, dict_data = raw_data.extract_dependent()

	statistics = StatisticTests(dict_data)
	kolmogorov = statistics.kolmogorov_normal()
	logfolmogorov = statistics.kolmogorov_lognormal()
	stationary = statistics.stationarity()
	print(kolmogorov_normal)
	print(kolmogorov_lognormal)
	print(stationary)
