buildModel <- setRefClass("buildModel",
	fields = list(data="data.frame", companies="character", rest ="character",
					dep="list", stationar="list", corr_vector="list", cut_off="list",
					limit="numeric", chosen="character", one_param_model="list",
					company="character", left="character", combo="list",
					best_in_class="list", llr="logical", compared="list", final_model="list"),
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
			# print("Best one parameter model is: ")
			# print(one_param_model)

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
 			for (i in 1:length(left)) {
				name <- left[[i]]         
				tmp <- c(name, chosen)
				combo[[name]] <<- tmp
			}

			combo
		},
		
		# best model in the class
		# use nlme
		best_model_in_class = function(combo) {
			best_in_class <<- list()
			form <- list()
			for(i in 1:length(combo)) {  
				name <- names(combo)[i]                               
				temp1<-"Intel ~ "
				temp2<-paste(combo[[i]][1:length(combo[[i]])], collapse=" + ")
				form[[name]] <- paste(temp1, temp2, collapse=" ")
			}
			form
			aic <- list()
			model_list <- list()
			for(k in names(combo)) {                                                                     
				for(k1 in names(form)) {                                                                      
					if(k == k1){                                                                                
						aic[[k]] <- summary(gls(as.formula(form[[k1]]), data))$AIC  
						model_list[[k]] <- gls(as.formula(form[[k1]]), data)                                              
			}}}   
			min_aic <- min(as.numeric(aic[1:length(aic)]))
			for(i in 1:length(aic)) {
				if(min_aic == aic[[i]]) {
					best_in_class <<- list(aic[i],model_list[i])
				}
			}

			best_in_class			
		},

		# LLR test with 5% error -> c= 0,004
		# use lmtest
		llr_test = function(model_small, model_big) {

			llr <<- logical()
			#llr <<- lrtest(model_big, model_small)
			c <- 0.004
			D <- -2*log(as.numeric(logLik(model_small))/as.numeric(logLik(model_big)))
			if (D > c) {
				llr <<- FALSE # Hypothesis is excepted, smaller model is better
			}
			else {
				llr <<- TRUE # Hypothesis is wrong, bigger model is better
			}

			llr
		},

		# compare models from different classes -> using llr_test
		compare_models = function(model_small, model_big) {
			compared <<- list()
			llr_temp <- llr_test(model_small, model_big)
			if(llr_temp == FALSE) {
				compared <<- list(llr_temp, model_small, "smaller model is better, search is over")
			}
			else {
				compared <<- list(llr_temp, model_big, "bigger model is better, search continues")
			}

			compared
		},

		# find best possible model for given data
		build_model = function(cut_off) {
			library(lmtest)
			require(lmtest)
			library(nlme)
			require(nlme)

			final_model <<- list()
			# set limit on parameters in the regression
			limit_helper <- set_limit(cut_off)
			# create smaller model via one_parameter_model
			small_model <- one_parameter_model(cut_off)
			small <- gls(as.formula(paste(dep$name,"~", as.character(names(small_model)), collapse="")), data)
			# create bigegr model via best_in_class
			comp_helper <- names(small_model)
			comp_chosen <- companies_chosen(comp_helper)
			comp_left <- companies_left(cut_off, comp_chosen)
			combo_helper <- create_combinations(comp_left, comp_chosen)
			big_model <- best_model_in_class(combo_helper)
			# compare models via compare models
			comparison <- compare_models(small, big_model[[2]][[1]])
			# here goes while loop 
			flag <- TRUE
			parameter <- 2
			while (flag & (parameter < limit_helper)) {
				if(flag==FALSE) {
					print("The smaller model is better, The search is over")

					final_model <<- list(small, summary(small))
					break
				}
				else {
					if (parameter < limit_helper) {
						comp_helper <- names(big_model[[1]])
						comp_chosen <- companies_chosen(comp_helper)
						comp_left <- companies_left(cut_off, comp_chosen)
						small<-big_model[[2]][[1]]
						combo_helper <- create_combinations(comp_left, comp_chosen)
						big_model <- best_model_in_class(combo_helper)
						flag <- compare_models(small, big_model[[2]][[1]])[[1]]
						parameter <- parameter + 1
						print("The parameters limit is not reached, searching further")

					}
					else {
						final_model <<- big_model
						break
					}
					# print("the big model is better and the number of parameter reached its max")
				}

				final_model <<- big_model
			}
			parameter <- parameter + 1

			final_model

		}

		))



