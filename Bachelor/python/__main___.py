"""__main___"""

from DataFormatting import *
from StatisticTests import *
from BuildModel import *
import cProfile
import re

def collect_data(file_name):
	raw_data = DataFormatting(file_name)
	dict_data = raw_data.keep_dict()
	list_companies = raw_data.getAllCompanies()
	dependent_variable, rest_companies, dict_final = raw_data.extract_dependent()

	return dict_data, list_companies, dependent_variable, rest_companies, dict_final

def collect_statistics(dict_data):
	statistics = StatisticTests(dict_data)
	stationary = statistics.stationarity()
	normal = statistics.kolmogorov_normal()
	log_normal = statistics.kolmogorov_lognormal()
	moments = statistics.findMoments()
	kde = statistics.build_kde()
	cdf = statistics.build_cdf()

	return stationary, moments, log_normal


if __name__ == '__main__':

	# initialize the data
	file_name = "../data/LearningSet.csv"
	dict_data, list_companies, dependent_variable, rest_companies, dict_final = collect_data(file_name)

	# create validation set
	# file_name2 = "../data/TestingSet.csv"
	# dict_data2, list_companies2, evaluation_set, rest_companies2, dict_final2 = collect_data(file_name2)

	# check the data characteristics
	stationary, moments, log_normal = collect_statistics(dict_data)
	if False in stationary.values() and False in log_normal.values():
		print("choose different model to build, deal with non stationary first")
	else:
		# create model and return the information
		model_raw = BuildModel(dict_data, list_companies, dependent_variable, rest_companies, dict_final)
		cor_vec = model_raw.correlation_vector()
		cut_off = model_raw.correlational_cutoff(cor_vec)
		build_model = model_raw.build_the_model(cut_off)

	print(build_model)

	# difference = []
	# for key in evaluation_set.keys():
	# 	for i in range(0, len(evaluation_set[key])):
	# 		difference.append(evaluation_set[i]-predictions[i])

	# print(difference)

	#cProfile.run('collect_data(file_name)')
	#cProfile.run('collect_statistics(dict_data)')