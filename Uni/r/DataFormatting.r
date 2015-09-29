getData <- setRefClass("getData",
	fields = list( name = "character", data = "data.frame", list_companies="character",
					dependent_variable = "list", rest_companies = "character"),
	methods = list( 

		get_data = function() {
			data <<- read.csv(name, header = TRUE, sep = ",", quote = "\"", dec = ".", fill = TRUE, comment.char = "")
			data
		},

		get_list_companies = function(data_frame) {
			list_companies <<- colnames(data_frame)
			list_companies
		},
		
		extract_dependent = function(list_companies) {
			dependent_name <- as.character(list_companies[[1]])
			dependent_variable <<- list(name=dependent_name, value=c(data[[dependent]]))
			dependent_variable
		},

		get_rest_companies = function(dependent, list_companies) {
			rest_companies <<- list_companies[list_companies != dependent$name]
			rest_companies
		}
	))






# we assume, that we can anytime iterate over data.frame.
# so rest_companies are just for keeping track

# data <- get_data("../data/LearningSet.csv")
# list_companies <- get_list_companies(data)
# dependent_variable <- extract_dependent(list_companies)
# rest_companies <- get_rest_companies(dependent_variable, list_companies)