"""Class for data formatting"""

import pandas as pd
import cProfile

class DataFormatting:

	def __init__(self, file_name):
		self.file_name = file_name
		self.data = pd.read_csv(str(self.file_name))
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
				pass	# stationary, moments, log_normal = collect_statistics(dict_data)
	# if False in stationary.values() and False in log_normal.values():
	# 	print("choose different model to build, deal with non stationary first")
	# else:
	# 	# create model and return the information
	# 	model_raw = BuildModel(dict_data, list_companies, dependent_variable, rest_companies, dict_final)
	# 	cor_vec = model_raw.correlation_vector()
	# 	cut_off = model_raw.correlational_cutoff(cor_vec)
	# 	build_model, predictions = model_raw.build_the_model(cut_off)

		# clean up the dependent_dict
		for key in self.dependent_variable.keys():
			for i in range(0, len(self.dependent_variable[key])):
				self.dependent_variable[key][i] = float("{0:.2f}".format(self.dependent_variable[key][i]))
		
		return self.dependent_variable, self.rest_companies, self.dict_final


if __name__ == '__main__':
	raw_data = DataFormatting("../data/LearningSet.csv")
	dict_data = raw_data.keep_dict()
	list_companies = raw_data.getAllCompanies()
	dependent_variable, rest_companies, dict_final = raw_data.extract_dependent()

	print(dict_final)
	#print(cProfile.run('data = pd.read_csv("../data/LearningSet.csv")'))
	



