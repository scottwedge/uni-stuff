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

	# get real data 
	build_raw = DataFormatting("../data/LearningSet.csv")
	build_dict = build_raw.keep_dict()
	comp_model = build_raw.getAllCompanies()
	dependent_variable_mod, rest_mod, dict_final_mod = build_raw.extract_dependent()
	real_model = BuildModel(build_dict, comp_model, dependent_variable_mod, rest_mod, dict_final_mod)
	y_mod = build_dict[list(dependent_variable_mod.keys())[0]]

	test_model = BuildModel(test_dict, comp_test, dependent_variable_tmp, rest, dict_final_tmp)
	y = test_dict[list(dependent_variable_tmp.keys())[0]]

	# manually given resulting list of the companies
	model_list = ['STMElectro', 'Olympus', 'St Jude', 'Lenovo', 'MicronTech', 'Google']

	# get params on test_set
	test_data = test_model.get_data_for_comparison(model_list, test_dict) 
	build_data = real_model.get_data_for_comparison(model_list, build_dict)
	model = sm.GLS(y_mod, build_data)
	params = model.fit().params

	predict = model.predict(params, test_data)
	diff = y - predict
	mean_pred = numpy.mean(predict)
	std_pred = numpy.std(predict)
	max_dif = max(diff)
	min_diff = min(diff)
	if max_dif > (min_diff * (-1)):
		dev = max_dif
	else:
		dev = min_diff

	# plot predictions and real prices
	plt.figure()
	plt.title("Predictions vs Real Prices")
	plt.plot(y, color="r", linewidth=2.0)
	plt.plot(predict, color="b", linewidth=1.0)
	plt.savefig("PythonPredictions.png")
	plt.clf()

	print("the mean of the y is: " + str(numpy.mean(y)))
	print("the std of the y is: " + str(numpy.std(y)))

	print("the mean of the prediction is: " + str(mean_pred))
	print("the standart deviation is: " + str(std_pred))


	return predict, diff, mean_pred, std_pred

if __name__ == '__main__':

	# initialize the data
	#file_name = "../data/LearningSet.csv"
	#build_model(file_name)

	predict, diff, av, dev = build_predictions()

	# cProfile.run('collect_data(file_name)')
	# cProfile.run('collect_statistics(dict_data)')
	# cProfile.run('build_model(file_name)')

