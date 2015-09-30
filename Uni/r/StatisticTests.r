statistic <- setRefClass("statistic",
	fields=list(data="data.frame", companies_list="character", stationar="list",
				cdf ="list", kde="list"),
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
				
				path_cdf <- file.path("img","CDF", paste("cdf_", companies_list[[i]], ".png", sep = ""))
				png(path_cdf)
				plot(graph[[name]], verticals = TRUE, do.points = FALSE, main=name)
				#dev.copy(png, path_cdf)
				dev.off()	
			}

			cdf
		}
		# # test for normal distribution, 15% error
		# normal_distribution = function(){
			
		# }
		

		))



# # test for log-normal distribution, 5% error
# lognormal_distribution <- function(){
	
# }


# # build kde
# build_kde <- function() {
	
# }

# # find moments: mean, var, skew, kurtosis
# find_moments <- function() {
	
# }

