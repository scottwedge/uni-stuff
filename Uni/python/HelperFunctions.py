"""Helper functions"""

from DataFormating import *


class HelperFunctions:

	def __init__(self):
		pass


	# create correlation vector
	def correlation_vector(dict_data, list_companies):
		correlation_with_Intel = {}
		for key in dict_data.keys():
			correlation_with_Intel[key] = []
		for key in correlation_with_Intel.keys():
			correlation_with_Intel[key] = numpy.corrcoef(dict_data[list_companies[0]], dict_data[key])[0][1] #ToDo compute dependant variable
		return correlation_with_Intel