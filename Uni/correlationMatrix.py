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

learningSet.close()
#companies correlated with intel
companies = []
correlation_list = []
correlation_dict = {}
indexes = list(range(0,71))
correlationMatrix = open('data/CorrelationMatrix.csv')
read_matrix = csv.reader(correlationMatrix, delimiter=',')
for row in read_matrix:
	companies.append(row[0])
	correlation_list.append(row[1])
#companies_dict = {companies[]:[]}
correlation_dict = {str(correlation_list[0]):[float(correlation_list[i]) for i in range(1,len(correlation_list))]}
#choosing the final companies
important_companies = []
#print(correlation_dict)
print(correlation_dict)
correlationMatrix.close()