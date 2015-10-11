main <- setRefClass("main",
	fields = list(name="character",data_list="list", final_model="list",
		predictions="list"),
	
	methods = list(

		collect_data = function(name) {

			source("DataFormattinf.r")
			d <- getData(name)
			data <- d$get_data()
			companies <- d$get_list_companies(data)
			dep <- d$extract_dependent(companies)
			rest <- d$get_rest_companies(dep, companies)
			data_list <<- c(data, data_list)
			data_list <<- c(companies, data_list)
			data_list <<- c(dep, data_list)
			data_list <<- c(rest, data_list)
			

		},

		))