import requests
import sys
import getopt
import datetime
from bs4 import BeautifulSoup as bsoup

smasher = ''
show_t = 1

#filters
threshold = 1
year = 'ALL' #datetime.datetime.now().year
comp = '>='

options = getopt.getopt(sys.argv[1:], 's:t:y:c:')[0]
for i in range(4):
    try:
        o = options[i][0]
        v = options[i][1]
        if o == '-s':
            smasher = v
        elif o == '-t':
            if v.isnumeric():
                threshold = int(v)
        elif o == '-y':
            if v.isnumeric() or v.upper() == 'ALL':
                year = v
        elif o == '-c' and year.upper() != 'ALL':
            comp = v
    except: pass

if smasher == '':
    smasher = input('Smasher: ')
smasher = '_'.join(i[0].upper() + i[1:] for i in smasher.split(' '))

page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
soup = bsoup(page.content, "html.parser")
tables = soup.find_all('table', {'class': 'wikitable'})
results = []
year = str(year)
if year.upper() == 'ALL':
    year = tables[0].contents[3].contents[3].text.split(', ')[1]

for i in range(3, len(tables[0].contents), 2):
    t = tables[0].contents[i]
    
    t_name = t.contents[1].text
    t_year = int((t.contents[3].text)[-4:])
    t_place = str(t.contents[5].text).replace(' ', '')
    
    results += [[t_place, t_name, t_year]]


print('Will list tourney names for placings of ' + str(threshold) + ' or below.')
print(smasher + '\'s results for year ' + comp + ' ' + year + ':')
results = [i for i in results if i[0] != '—' and eval(str(i[2]) + comp + year)]
s = lambda x: int(''.join([k for j in x[0] for k in j if k.isnumeric()]))
results = sorted(results, key = s)
for i in range(len(results)):
    r = [i[0] for i in results if i[0] != '—']
    place = results[i][0]
    if results[i - 1][0] != place:
        count = r.count(place)
        print(place, '-', count)
        if show_t and s([place]) >= threshold:
            for k in range(len(results)):
                if results[k][0] == place:
                    try:
                        print(results[k][1], end = ' ')
                    except: pass
                    if comp != '==':
                        print('(' + str(results[k][2]) + ')', end = '')
                    print()
        print()
    
