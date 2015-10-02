buildModel <- setRefClass("buildModel",
	fields = list(data="data.frame", companies="character", rest ="character",
					dep="list", stationar="list", corr_vector="list", cut_off="list",
					limit="numeric", chosen="character", one_param_model="list",
					company="character", left="character", combo="list",
					best_in_class="list", llr="list", model_big="numeric",
					model_big="numeric"),
	methods = list(
		# correlation vector
		correlation_vector = function(dep, rest) {
			corr_vector <<- list()
			for (i in 1:length(rest)) {
				name <- rest[[i]]
				corr_vector[[name]] <<- as.numeric(cor(data[dep[[1]]], data[[name]]))
			}

			corr_vector
		},
		
		# correlational cut-off
		correlation_cutoff = function(corr_vector) {
			cut_off <<- list()
			cut_off <<- corr_vector[corr_vector > 0.3 | corr_vector < -0.3]
	
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
		},

		# one parameter model via correlation
		one_parameter_model = function(cut_off) {
			one_param_model<<-list()
			helper <- c()
			for (i in 1:length(cut_off)) {
				helper <- append(helper, cut_off[[i]])
			}
			max_cor <- max(helper)
			one_param_model <<- cut_off[cut_off == max_cor]
			print("Best one parameter model is: ")
			print(one_param_model)

			one_param_model
		},

		# companies chosen list
		# Don'tforget to get the company explicetly (<<- names(one_param_model)[1]) 
		companies_chosen = function(company) {
			chosen <<- append(chosen, company)

			chosen						
		},

		# companies left list
		companies_left = function(cut_off, chosen) {
			left <<- names(cut_off)[!(names(cut_off) %in% chosen)]

			left
		},

		# create combinations
		create_combinations = function(left, chosen) {
			combo <<- list()
 			for (i in 1:length(lf)) {
				name <- lf[[i]]         
				tmp <- c(name, ch)
				combo[[name]] <<- tmp
			}

			combo
		},
		
		# best model in the class
		best_model_in_class = function() {
			best_in_class <<- list()			
		},

		# LLR test with 5% error -> c= 0,004
		# if TRUE -> Hypothesis accepted and smaller model is better
		# if FALSE ->
		llr_test = function(model_big, model_small) {
			llr <<- list()
			llr <<- lrtest(model_big, model_small)
			# c <- 0.004
			# D <- lrtest(model_big, model_small)
			# if (D > c) {
			# 	llr <<- FALSE
			# }
			# else {
			# 	llr <<- TRUE
			# }

			llr
		}

		))


# # compare models from different classes -> using llr_test
# compare_models = function() {

# }

# # find best possible model for given data
# build_model = function() {

# } 
