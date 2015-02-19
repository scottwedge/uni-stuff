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
correlationMatrix = open('data/CorrelationMatrix.csv')
read_matrix = csv.reader(correlationMatrix, delimiter=',')
for row in read_matrix:
	companies.append(row[0])
	correlation_list.append(row[1])
correlation_list.remove('Intel')
for i in range(0,len(correlation_list)):
	correlation_list[i] = float(correlation_list[i])
companies.remove('')
#get the final dictionary to work with
correlation_dict = dict(zip(correlation_list, companies))
#clean our correlation_list - first-order cut-off
for coefficient in correlation_list:
	if (coefficient < -(0.25)) or (coefficient > 0.25):
		pass
	else:
		correlation_list.remove(coefficient)
#now we only get the names of the company that stayed for further analysis
difference = []
for key in correlation_dict.keys():
	if key not in correlation_list:
		companies.remove(correlation_dict[key])
		difference.append(correlation_dict[key])
	else:
		pass

print(len(correlation_list), correlation_list)
print(len(companies), companies)
#print(correlation_dict)
print(difference)
correlationMatrix.close()