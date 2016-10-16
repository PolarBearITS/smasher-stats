import requests
import sys
import getopt
import datetime
from bs4 import BeautifulSoup as bsoup

smasher = ''
show_t = 1

#filters
threshold = 5
year = datetime.datetime.now().year #'ALL'
comp = '>='
game = 'Melee'

flags = 's:t:y:c:g:'
options = getopt.getopt(sys.argv[1:], flags)[0]
for i in range(len(flags)//2):
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
        elif o == '-g':
            game = v
    except: pass

games = [
    ['MELEE', 'SMASH MELEE', 'SMASH BROS MELEE', 'Super Smash Bros. Melee'],
    ['64', 'SMASH 64', 'SUPER SMASH BROS 64', 'Super Smash Bros.'],
    ['BRAWL', 'SMASH BROS BRAWL', 'SMASH BRAWL', 'Super Smash Bros. Brawl'],
    ['SM4SH', 'SMASH 4', 'SMASH WII U', 'SMASH BROS 4', 'SMASH BROS WII U', 'SMASH BROS 4', 'SUPER SMASH BROS 4', 'Super Smash Bros. for Wii U'],
    ['PM', 'PROJECT MELEE', 'SUPER SMASH BROS PROJECT M', 'SUPER SMASH BROS PM', 'Project M']
]
for g in games:
    if game in g:
        game = g[-1]

if smasher == '':
    smasher = '_'.join(i[0].upper() + i[1:] for i in input('Smasher: ').split(' '))
page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
soup = bsoup(page.content, "html.parser")
while 'There is currently no text in this page.' in soup.text:
    print('Invalid tag. Try again.')
    smasher = '_'.join(i[0].upper() + i[1:] for i in input('Smasher: ').split(' '))
    page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
    soup = bsoup(page.content, "html.parser")

tables = soup.find_all('div', {'id': 'mw-content-text'})[0].contents[2].contents[1].contents[1]
for h in tables.find_all('h3'):
    if game in h.contents[0].text:
        tables = tables.contents[tables.index(h) + 2]
results = []
year = str(year)
if year.upper() == 'ALL':
    year = tables.contents[3].contents[3].text.split(', ')[1]

for i in range(3, len(tables.contents), 2):
    t = tables.contents[i]
    
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
    
