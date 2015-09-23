"""Class for data formating"""

import pandas as pd

class DataFormating:

	def __init__(self, file_name):
		self.file_name = file_name
		self.data = pd.read_csv(str(self.file_name))
#		self.data = None
		self.dict_data = {}
		self.dict_final = {}
		self.list_companies = []
		self.rest_companies = []
		self.dependent_variable = {}

	# def get_data(self):
	# 	return self.data
	def keep_dict(self):
		for key in self.data.keys():
			self.dict_data[key] = []
		for key in self.dict_data.keys():
			for i in range(0,len(self.data[key])):
				self.dict_data[key].append(float(self.data[key][i]))
		
		return self.dict_data

	def format_into_dict(self):
		for key in self.data.keys():
			self.dict_final[key] = []
		for key in self.dict_final.keys():
			for i in range(0,len(self.data[key])):
				self.dict_final[key].append(float(self.data[key][i]))
		
		return self.dict_final

	def getAllCompanies(self):
		for key in self.data.keys():
			self.list_companies.append(key)
		
		return self.list_companies

	def getCompanies(self):
		for key in self.data.keys():
			self.rest_companies.append(key)
		
		return self.rest_companies

	def extract_dependent(self):
		self.dict_final = self.format_into_dict()
		self.rest_companies = self.getCompanies()
		self.dependent_variable = {list(self.data.keys())[0]:list(self.data[list(self.data.keys())[0]])} 
		for key in self.dependent_variable.keys():
			if key in self.rest_companies:
				self.rest_companies.remove(key)
			else:
				pass
			if key in self.dict_final.keys():
				del self.dict_final[key]
			else:
				pass
		# clean up the dependent_dict
		for key in self.dependent_variable.keys():
			for i in range(0, len(self.dependent_variable[key])):
				self.dependent_variable[key][i] = float("{0:.2f}".format(self.dependent_variable[key][i]))
		
		return self.dependent_variable, self.rest_companies, self.dict_final


if __name__ == '__main__':
	raw_data = DataFormating("../data/LearningSet.csv")
#	data = raw_data.get_data()
	dict_data = raw_data.keep_dict()
	list_companies = raw_data.getAllCompanies()
	dependent_variable, rest_companies, dict_final = raw_data.extract_dependent()

#	print('Intel' in dict_data.keys())
	print(dependent_variable)
	print("Intel" in list_companies)
	print("Intel" in dict_data.keys())
	print("Intel" in rest_companies)
	print("Intel" in dict_final.keys())


