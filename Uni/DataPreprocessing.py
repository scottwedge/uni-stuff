import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import numpy
from scipy import stats as stat
import statsmodels.api as sm
import statsmodels.tsa.stattools as statmodel
from multiprocessing import Pool
import itertools
import sklearn as sk
from sklearn import linear_model  as lm
from sklearn.tree import DecisionTreeRegressor


'''Data manipulation'''
def getData(file_name):
    data = pd.read_csv(str(file_name))
    return data

def formatDataIntoDict(data):
    dict_data = {}
    for key in data.keys():
        dict_data[key] = []
    for key in dict_data.keys():
        for i in range(0,len(data[key])):
            dict_data[key].append(float(data[key][i]))
    return dict_data

def getCompanies(data):
    list_companies = []
    for key in data.keys():
        list_companies.append(key)
    return list_companies

def extract_dependant(dict_data, list_companies):
    dependant_variable = {list_companies[0]:dict_data[list_companies[0]]} #separate dependant and explanatory variables 
    for key in dependant_variable.keys():
        if key in list_companies:
            list_companies.remove(key)
        else:
            pass
        if key in dict_data.keys():
            del dict_data[key]
        else:
            pass
    return dependant_variable, list_companies, dict_data

'''Test for: stationary, '''
def passes_dftest(data):
    print("Processing {}".format(data[0]))
    if statmodel.adfuller(data[1], 250, 'ctt', 't-stat', False, False)[0] < 1:
        return (data[0], True)
    else:
        return (data[0], False)

#check week stationarity and stationary with Deakey-Fuller Test
def stationarity(dict_data):
    stationary = {}
    #initiate output dictionary
    for key in dict_data.keys():
        stationary[key] = False
    print(stationary.keys())
    with Pool() as p:
        print("Starting parallel map")
        p.map(passes_dftest, dict_data.items())
    return stationary

'''Test for distributions, 
Hypothesis(0)=empirical DF is from tested distribution'''
#Kolmogorov, distribution = normal, 15% error
def kolmogorov_normal(dict_data):
    result_dict = {}
    for key in dict_data.keys():
        if stat.kstest(dict_data[key], 'norm', args=(num.average(dict_data[key]), num.std(dict_data[key])), N=1239)[0] < 0.032331:
            result_dict[key] = True
        else:
            result_dict[key] = False
    return result_dict

#Kolmogorov, distribution = lognormal, 5% error
def kolmogorov_lognormal(dict_data):
    result_dict = {}
    for key in dict_data.keys():
        if stat.kstest(dict_data[key], 'lognorm', args=(num.average(dict_data[key]), num.std(dict_data[key])), N=1239)[0] < 1.039:
            result_dict[key] = True
        else:
            result_dict[key] = False
    return result_dict

'''Here we build CDF and PDF for our data, save it to img/,
compute 1, 2, 3 moments, variation'''
#build CDF and save it under "CDF_of_copany"
def built_cdf(dict_data):
    pdf_dict = dict_data
    num_bins = 100
    plt.figure()
    for key in pdf_dict.keys():
        counts, bin_edges = num.histogram(pdf_dict[key], bins = num_bins, normed=True)
        cdf = num.cumsum(counts)
        pdf_dict[key] = [cdf, bin_edges]
        plt.title(key)
        plt.plot(bin_edges[1:], cdf)
        plt.savefig("img/CDF/CDF_of_{}.png".format(key))
        plt.clf()

#build smoothed with gaussian kernel PDF and save it under "KDE_of_company"
def build_kde(dict_data):
    plt.figure()
    kde_dict = dict_data
    for key in kde_dict.keys():
        kde = stat.gaussian_kde(kde_dict[key])
        xgrid = numpy.linspace(min(kde_dict[key]), max(kde_dict[key]), 100)
        plt.title(key)
        plt.hist(kde_dict[key], bins=100, normed=True, color="b")
        plt.plot(xgrid, kde(xgrid), color="r", linewidth=3.0)
        plt.savefig("img/KDE/KDE_of_{}.png".format(key))
        plt.clf()
    
    return pdf_dict, kde_dict 

#find skew and kurtosis
def findMoments(dict_data):
    #for every company find mean, var, skew, kurtosis
    result_dict = {}
    for key in dict_data.keys():
        result_dict[key] = [numpy.sum(dict_data[key])/len(dict_data[key]), numpy.std(dict_data[key]), stat.skew(dict_data[key]), stat.kurtosis(dict_data[key], fisher=True)]
    return result_dict

#bring the data to the normal distribution
def log_data(dict_data):
    log_data = {}
    for key in dict_data.keys():
        log_data[key] = []
        for item in dict_data[key]:
            new_item = numpy.log(item)
            log_data[key].append(new_item)
    return log_data


'''Helper functions, Tests'''
#different helper functions and tests:
def checkDictionary(dictionary,listCheck):
    result_value = False
    check_list = [False for i in range(0,len(listCheck))]
    for i in range(0, len(listCheck)):
        for key in dictionary.keys():
            if key in listCheck:
                check_list[i] = True
            else:
                check_list[i] = False
    for item in check_list:
        if False in check_list:
            result_value = False
        else:
            result_value = True
    return result

#helper function to create combinations from two arrays
def create_combinations(companies_left, companies_chosen):
    combinations = []
    #combinations.clear()
    for item in companies_left:
        combinations.append([item])
    for i in range(0, len(combinations)):
        for item in companies_chosen:
            combinations[i].append(item)
    return combinations


'''Algorithm 1: step-forward selection. Best model with one parameter computed.
The best model with 2 parameters computed. Both models are compared using LLR test.
If bigger model is better the iteration goes further until the set limit of parametrs not reached 
or until the smaller model woul be better'''

#make correlation vector
def correlation_vector(dict_data, list_companies):
    correlation_with_Intel = {}
    for key in dict_data.keys():
        correlation_with_Intel[key] = []
    for key in correlation_with_Intel.keys():
        correlation_with_Intel[key] = numpy.corrcoef(dict_data[list_companies[0]], dict_data[key])[0][1] #ToDo compute dependant variable
    return correlation_with_Intel


#in order to reduce the run time for a bit
def correlational_cutoff(border, correlation_vector):
    rest_companies = {}
    for key, value in correlation_vector.items():
        if value > border:
            rest_companies[key] = value
        else:
            pass
    return rest_companies 

#format data, build the regression (OLS) and choose the bset model among the class
def best_model_in_the_class(dict_data, combinations):
    helper_dict = {}
    helper_list = []
    combinations_dict = {}
    r_squared = {i: [] for i in range(0, len(combinations))}
    for i in range(0, len(combinations)):
        combinations_dict[i] = combinations[i]

    #create proper data for Linear Regression
    for key in combinations_dict.keys():
        for i in range(0, len(dict_data['Intel'])):
            for item in combinations_dict[key]:
                helper_dict[i] = [v[i] for k, v in dict_data.items() if k in combinations_dict[key]]
                helper_list = [value for key, value in sorted(helper_dict.items())]
        model = sm.OLS(y, helper_list)
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

"""Find 1-parameter regression"""
def one_parameter_model(correlational_cutoff_vector, list_companies, dict_data):
    #extract the dependent variable from correlational vector
    dependant, companies, test_data = extract_dependant(correlational_cutoff_vector, list_companies)
    cor_sorted = sorted(cut_off.values())
    max_cor = max(cor_sorted)
    model = ""
    company = ""
    for key, value in cut_off.items():
        if max_cor == value:
            model = "Best 1-parameter model is: "+ str(key) +" with "+ str(value) + " correlation"
            company = key
        else:
            pass
    smaller_model_list = []
    for i in range(0, len(dict_data['Intel'])):
        smaller_model_list.append([dict_data[company][i]])
    return model, company, smaller_model_list

"""Find two parameter regression"""
def two_parameter_model(companies_left, companies_chosen):
    pass

def llr_test(model_null, model_alternative, rejected):
    #LLR test itself, 5% error -> c = 0,004 according to chi-square distribution table
    c = 0.004
    D = -2 * numpy.log(model_null/model_alternative)
    if (D  > c):
        print("The Null-Hypothesis is confirmed")
        rejected = False
    else:
        print("The Null-Hypothesis is rejected")
        rejected = True
    return rejected 

#helper-function to format the data for further OLS-build
def get_data_for_comparison(best_model):
    model_dict = {}
    model_list = []
    for i in range (0, len(dict_data['Intel'])):
        for item in best_model:
            model_dict[i] = [v[i] for k, v in dict_data.items() if k in best_model]
            model_list = [value for key, value in sorted(model_dict.items())]
    return model_list

#helper-function to compare models
def compare_models(y, smaller_model_list, bigger_model_list):
    model_null = sm.OLS(y,smaller_model_list)
    model_alternative = sm.OLS(y, bigger_model_list)
    params_null = sm.OLS(y,smaller_model_list).fit().params
    params_alternative = sm.OLS(y, bigger_model_list).fit().params
    null = model_null.loglike(params_null)
    alternative = model_alternative.loglike(params_alternative)
    
    #use llr-test
    rejected = llr_test(null, alternative, flag)

    return rejected

def set_the_limit(cut_off):
    #set the limit on nnumbers of the parameters in the regression
    total_number = len(cut_off)
    limit = 0
    limit += total_number//10
    if total_number%10>=5:
        limit += 1
    else:
        pass
    return limit

if __name__ == "__main__":
    '''Resulting outputs'''
    f = 'data/LearningSet.csv'
    data = getData(f)
    list_companies = getCompanies(data)
    dict_data = formatDataIntoDict(data)
    dependant_variable = {'Intel': dict_data['Intel']}
    cor_vec = correlation_vector(dict_data, list_companies)
    #first cut-off, evrything with the correlation less than 30% is left out
    cut_off = correlational_cutoff(0.3, cor_vec)

    small_model, company, smaller_model_list = one_parameter_model(cut_off, list_companies, dict_data)
    print(small_model)

    """! Initialize companies left and companies chosen after finding first fixed parameter!"""
    #remember the company from the first iteration and delete from the general list
    companies_chosen = []
    companies_chosen.append(company)

    #initializing companies_left-list
    companies_left = []
    for key in cut_off.keys():
        companies_left.append(key)
    #deleting chosen companies
    for item in companies_chosen:
        if item in companies_left:
            companies_left.remove(item)
        else:
            pass

    combinations = create_combinations(companies_left, companies_chosen)    

    #dependent data
    y = dict_data['Intel']
    
    big_model, final, r_squared, helper_dict, helper_list = best_model_in_the_class(dict_data, combinations)

    #create model for further comparison
    bigger_model_list = get_data_for_comparison(big_model)
    
    #global variable, status flag for the second global condition, here we think that bigger model will be always better
    flag = True

    #compare two models (1 vs 2)
    rejected = compare_models(y, smaller_model_list, bigger_model_list)

    if rejected == False:
        print("the smaller model is better. the search is over", small_model)
    else:
        print("the bigger model is better. Search further", big_model)
        #extract the best models
        for item in big_model:
            if item in companies_chosen:
                pass
            else:
                companies_chosen.append(item)
                companies_left.remove(item)
                small_model = big_model
                smaller_model_list = bigger_model_list

    #(2 vs 3)
    #if the bigger model is better, than the smaller one AND limit is not reached build new model
    #1. Build new combiantions
    combinations = create_combinations(companies_left, companies_chosen)
    #2. Format data for model searching
    #rewrite small and big ones
    big_model, final, r_squared, helper_dict, helper_list = best_model_in_the_class(dict_data, combinations)
    bigger_model_list = get_data_for_comparison(big_model)
    rejected = compare_models(y, smaller_model_list, bigger_model_list)
    if rejected == False:
        print("the smaller model is better. the search is over", small_model)
    else:
        print("the bigger model is better. Search further", big_model)
        #extract the best models
        for item in big_model:
            if item in companies_chosen:
                pass
            else:
                companies_chosen.append(item)
                companies_left.remove(item)
                small_model = big_model
                smaller_model_list = bigger_model_list
    #3vs4
    combinations = create_combinations(companies_left, companies_chosen)
    big_model, final, r_squared, helper_dict, helper_list = best_model_in_the_class(dict_data, combinations)
    bigger_model_list = get_data_for_comparison(big_model)
    rejected = compare_models(y, smaller_model_list, bigger_model_list)
    if rejected == False:
        print("the smaller model is better. the search is over", small_model)
    else:
        print("the bigger model is better. Search further", big_model)
        #extract the best models
        for item in big_model:
            if item in companies_chosen:
                pass
            else:
                companies_chosen.append(item)
                companies_left.remove(item)
                small_model = big_model
                smaller_model_list = bigger_model_list




