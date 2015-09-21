"""Class for data formating"""

import pandas as pd

class DataFormating:

	def __init__(self, file_name):
		self.file_name = file_name
		self.data = None
		self.dict_data = {}
		self.list_companies = []
		self.dependent_variable = {}

	def get_data(self):
		self.data = pd.read_csv(str(self.file_name))
		return self.data

	def format_into_dict(self):
		for key in self.data.keys():
			self.dict_data[key] = []
		for key in self.dict_data.keys():
			for i in range(0,len(self.data[key])):
				self.dict_data[key].append(float(self.data[key][i]))
		return self.dict_data

	def getCompanies(self):
		for key in self.data.keys():
			self.list_companies.append(key)
		return self.list_companies

	def extract_dependent(self):
		self.dependent_variable = {list(self.data.keys())[0]:list(self.data[list(self.data.keys())[0]])} 
		for key in self.dependent_variable.keys():
			if key in self.list_companies:
				self.list_companies.remove(key)
			else:
				pass
			if key in self.dict_data.keys():
				del self.dict_data[key]
			else:
				pass
		return self.dependent_variable, self.list_companies, self.dict_data


if __name__ == '__main__':
	raw_data = DataFormating("../data/LearningSet.csv")
	data = raw_data.get_data()
	dict_data = raw_data.format_into_dict()
	companies = raw_data.getCompanies()
	dependent_variable, list_companies, dict_data = raw_data.extract_dependent()

	print(dependent_variable)
	print(list_companies)
	print(dict_data)

