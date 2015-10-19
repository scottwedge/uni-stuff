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

# returns predictions vector, differencies vector, average error, max eror
build_predictions <- function() {
	predictions <- list()

	# get data.frame to build predictions
	t <- getData(name="../data/TestingSet.csv")
	test_data <- t$get_data()

	d <- getData(name="../data/LearningSet.csv")
	build_data <- d$get_data()

	#get gls model
	model <- gls(Intel ~ Olympus + Cardinal + St.Jude + MicronTech + STMElectro + Lenovo, build_data)
	pv <- predict(model, test_data)
	dv <- (test_data$Intel - pv)
	average <- mean(dv)
	max <- max(dv)
	min <- min(dv)
	if(max > (-1 * min)) {
		dev <- max
	}
	else {
		dev <- min
	}

	png("Predicitions")
	plot(test_data$Intel, type="l", col="red", ann=FALSE)
	par(new=TRUE)
	plot(pv, type="l", col="blue", axes=FALSE, ann=FALSE)
	legend("top", c("Real Prices", "Predictions"), lty=c(1,1), lwd=c(1.5,1.5), col=c("red", "blue"))
	dev.off()

	predictions$predictions <- pv
	predictions$difference <- dv
	predictions$errors <- list(average=average, dev=dev)

	predictions
}