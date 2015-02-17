import csv
import statistics

data_dict = {}
helper_list = []
average = 0;
learningSet = open('data/LearningSet.csv')
read_it = csv.DictReader(learningSet, delimiter=',')
#getting list of companies for keys in our data_dict 
for row in read_it:
	for company_key in row.keys():
		if company_key not in data_dict:
			data_dict[company_key] = []

		data_dict[company_key].append(float(row[company_key]))

#data_dict={(companies[i] for i in range(0,len(companies))):[] }
for k, v in data_dict.items():
	print(k, v)
#print(data_dict)
learningSet.close()