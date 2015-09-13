"""Class for statistical tests"""


class StatisticTests:

	def __init__(self, dict_data):
		self.dict_data = dict_data
		self.stationary = {} 
		self.kolmogorov_dict = {}
	    self.logkolmogorov_dict = {}

	# helper for multiprocessing
	def passes_dftest(data):
	    if statmodel.adfuller(data[1], 250, 'ctt', 't-stat', False, False)[0] < 1:
	        return (data[0], True)
	    else:
	        return (data[0], False)

	#check week stationarity and stationary with Deakey-Fuller Test
	def stationarity(self):
	    for key in self.dict_data.keys():
	        self.stationary[key] = False
	    print(self.stationary.keys())
	    with Pool() as p:
	        p.map(passes_dftest, self.dict_data.items())
	    return self.stationary

	'''Test for distributions, 
	Hypothesis(0)=empirical DF is from tested distribution'''
	#Kolmogorov, distribution = normal, 15% error
	def kolmogorov_normal(self):
	    for key in self.dict_data.keys():
	        if stat.kstest(self.dict_data[key], 'norm', args=(num.average(self.dict_data[key]), num.std(self.dict_data[key])), N=1239)[0] < 0.032331:
	            self.kolmogorov_dict[key] = True
	        else:
	            self.kolmogorov_dict[key] = False
	    return self.kolmogorov_dict

	#Kolmogorov, distribution = lognormal, 5% error
	def kolmogorov_lognormal(self):
	    for key in self.dict_data.keys():
	        if stat.kstest(self.dict_data[key], 'lognorm', args=(num.average(self.dict_data[key]), num.std(self.dict_data[key])), N=1239)[0] < 1.039:
	            self.logkolmogorov_dict[key] = True
	        else:
	            self.logkolmogorov_dict[key] = False
	    return self.logkolmogorov_dict

	'''Here we build CDF and PDF for our data, save it to img/,
	compute 1, 2, 3 moments, variation'''
	#build CDF and save it under "CDF_of_copany"
	def build_cdf(self):
	    pdf_dict = dict_data
	    num_bins = 100
	    plt.figure()
	    for key in pdf_dict.keys():
	        counts, bin_edges = numpy.histogram(pdf_dict[key], bins = num_bins, normed=True)
	        cdf = numpy.cumsum(counts)
	        pdf_dict[key] = [cdf, bin_edges]
	        plt.title(key)
	        plt.plot(bin_edges[1:], cdf)
	        plt.savefig("img/CDF/CDF_of_{}.png".format(key))
	        plt.clf()
	    return pdf_dict

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
	    
	    return kde_dict 

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

if __name__ == '__main__':
	pass