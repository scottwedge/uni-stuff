import pandas as pd
import datetime
import matplotlib.pyplot as plt 
import numpy as num
from scipy import stats as stat
import statsmodels.tsa.stattools as statmodel
from multiprocessing import Pool
import itertools
import math
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

def extract_company(parameter_fixed, ):
    extractable = []


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
        xgrid = num.linspace(min(kde_dict[key]), max(kde_dict[key]), 100)
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
        result_dict[key] = [num.sum(dict_data[key])/len(dict_data[key]), num.std(dict_data[key]), stat.skew(dict_data[key]), stat.kurtosis(dict_data[key], fisher=True)]
    return result_dict

#bring the data to the normal distribution
def log_data(dict_data):
    log_data = {}
    for key in dict_data.keys():
        log_data[key] = []
        for item in dict_data[key]:
            new_item = math.log(item)
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
        correlation_with_Intel[key] = num.corrcoef(dict_data[list_companies[0]], dict_data[key])[0][1] #ToDo compute dependant variable
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

"""Find 1-parameter regression"""
def one_parameter_model(correlational_cutoff_vector, list_companies):
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
    return model, company

"""Find two parameter regression"""
def two_parameter_model(company,correlational_cutoff_vector):
    pass

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

    one_parameter_model, company = one_parameter_model(cut_off, list_companies)
    print(one_parameter_model)
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

    #let's create test combination Olympus, Google = combinations
    helper_dict = {i: [] for i in range(0, len(dict_data['Intel']))}
    helper_list = []
    combinations = ['Olympus', 'Google']

    y = dict_data['Intel']

    for i in range(0, len(dict_data['Intel'])):
        for item in combinations:
            helper_dict[i].append(dict_data[item][i])
        helper_list.append(helper_dict[i])

    reg = lm.LinearRegression()
    fit = reg.fit(helper_list, y)
    score = fit.score(helper_list, y)    

    print(dict_data['Olympus'])
    print(dict_data['Google'])
    print("R² of the combination is: ", score)
'''
    #create regression for combinations from chosen and one free parameters, choose best regression among the class with R²
    r_square = {}
    final = {} #final dict is the resulting dictionary with r² as the key and corresponding combination as value
    helper_dict = {} #for every combination the dictionary will be overwritten to save memory
    helper_list = [] #formating the combination_array_dict to list to use LinearRegression
    helper_combination = {}
    helper_coeff = {}
    #create combonations
    combination_list = []
    for item in companies_left:
        combination_list.append([item])
    for i in range(0, len(combination_list)):
        for element in companies_chosen:
            combination_list[i].append(element)
    for i in range(0, len(combination_list)):
        helper_combination[i] = combination_list[i]
        helper_coeff[i] = []

    #create dependent varibale array
    y = dict_data['Intel']
    
    for i in range(0, len(dict_data['Intel'])):
        for item in combination_list:
            helper_dict[i] = []
            for element in item:
                helper_dict[i].append(dict_data[element][i]) 
        helper_list.append(helper_dict[i])  
        reg = lm.LinearRegression()
        #fit = reg.fit(helper_list, y)
'''


