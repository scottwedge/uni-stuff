from bs4 import BeautifulSoup
import urllib.request
import re

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

#print("length:" + str(len(output_diversified)), output_diversified)

#medical divicesmanufacturers
url_3 = "http://www.mddionline.com/article/top-40-medical-device-companies"
soup_3 = BeautifulSoup(urllib.request.urlopen(url_3))
output_medical = []
headline_3 = soup_3.find(id="article_title")
table_3 = headline_3.find_next_sibling("table")
for row in table_3.find_all("tr")[1:40]:
	cells = row.find_all("td")
	output_medical.append(cells[1].text)

def clear_medic(list_in):
	for item in list_in:
		item = re.sub(r'\s?\\.*\n', '', str(item))

#output_medical_new = clear_medic(output_medical)
print(output_medical)



