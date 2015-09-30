statistic <- setRefClass("statistic",
	fields=list(data="data.frame", companies_list="character", stationar="list",
				cdf ="list", kde="list", hist_den="list", moments="list", normal="list", lognormal="list"),
	methods=list(
		# check stationary
		stationary = function() {
			stationar <<- list()
			for(company in companies_list) {

				if (as.numeric(adf.test(data[[company]])[1]) > -3.43) {
					stationar <<- c(stationar$company<<- list(company, "True"), stationar)
				} else {
					stationar <<- c(stationar$company<<- list(company, "False"), stationar)
				}
			}
			
			stationar

		},

		# build cdf
		build_cdf = function() {
			cdf <<-list()
			graph <- list()
			for(i in 1:length(companies_list)) {
				name <- companies_list[[i]]
				tmp <- list(sort(ecdf(data[[name]])(data[[name]])))
				graph_temp <- ecdf(data[[name]])
				graph[[name]] <- graph_temp 
				cdf[[name]] <<- tmp 
				
				path_cdf <- file.path("img","CDF", paste("cdf_", name, ".png", sep = ""))
				png(path_cdf)
				plot(graph[[name]], verticals = TRUE, do.points = FALSE, main=name)
				#dev.copy(png, path_cdf)
				dev.off()	
			}

			cdf
		},

		# build kde
		build_hist = function() {
			hist_den <<- list()
			for (i in 1:length(companies_list)) {
				name <- companies_list[[i]]
				x <- data[[name]]
				path_kde <- file.path("img","KDE", paste("kde_", name, ".png", sep = ""))
				png(path_kde)
				hist(x, prob=TRUE)
				lines(density(x))
				dev.off()

			}
			hist_den
			
		},

		# find moments: mean, standart deviation, skew, kurtosis
		find_moments = function() {
			moments <<- list()
			for (i in 1:length(companies_list)) {
				name <- companies_list[[i]]
				tmp <- list(mean(data[[name]]), sd(data[[name]], na.rm = FALSE), skewness(data[[name]]), kurtosis(data[[name]]))
				moments[[name]] <<- tmp
			}

			moments
		},

		# test for normal distribution, 15% error
		normal_distribution = function(){
			normal <<- list()
			norm_vec <- rnorm(length(data[[companies_list[[1]]]]))
			for (i in 1:length(companies_list)) {
				name <- companies_list[[i]]
				tmp <- (ks.test(data[[name]], norm_vec)[[1]][[1]]< 0.032331)
				normal[[name]] <<- tmp
			}

			normal
		},
		
		# test for log-normal distribution, 5% error
		lognormal_distribution = function(){
			lognormal <<- list()
		}

		))






