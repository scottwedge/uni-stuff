buildModel <- setRefClass("buildModel",
	fields = list(data="data.frame", companies="character", rest ="character",
					dep="list", stationar="list", corr_vector="list"),
	methods = list(
		# correlation vector
		correlation_vector = function(dep, rest) {
			corr_vector <<- list()
			for (i in 1:length(rest)) {
				name <- rest[[i]]
				tmp <- list(cor(data[dep[[1]]], data[[name]]))
				corr_vector[[name]] <<- tmp
			}

			corr_vector
		}
		


		))

# # correlational cut-off
# correlational_cutoff = function() {
	
# }

# # set the limit
# set_limit = function() {

# }

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
