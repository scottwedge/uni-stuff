from bs4 import BeautifulSoup
import urllib.request

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
final_list = []
for key in output.keys():
	for item in output[key]:
		if key != 2013:
			if item in output[key+1]:
				final_list.append(item)
		else:
			if item not in final_list:
				final_list.append(item)
print(final_list)
