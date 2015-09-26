"""__main___"""

from DataFormating import *
from StatisticTests import *
from BuildModel import *

if __name__ == '__main__':

	# initialize the data
	raw_data = DataFormating("../data/LearningSet.csv")
	dict_data = raw_data.keep_dict()
	list_companies = raw_data.getAllCompanies()
	dependent_variable, rest_companies, dict_final = raw_data.extract_dependent()

	# check the data characteristics
	statistics = StatisticTests(dict_data)
	stationary = statistics.stationarity()
	normal = statistics.kolmogorov_normal()
	log_normal = statistics.kolmogorov_lognormal()
	moments = statistics.findMoments()
	kde = statistics.build_kde()
	cdf = statistics.build_cdf()

	if False in stationary.values() and False in log_normal.values():
		print("choose different model to build, deal with non stationary first")
	else:
		# create model and return the information
		model_raw = BuildModel(dict_data, list_companies, dependent_variable, rest_companies, dict_final)
		cor_vec = model_raw.correlation_vector()
		cut_off = model_raw.correlational_cutoff(cor_vec)
		build_model = model_raw.build_the_model(cut_off)

	print(build_model)



