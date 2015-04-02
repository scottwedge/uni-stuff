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


#Akaike criterion for choosing maximum number of the companies for regression
'''Algorithm 1'''
#As the first step, after statistical characteristics are figured out
#The correlation vector is computed, sorted 


#checking the AIC value for linera regresion from one explanatory variable
def build_reression(dict_data, list_data):
    #first company in the csv is ALWAYS! our dependent variable 
    result_dict = {}
    dependant = list_companies[0]
    dependent_variable = {list_companies[0]:dict_data[list_companies[0]]}
    del dict_data[dependant]
    #Preprocessing data into usable format for scikit.LinearRegression = sci_dict
    sci_dict = {}
    for key in dict_data.keys():
        sci_dict[key] = []
        for item in dict_data[key]:
            sci_dict[key].append([item])
    #first we will build the regression with 1 dexplanatory variable
    #count AIC, R² and regression's parameters
    #assume the regression y = ß0 + ß1*x
    for key in sci_dict.keys():
        regression = lm.LassoLarsIC()
        FitRegr = regression.fit(sci_dict[key], dependent_variable[list(dependent_variable.keys())[0]])
        RSquare = FitRegr.score(sci_dict[key], dependent_variable[list(dependent_variable.keys())[0]])
        result_dict["y=ß0+ß1*{}".format(key)] = [RSquare, FitRegr.criterion_[1]]
    #evaluation of the best regression based on min AIC value
    helper_list = []
    for k, v in result_dict.items():
        helper_list.append(v[0])
        best_r = max(helper_list)
        best_aic = min(helper_list)
    for key in result_dict.keys():
        if result_dict[key][0] == best_r:
            best = str(key) + " Is the best regression with R²: " + str(result_dict[key][0])
        else:
            pass
    #at this point we have chosen "best" variant among 1-variable-regressions
    
    return best

#Best combination of 5 from 68  
'''def best_regression(data):
    #the first column in the data set is ALWAYS the dependant variable
    companies_list = getCompanies(data)
    data_dict = formatDataIntoDict(data)
    dependant_variable = {companies_list[0]:dict_data[companies_list[0]]} #separate dependant and explanatory variables 
    for key in dependant_variable.keys():
        if key in list_companies:
            companies_list.remove(key)
        else:
            pass
        if key in data_dict.keys():
            del data_dict[key]
        else:
            pass
    #create all possible combinations 5 of 68
    comb_companies = []
    for item in itertools.combinations(list_companies, 5):
        comb_companies.append(item)

    #formating combinations into dictionary 
    test_combination_indexed = {}
    for item in comb_companies:
        test_combination_indexed = {i: comb_companies[i] for i in range(0, len(comb_companies))}

    r_square = {i: [] for i in range(0, len(test_combination_indexed.keys()))}  #create dict with R² as the key and combination as value, initiating the dictionary 
    final = {} #final dict is the resulting dictionary with r² as the key and corresponding combination as value
    combination_array_dict = {} #for every combination the dictionary will be overwritten to save memory
    combination_array_list = [] #formating the combination_array_dict to list to use LinearRegression
    #get R² for all combinations
    for key_index in test_combination_indexed.keys():
        for i in range(0, len(dict_data['Intel'])):
            combination_array_dict[i] = [value[i] for key, value in dict_data.items() if key in test_combination_indexed[key_index]] 
            combination_array_list = [value for key, value in sorted(combination_array_dict.items())]
        reg = lm.LinearRegression()
        test = reg.fit(combination_array_list, y)
        r = test.score(combination_array_list, y)
        r_square[key_index].append(r) 

    #final_dict getting values from the previous step
    for key1 in test_combination_indexed.keys():
        for key2 in r_square.keys():
            if key1 == key2:
                final[float(r_square[key2][0])] = list(test_combination_indexed[key1]) 
            else:
                pass

    #choose "best match" by taking combination with the highest R²
    best_r = max(dinal.keys())
    best_match = "The best combination of 5 companies from 68 given is: " + str(final(best_r)) + " with R²: " + str(best_r)

    return best_match'''
#make correlation vector
def correlation_vector(dict_data, list_companies):
    correlation_with_Intel = {}
    for key in dict_data.keys():
        correlation_with_Intel[key] = []
    for key in correlation_with_Intel.keys():
        correlation_with_Intel[key] = num.corrcoef(dict_data[list_companies[0]], dict_data[key])[0][1] #ToDo compute dependant variable
    return correlation_with_Intel

if __name__ == "__main__":
    '''Resulting outputs'''
    f = 'data/LearningSet.csv'
    data = getData(f)
    list_companies = getCompanies(data)
    dict_data = formatDataIntoDict(data)
    cor_vec = correlation_vector(dict_data, list_companies)
    #first cut-off, evrything with the correlation less than 30% is left out
    rest_companies = {}
    for key, value in cor_vec.items():
        if value > 0.3:
            rest_companies[key] = value
        else:
            pass
    #leave only data from the rest_companies
    dependant, companies, test_data = extract_dependant(rest_companies, list_companies)
    first_cutoff = {}
    for key in test_data.keys():
        first_cutoff[key] = dict_data[key]
    print(len(first_cutoff), first_cutoff)
    '''
    #get difference between original number of companies and rest after first cut off
    cut_temp = []
    for item in dict_data.keys():
        if item not in first_cutoff.keys():
            cut_temp.append(item)
        else:
            pass
    cut_temp.remove(list(dependant.keys())[0])
    print(len(cut_temp), cut_temp)'''

    #forward step-wise selection
    #rank companies according to their 
    #choosing the company with the highet correlation coefficient
    



    