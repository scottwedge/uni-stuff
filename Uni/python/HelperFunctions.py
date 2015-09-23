"""Helper functions"""

import numpy
from DataFormating import *


class HelperFunctions:

	def __init__(self, dict_data, list_companies):
		self.dict_data = dict_data
		self.list_companies = list_companies

		self.correlation_with_Intel = {}


	# create correlation vector
	def correlation_vector(self):
		for key in self.dict_data.keys():
			self.correlation_with_Intel[key] = []
		for key in self.correlation_with_Intel.keys():
			self.correlation_with_Intel[key] = numpy.corrcoef(self.dict_data[self.list_companies[0]], self.dict_data[key])[0][1] #ToDo compute dependant variable
		
		return self.correlation_with_Intel






