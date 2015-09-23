"""Class for model building:
1. Pre-process the data. Correlational cut-off.
2. Using step-forward approach, determine the 1-parameter model using Correlational
3. Build all possible models with fixed parameter from the previous step and """

from DataFormating import *
import numpy 

class BuildModel:

	def __init__(self, dict_data, list_companies, dependent_variable, final_dict):
		self.dict_data = dict_data
		self.list_companies = list_companies
		self.dependent_variable = dependent_variable
		self.final_dict = final_dict

		self.correlation_with_Intel = {}
		self.rest_companies = {}
		self.limit = 0
		self.companies_left = []
		self.model = ""
		self.company = ""
		self.smaller_model_list = []
		self.companies_chosen = []
		self.combinations = []

	# Create correlation vector
	def correlation_vector(self):
		dependent_name = list(self.dependent_variable.keys())[0]
		for key in self.dict_data.keys():
			if  key != "Intel":
				self.correlation_with_Intel[key] = []
		for key in self.dict_data.keys():
			if key != "Intel":
				self.correlation_with_Intel[key] = numpy.corrcoef(self.dependent_variable[dependent_name], self.dict_data[key])[0][1]
			else:
				pass
			
		return self.correlation_with_Intel

	# Step 1 : reduce the amount data to process. Correlational cut-off. Border is set to 30% 
	def correlational_cutoff(self):
		self.correlation_with_Intel = self.correlation_vector()
		for key, value in self.correlation_with_Intel.items():
			if value > 0.3:
				self.rest_companies[key] = value
			else:
				pass

		return self.rest_companies

	# set the parameter number limit
	def set_the_limit(self):
		limited = self.correlational_cutoff()
		total_number = len(limited)
		self.limit += total_number // 10
		if total_number % 10 >= 5:
			self.limit += 1
		else:
			pass

		return self.limit

	# Step 2: build 1-parameter model using correlation_vector
	def one_parameter_model(self):
		# extract the dependent variable from correlational vector
		self.rest_companies = self.correlational_cutoff()
		cor_sorted = sorted(self.rest_companies.values())
		max_cor = max(cor_sorted)
		for key, value in self.rest_companies.items():
			if max_cor == value:
				self.model = "Best 1-parameter model is: "+ str(key) +" with "+ str(value) + " correlation"
				self.company = key
			else:
				pass
		for i in range(0, len(self.dict_data['Intel'])):
			self.smaller_model_list.append([self.dict_data[self.company][i]])

		return self.model, self.company, self.smaller_model_list 

	# inner helper
	def companies_chosen_list(self):
		self.companies_chosen.append(self.company)
		
		return self.companies_chosen

	# inner helper
	def companies_left_list(self):
		# initializing companies_left-list
		for key in self.rest_companies.keys(): 
			self.companies_left.append(key)
		# deleting chosen companies
		for item in self.companies_chosen:
			if item in companies_left:
				self.companies_left.remove(item)
			else:
				pass
		
		return self.companies_left

	# inner helper
	def create_combinations(self):
		for item in self.companies_left:
			combinations.append([item])
		for i in range(0, len(self.combinations)):
			for item in self.companies_chosen:
				self.combinations[i].append(item)

		return self.combinations

	# Compare models among the class, choose one for llr-test
	def best_model_in_the_class(self, dict_data, combinations):
		helper_dict = {}
		helper_list = []
		combinations_dict = {}
		r_squared = {i: [] for i in range(0, len(combinations))}
		for i in range(0, len(combinations)):
			combinations_dict[i] = combinations[i]
		#create weights
		#create proper data for Linear Regression
		for key in combinations_dict.keys():
			for i in range(0, len(dict_data['Intel'])):
				for item in combinations_dict[key]:
					helper_dict[i] = [v[i] for k, v in dict_data.items() if k in combinations_dict[key]]
					helper_list = [value for key, value in sorted(helper_dict.items())]
			model = sm.GLS(y, helper_list)
			regression = model.fit()
			r = regression.rsquared 
			r_squared[key].append(r)
		#map the results into final    
		determination_combination_dict = {}
		for k1 in combinations_dict.keys():
			for k2 in r_squared.keys():
				if k1 == k2:
					determination_combination_dict[float(r_squared[k2][0])] = list(combinations_dict[k1])

		#choose the best model among the class 
		best_r = max(determination_combination_dict.keys())
		best_model = determination_combination_dict[best_r]

		return best_model, determination_combination_dict, r_squared, helper_dict, helper_list




if __name__ == '__main__':
	raw_data = DataFormating("../data/LearningSet.csv")
	dict_data = raw_data.keep_dict()
	list_companies = raw_data.getAllCompanies()
	dependent_variable, rest_companies, dict_final = raw_data.extract_dependent()

	model = BuildModel(dict_data, list_companies, dependent_variable, dict_final)
	cor_vector = model.correlation_vector()

	model, company, smaller_model_list  = model.one_parameter_model()

	print(model)

