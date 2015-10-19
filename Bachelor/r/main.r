# required packages: nlme, stats, tseries, moments
# make sure they are installed
# run library(library_name) for each library


main <- function() {
	# activate libraries
	library(nlme)
	library(stats)
	library(tseries)
	library(moments)

	# create data class
	source("DataFormatting.r")
	d <- getData(name="../data/LearningSet.csv")
	build_data <- d$get_data()
	companies <- d$get_list_companies(build_data)
	dependent <- d$extract_dependent(companies)
	rest <- d$get_rest_companies(dep, companies)

	# get statistics 
	source("StatisticTests.r")
	s <- statistic(data=build_data, companies_list=companies)
	stationary <- s$stationary()
	cdf <- s$build_cdf()
	kde <- s$build_hist()
	moments <- s$find_moments()
	normal <- s$normal_distribution()
	lognormal <- s$lognormal_distribution()

	# build the model
	if (FALSE %in% stationary) {
		print("Choose different model to build dependencies")
	}
	else {
		source("BuildModel.r")
		b <- buildModel(data=build_data, companies=companies, rest=rest, dep=dependent)
		corr_vector <- b$correlation_vector(dependent, rest)
		corr_cutoff <- b$correlation_cutoff(corr_vector)

		best_model <- b$build_model(corr_cutoff)
		print(summary(best_model[[2]][[1]]))

	}

	best_model

}