from bs4 import BeautifulSoup
import urllib.request

url_1 = 'http://en.wikipedia.org/wiki/Automotive_industry'
soup = BeautifulSoup(urllib.request.urlopen(url_1))

ranks = list(range(1, 31))
output = {rank:[] for rank in ranks}
#get the table in a list form
headline = soup.find(id="By_manufacturer")
table = headline.parent.find_next_sibling("table")

for row in table.find_all("tr")[1:31]:
	cells = row.find_all("td")
	for rank in ranks:
		output[rank].append(cells[1].text)

list_outers = ['Toyota', 'GM', 'Volkswagen', 'Ford', 'Nissan', 
'Fiat Chrysler Automobiles', 'Honda', 'PSA',
'BMW', 'Daimler AG', 'Tata', 'Fuji']

		
url_2 = 'http://www.gsmarena.com/makers.php3'
soup_2 = BeautifulSoup(urllib.request.urlopen(url_2))

output_diversified = []
#get needed element
headline_2 = soup_2.find(id="brandmenu")
table_2 = headline_2.ul
for i in table_2.find_all("li"):
	list_div = i.find_all("a")
	output_diversified.append(i.text)

print("length:" + str(len(output_diversified)), output_diversified)



