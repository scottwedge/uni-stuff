#!/usr/bin/r.
# helper functions to test run time
data_read <- function() {
	source("DataFormatting.r")
	d <- getData(name="../data/LearningSet.csv")
	build_data <- d$get_data()
	companies <- d$get_list_companies(build_data)
	dependent <- d$extract_dependent(companies)
	rest <- d$get_rest_companies(dep, companies)
}

stat <- function(build_data, companies) {
	source("StatisticTests.r")
	s <- statistic(data=build_data, companies_list=companies)
	stationary <- s$stationary()
	cdf <- s$build_cdf()
	kde <- s$build_hist()
	moments <- s$find_moments()
	normal <- s$normal_distribution()
	lognormal <- s$lognormal_distribution()
}

model <- function(build_data, companies, rest, dependent) {
	source("BuildModel.r")
	b <- buildModel(data=build_data, companies=companies, rest=rest, dep=dependent)
	corr_vector <- b$correlation_vector(dependent, rest)
	corr_cutoff <- b$correlation_cutoff(corr_vector)

	best_model <- b$build_model(corr_cutoff)
	# print(summary(best_model[[2]][[1]]))
}

main <- function() {
	# activate libraries
	library(nlme)
	library(stats)
	library(tseries)
	library(moments)
	library(hydroGOF)

	# create data class
	source("DataFormatting.r")
	d <- getData(name="../data/LearningSet.csv")
	build_data <- d$get_data()
	companies <- d$get_list_companies(build_data)
	dependent <- d$extract_dependent(companies)
	rest <- d$get_rest_companies(dependent, companies)

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
		# print("Choose different model to build dependencies")
	}
	else {
		source("BuildModel.r")
		b <- buildModel(data=build_data, companies=companies, rest=rest, dep=dependent)
		corr_vector <- b$correlation_vector(dependent, rest)
		corr_cutoff <- b$correlation_cutoff(corr_vector)

		best_model <- b$build_model(corr_cutoff)
		# print(summary(best_model[[2]][[1]]))

	}

	best_model

}

# returns predictions vector, differencies vector, average error, max eror
build_predictions <- function() {
	predictions <- list()

	# get data.frame to build predictions
	t <- getData(name="../data/TestingSet.csv")
	test_data <- t$get_data()

	d <- getData(name="../data/LearningSet.csv")
	build_data <- d$get_data()

	#get gls model
	# original model
	model <- gls(Intel ~ Olympus + Cardinal + St.Jude + MicronTech + STMElectro + Lenovo, build_data)
	# new model
	#model <- gls(Intel ~ Olympus + Google + St.Jude + MicronTech + STMElectro + Lenovo, build_data)
	pv <- predict(model, test_data)
	dv <- (test_data$Intel - pv)
	mean_pred <- mean(pv)
	std_pred <- sd(pv)
	ab_er <- mae(pv, test_data$Intel)
	sqrmer <- rmse(pv, test_data$Intel)

	png("../RPredicitions.png")
	plot(test_data$Intel, type="l", col="grey", ann=FALSE)
	par(new=TRUE)
	plot(pv, type="l", col="green", axes=FALSE, ann=FALSE)
	legend("top", c("Real Prices", "Predictions"), lty=c(1,1), lwd=c(1.5,1.5), col=c("grey", "green"))
	dev.off()

	predictions$model <- model
	predictions$predictions <- pv
	predictions$difference <- dv
	predictions$errors <- list(mean=mean_pred, std=std_pred, mean_er=ab_er, std_er=sqrmer)

	print("the mean of the y is: ")
	print(mean(test_data$Intel))
	print("the std of the y is: ")
	print(sd(test_data$Intel))
	print("the mean of the predictions is: ")
	print(mean_pred)
	print("the std of the predictions is: ")
	print(std_pred)
	print("the mean absolute error of the predictions is: ")
	print(ab_er)
	print("the root mean squared error of the predictions is: ")
	print(sqrmer)

	predictions
}

