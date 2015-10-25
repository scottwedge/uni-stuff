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

def build_model(file_name):
	dict_data, list_companies, dependent_variable, rest_companies, dict_final = collect_data(file_name)
	stationary, moments, log_normal = collect_statistics(dict_data)
	if False in stationary.values() and False in log_normal.values():
		print("choose different model to build, deal with non stationary first")
	else:
		# create model and return the information
		model_raw = BuildModel(dict_data, list_companies, dependent_variable, rest_companies, dict_final)
		cor_vec = model_raw.correlation_vector(dict_data)
		cut_off = model_raw.correlational_cutoff(cor_vec)
		build_model = model_raw.build_the_model(cut_off)

	print(build_model)
	return build_model

def build_predictions():
	# get testing data.frame and dependent
	test_raw = DataFormatting("../data/TestingSet.csv")
	test_dict = test_raw.keep_dict()
	comp_test = test_raw.getAllCompanies()
	dependent_variable_tmp, rest, dict_final_tmp = test_raw.extract_dependent()

	test_model = BuildModel(test_dict, comp_test, dependent_variable_tmp, rest, dict_final_tmp)
	y = test_dict[list(dependent_variable_tmp.keys())[0]]

	# manually given resulting list of the companies
	model_list = ['STMElectro', 'Olympus', 'St Jude', 'Lenovo', 'MicronTech', 'Google']

	# get params on test_set
	test_data = test_model.get_data_for_comparison(model_list, test_dict) 
	params = sm.GLS(y, test_data).fit().params

	predict = sm.GLS(y, test_data).predict(params)
	diff = y - predict
	av = numpy.mean(diff)
	max_dif = max(diff)
	min_diff = min(diff)
	if max_dif > (min_diff * (-1)):
		dev = max_dif
	else:
		dev = min_diff

	print("difference vector is: " + str(diff))
	print("the average difference is: " + str(av))
	print("max deviation is: " + str(dev))

	return predict, diff, av, dev

if __name__ == '__main__':

	# initialize the data
	#file_name = "../data/LearningSet.csv"
	#build_model(file_name)

	predict, diff, av, dev = build_predictions()

	# cProfile.run('collect_data(file_name)')
	# cProfile.run('collect_statistics(dict_data)')
	# cProfile.run('build_model(file_name)')

