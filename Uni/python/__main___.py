"""__main___"""

from DataFormating import *

if __name__ == '__main__':

	# initialize the data
	raw_data = DataFormating("../data/LearningSet.csv")
	dict_data = raw_data.keep_dict()
	list_companies = raw_data.getAllCompanies()
	dependent_variable, rest_companies, dict_final = raw_data.extract_dependent()
	print(dependent_variable)

	# check the data characteristics

	# create model and return the information
