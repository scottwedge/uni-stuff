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
print(len(list_outers))
		
url_2 = 'http://www.statista.com/statistics/264366/revenue-of-the-worldwide-leading-aircraft-manufacturers-and-suppliers/'
soup_2 = BeautifulSoup(urllib.request.urlopen(url_2))

ranks = []


