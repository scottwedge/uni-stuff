buildModel <- setRefClass("buildModel",
	fields = list(data="data.frame", companies="character", rest ="character",
					dep="list", stationar="list", corr_vector="list", cut_off = "list",
					limit="numeric"),
	methods = list(
		# correlation vector
		correlation_vector = function(dep, rest) {
			corr_vector <<- list()
			for (i in 1:length(rest)) {
				name <- rest[[i]]
				tmp <- cor(data[dep[[1]]], data[[name]])
				corr_vector[[name]] <<- tmp
			}

			corr_vector
		},
		
		# correlational cut-off
		correlation_cutoff = function(corr_vector) {
			cut_off <<- list()
			for (i in 1:length(corr_vector)) {
				name <- corr_vector[[i]]
				cut_off <<- corr_vector[corr_vector > 0.3 | corr_vector < -0.3] 
			}	

			cut_off		
		},

		# set the limit
		set_limit = function(cut_off) {
			limit<<-0
			whole <- length(cut_off)%/%10
			if (length(cut_off)%%10 >= 5) {
				part <- 1
			}
			else {
				part <-0
			}
			limit<<- whole + part

			limit
		}

		))



# # companies chosen list
# companies_chosen = function() {
	
# }

# # companies left list
# companies_left = function() {
	
# }

# # one parameter model via correlation
# one_parameter_model = function() {
	
# }

# # create combinations
# create_combinations = fonction() {
	
# }

# # best model in the class
# best_in_class = function() {
	
# }

# # llr_test
# llr_test = function() {

# }

# # compare models from different classes -> using llr_test
# compare_models = function() {

# }

# # find best possible model for given data
# build_model = function() {

# } 
