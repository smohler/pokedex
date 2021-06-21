# make an example data set to test solution.py
import random
import io
import csv
import requests
import pandas as pd

# make list of id tags with zero padding
ids = [str(n).zfill(3) for n in range(1, 51)]

# make random node connections
evolutions = {}
for id in ids:
    k = random.choice(range(2))
    if k == 0:
        evolutions[id] = None
    else: #k>0
        sample = random.sample(ids, k)
        if id in sample:
            sample.remove(id)
        evolutions[id] = ','.join(sample)

# import 50 Pokemon Names from a github csv file
url = 'https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv'
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))
names = df.identifier.tolist()[:50]
#capitalize first letter
names = map(lambda x: x.capitalize(), names)



Types = {'Fire','Flying','Ice','Psychic', 'Poison', 'Rock', 'Ground', 'Thunder', 'Fear'}
Columns = [['Id', 'Name', 'Evolution', 'Types', 'Weaknesses'], ['iD', 'name', 'eVoluTion', 'tYpes', 'WeaKneSSes']]

#make test-database.csv file
import csv
with open('tests\\random_database.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',')
    random.shuffle(random.choice(Columns))
    
    #pick case sensitive columns labeling
    case = random.choice(Columns)
    Columns = list(map(lambda x: x.lower(), case))
    datawriter.writerow(case)

    #find column positions
    Id_idx = Columns.index('id')
    Name_idx = Columns.index('name')
    Evolution_idx = Columns.index('evolution')
    Weaknesses_idx = Columns.index('weaknesses')
    Types_idx = Columns.index('types')

    #write each row matching to the column position
    for name, id, evo in zip(names, evolutions.keys(), evolutions.values()):
        #define row
        row = ['0', '1', '2', '3', '4']
        

        # pick weaknesses and strength (can't be weak and strong against the same type)
        n = lambda x,y: random.choice(range(x,y))
        weak = random.sample(Types, n(0,4))
        strong = Types.difference(weak)

        #assign to row
        row[Id_idx]= id
        row[Name_idx]= name
        row[Evolution_idx]= evo
        row[Weaknesses_idx]= ','.join(weak)
        row[Types_idx] = ','.join(random.sample(strong, n(1,5)))

        #write row
        datawriter.writerow(row)