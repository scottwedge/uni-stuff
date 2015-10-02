"""Class for model building:
1. Pre-process the data. Correlational cut-off.
2. Using step-forward approach, determine the 1-parameter model using Correlational
3. Build all possible models with fixed parameter from the previous step and """

from DataFormatting import *
import numpy
import statsmodels.api as sm 
import cProfile

class BuildModel:

	def __init__(self, dict_data, list_companies, dependent_variable, rest_companies, final_dict):
		self.dict_data = dict_data
		self.list_companies = list_companies
		self.dependent_variable = dependent_variable
		self.final_dict = final_dict

		self.correlation_with_Dependent = {}
		self.rest_companies = {}
		self.companies_chosen = []
		self.companies_left = []
		self.combinations = []
		self.model = ""
		self.company = ""
		self.smaller_model_list = []
		self.best_model_in_class = None
		self.rejected = True
		self.comparison_model_list = []
		self.info_small_model = None
		self.info_big_model = None
		self.resulting_model = None
		self.limit = 0

	# create correlational vector
	def correlation_vector(self):
		for key in self.dict_data.keys():
			if key != list(self.dependent_variable.keys())[0]:
				self.correlation_with_Dependent[key] = []
		for key in self.correlation_with_Dependent.keys():
			if key != list(self.dependent_variable.keys())[0]:
				self.correlation_with_Dependent[key] = numpy.corrcoef(self.dict_data[self.list_companies[0]], self.dict_data[key])[0][1] #ToDo compute dependant variable
		
		return self.correlation_with_Dependent

	# cut off all the companies with correlation lower than 30%
	def correlational_cutoff(self, correlation_vector):
		for key, value in correlation_vector.items():
			if value > 0.3 or value < -0.3:
				self.rest_companies[key] = value
			else:
				pass
		return self.rest_companies 

	# inner helper
	def companies_chosen_list(self, company):
		self.companies_chosen.append(str(company))
		
		return self.companies_chosen
	
	# inner helper
	def companies_left_list(self, cut_off, companies_chosen):
		for key in cut_off.keys(): 
			self.companies_left.append(key)
		for item in companies_chosen:
			if item in self.companies_left:
				self.companies_left.remove(item)
			else:
				pass
		
		return self.companies_left

	# helper function to create combinations from two arrays 
	def create_combinations(self, companies_left, companies_chosen):
		for item in companies_left:
			self.combinations.append([item])
		for i in range(0, len(self.combinations)):
			for item in companies_chosen:
				self.combinations[i].append(item)
		
		return self.combinations

	# choose the best model among the class
	# check, wether AIC works the same way
	def best_model_in_the_class(self, combinations):
		helper_dict = {}
		helper_list = []
		combinations_dict = {}
		y = self.dependent_variable[list(self.dependent_variable.keys())[0]]
		r_squared = {i: [] for i in range(0, len(combinations))}
		aic = {i: [] for i in range(0, len(combinations))} 
		for i in range(0, len(combinations)):
			combinations_dict[i] = combinations[i]
		#create weights
		#create proper data for Linear Regression
		for key in combinations_dict.keys():
			for i in range(0, len(self.dict_data['Intel'])):
				for item in combinations_dict[key]:
					helper_dict[i] = [v[i] for k, v in self.dict_data.items() if k in combinations_dict[key]]
					helper_list = [value for key, value in sorted(helper_dict.items())]
			model = sm.GLS(y, helper_list)
			regression = model.fit()
			r = regression.rsquared 
			akaike = regression.aic
			r_squared[key].append(r)
			aic[key].append(akaike)
		#map the results into final    
		determination_combination_dict = {}
		for k1 in combinations_dict.keys():
			for k2 in r_squared.keys():
				if k1 == k2:
					determination_combination_dict[float(r_squared[k2][0])] = list(combinations_dict[k1])

		# choose via AIC
		aic_combination_dict = {}
		for k1 in combinations_dict.keys():
			for k2 in aic.keys():
				if k1 == k2:
					aic_combination_dict[float(aic[k2][0])] = list(combinations_dict[k1])

		best_aic = min(aic_combination_dict.keys())
		self.best_model_in_class = aic_combination_dict[best_aic]

		#choose the best model among the class 
		#best_r = max(determination_combination_dict.keys())
		#self.best_model_in_class = determination_combination_dict[best_r]

		return self.best_model_in_class

	# build one parameter model based on correlation
	def one_parameter_model(self, cut_off):
		#extract the dependent variable from correlational vector
		cor_sorted = sorted(cut_off.values())
		max_cor = max(cor_sorted)
		for key, value in cut_off.items():
			if max_cor == value:
				self.model = "Best 1-parameter model is: "+ str(key) +" with "+ str(value) + " correlation"
				self.company = key
			else:
				pass
		for i in range(0, len(self.dict_data['Intel'])):
			self.smaller_model_list.append([self.dict_data[self.company][i]])
		
		return self.model, self.company, self.smaller_model_list

	# LLR test with 5% error -> c = 0,004 according to chi-square distribution table
	def llr_test(self, model_null, model_alternative):
		c = 0.004
		D = -2 * numpy.log(model_null/model_alternative)
		if (D  > c):
			self.rejected = False
		else:
			self.rejected = True
		
		return self.rejected 

	# inner helper
	def get_data_for_comparison(self, model):
		model_dict = {}
		for i in range (0, len(self.dict_data[list(self.dependent_variable.keys())[0]])):
			for item in model:
				model_dict[i] = [v[i] for k, v in self.dict_data.items() if k in model]
				self.comparison_model_list = [value for key, value in sorted(model_dict.items())]
		
		return self.comparison_model_list

	# set the limit on number of predictors in the final regression
	def set_the_limit(self, cut_off):
		total_number = len(cut_off)
		self.limit = 0
		self.limit += total_number//10
		if total_number%10>=5:
			self.limit += 1
		else:
			pass
		
		return self.limit

	# compare models via llr-test
	def compare_models(self, smaller_model_list, bigger_model_list):
		y = self.dependent_variable[list(self.dependent_variable.keys())[0]]
		
		model_null = sm.GLS(y, smaller_model_list)
		model_alternative = sm.GLS(y, bigger_model_list)
		
		params_null = sm.GLS(y, smaller_model_list).fit().params
		params_alternative = sm.GLS(y, bigger_model_list).fit().params
		
		null = model_null.loglike(params_null)
		alternative = model_alternative.loglike(params_alternative)
		
		self.info_small_model = model_null.fit().summary()
		self.info_big_model = model_alternative.fit().summary()
		
		self.rejected = self.llr_test(null, alternative)

		return self.rejected, self.info_small_model, self.info_big_model

	def build_the_model(self, cut_off):
		parameters_number = 2
		dependent_data = self.dependent_variable[list(self.dependent_variable.keys())[0]]
		resulting_model = None
		max_parameters = self.set_the_limit(cut_off)
		
		# 1. create smaller model
		small_model, company, smaller_model_list = self.one_parameter_model(cut_off)

		# 2. create combinations
		companies_chosen = self.companies_chosen_list(company)
		companies_left = self.companies_left_list(cut_off, companies_chosen)
		combinations = self.create_combinations(companies_left, companies_chosen)    

		# 3. choose best bigger model among the class
		big_model = self.best_model_in_the_class(combinations)
		bigger_model_list = self.get_data_for_comparison(big_model)

		# 4. compare the smaller and bigger models
		rejected, info_small_model, info_big_model = self.compare_models(smaller_model_list, bigger_model_list)

		# 5. if bigger -> redo 2 and 3, else print result
		# while дbigger model is better and limit is not reached
		while rejected and parameters_number < max_parameters:
			if rejected == False: # The smaller model is better, the search is over
				rejected = False
				print("the smaller model is better. the search is over")
				print(small_model, info_small_model)
				
				self.self.resulting_model = small_model
				break

			else: # rejected == True, the bigger model is better, search further
				rejected = True
				if parameters_number < max_parameters:
					for item in big_model:
						if item  not in companies_chosen:
							companies_chosen.append(item)
							companies_left.remove(item)
					small_model = big_model
					smaller_model_list = bigger_model_list
					combinations = self.create_combinations(companies_left, companies_chosen)
					big_model = self.best_model_in_the_class(combinations)
					bigger_model_list = self.get_data_for_comparison(big_model)
					rejected, info_small_model, info_big_model = self.compare_models(smaller_model_list, bigger_model_list)
				else:
					self.resulting_model = big_model
					break
			   
				self.resulting_model = big_model
			parameters_number += 1
			#print("current best model is ", str(self.resulting_model))
		print("The best model contains ", str(parameters_number), " parameters. And the model is: ", str(self.resulting_model))
		print(info_big_model)
		
		return self.resulting_model





if __name__ == '__main__':
	raw_data = DataFormatting("../data/LearningSet.csv")
	dict_data = raw_data.keep_dict()
	list_companies = raw_data.getAllCompanies()
	dependent_variable, rest_companies, dict_final = raw_data.extract_dependent()

	model_raw = BuildModel(dict_data, list_companies, dependent_variable, rest_companies, dict_final)
	cor_vec = model_raw.correlation_vector()
	cut_off = model_raw.correlational_cutoff(cor_vec)
	one_param, company, small_list = model_raw.one_parameter_model(cut_off)
	chosen = model_raw.companies_chosen_list(company)
	left = model_raw.companies_left_list(cut_off, chosen)
	comb = model_raw.create_combinations(left, chosen)
	bigger_model = model_raw.best_model_in_the_class(comb)
	data_compare = model_raw.get_data_for_comparison(bigger_model)
	compare, info_small, info_big = model_raw.compare_models(small_list, data_compare)
	#build_model = model_raw.build_the_model(cut_off)

	print(bigger_model)
	print(info_big)
