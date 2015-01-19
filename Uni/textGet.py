from bs4 import BeautifulSoup
import urllib.request
import re

url = "http://en.wikipedia.org/wiki/Semiconductor_sales_leaders_by_year#Ranking_for_year_2013"
soup = BeautifulSoup(urllib.request.urlopen(url))

years = list(range(2000, 2013+1))
output = {year:[] for year in years}
for year in years:
	headline = soup.find(id="Ranking_for_year_{}".format(year))
	table = headline.parent.find_next_sibling("div").table
	for row in table.find_all("tr")[1:20]:
		cells = row.find_all("td")
		output[year].append(cells[2].text)


#clean the dctionary from unneded info
def clean_list(dic):
	new = {}
	for key in output.keys():
		new[key] = []
		for item in output[key]:
			new[key].append(re.sub(r'\s?\(.*\)', '', str(item)))
	return new


output = clean_list(output)

#get all the companies, that worked through 2000-2013
all_companies = []


for key in output.keys():
	for item in output[key]: 
		if item not in  all_companies:
			all_companies.append(item)
counter = {value: 0 for value in all_companies} #initial dict

#take those companies, who were listed at least 11 years out of 14
for key in counter.keys():
	for key_j in output.keys():
		if key in output[key_j]:
			counter[key] = counter[key] + 1
		else:
			counter[key] = counter[key] + 0
final_list = []
for key in counter.keys():
	if counter[key] > 10:
		final_list.append(key)
	else:
		pass

print(final_list, len(final_list))


