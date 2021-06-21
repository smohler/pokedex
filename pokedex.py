import sys
import csv
import os
import itertools

class PokeDex:
    '''
    A PokeDex is a record of all the Pokemon a player has given
    a database.csv file. The PokeDex has methods which allow a player
    to query attributes for a given PokeMon.
    '''

    #dunder methods
    def __init__(self, database) -> None:
        # initialize with database.csv
        self.registry = self.Registry(database)
        self.lineage = self.Lineage()
        self.database = database
        pass

    def __str__(self) -> str:
        # print(PokeDex) functionality
        monsterStrings = f"{self.__repr__()}\n{'*'*16}\n"
        for id, monster in self.registry.items():
            monsterStrings += self.monsterString(id, monster)
        return monsterStrings

    def __repr__(self) -> str:
        # __repr__ should recreate the instance if eval(repr(self)) is called
        return f'PokeDex({self.database})'

    def __len__(self) -> int:
        return len(self.registry) 

    def __add__(self, other):
        # Combine self and other in a new PokeDex as a set union (no repeating IDS)

        # Get the IDS
        mine = self.registry.keys()
        theirs = other.registry.keys()

        # Find the new PokeMon and Repeats
        repeats = set(mine).intersection(set(theirs))
        new = set(mine).intersection(set(theirs))

        # Add the new PokeMon to your PokeDex

        # Add / Update a Field registry['Count'] for repeats

        pass



    # methods for dunder methods
    def monsterString(self, id, monster) -> str:
        # return a string to print for a given item in a registry
        name = monster['Name']
        types = '\n    '.join(monster['Types'])
        weaknesses = '\n    '.join(monster['Weaknesses'])
        if monster['Evolution']:
            evolution = '\n    '.join(monster['Evolution'])
        else:
            evolution = 'None'
        return f"Name:\n    {name}\nID:\n    {id}\nTypes:\n    {types}\nWeaknesses:\n    {weaknesses}\nEvolution:\n    {evolution}\n{'-'*16}\n"

    def Registry(self, filename) -> dict:
        """Import the database.csv file and define a dictionary from it"""

        #read CSV file line by line
        registry = {}
        with open(filename) as csvfile:
            line_reader = csv.reader(csvfile, delimiter=',')
            k = 0
            for line in line_reader:
                #Find index position of column names
                if k==0:
                    data = list(map(lambda x: x.lower(), line))
                    name, idx, weak, evo, types = self.findIndices(data)
                #Now read the line of the csv and assign each entry to a monster class!
                else:
                    data = list(map(lambda x: x.lower(), line))
                    Name = line[name].capitalize()
                    Id = line[idx]
                    Weaknesses = self.cleanText(line[weak])
                    Types = self.cleanText(line[types])
                    if len(line) == 4:
                        Evolution = None
                    else:
                        if line[evo] == '':
                            Evolution = None
                        else:
                            Evolution = line[evo].split(',')
                        
                    # Assign monster construction
                    registry[Id] = {'Name':Name, 'Weaknesses':Weaknesses, 'Types':Types, 'Evolution':Evolution}
                k+=1
        return registry

    def cleanText(self, data) -> list:
        ''' 
        A method to clean text data from database.csv to a standard capital case
        '''
        capital = map(lambda x: x.capitalize(), data.split(','))
        return list(capital)

    def findIndices(self, data) -> tuple:
        name = data.index('name')
        idx = data.index('id')
        weak = data.index('weaknesses')
        evo = data.index('evolution')
        types = data.index('types')
        return name, idx, weak, evo, types

    def Lineage(self) -> dict:
        '''
        A family relation graph for the PokeDex
        '''
        Relations = {}

        for ID, Monster in self.registry.items():
            if ID not in Relations and Monster['Evolution']:
                Relations[ID] = Monster['Evolution']
            else:
                Relations[ID] = [None]
        return Relations

    # method to print a Pokemon's attributes
    def attributes(self, name):
        '''
        Print a strategy for a pokemon giving its weaknesses, strengths, and evolutions
        
        '''
        #ensure capital case from user input
        ID = self.findID(name.capitalize())
        strongAgainst = '\n    '.join(self.findStrengths(name))
        weakAgainst = '\n    '.join(self.findWeakness(name))
        evolvedFrom = '\n    '.join(self.findEvolutions(name))
        print(f"ID:\n    {ID}\nStrong against:\n    {strongAgainst}\nWeak against:\n    {weakAgainst}\nEvolution:\n    {evolvedFrom}\n")
        return ID, self.findStrengths(name), self.findWeakness(name), self.findEvolutions(name)

    #class methods for attributes
    def findID(self, name):
        """
        I want to find the the ID of a monster given it's name
        """
        for key, val in self.registry.items():
            if val['Name'].lower() == name.lower():
                return key
        print(f'\n The monster "{name}" is not in the PokeDex!')
        return False

    def findStrengths(self, name):
        """
        You are strong against a monster that have your strength in THEIR weakness!
        """
        strongAgainst=[]
        ID = self.findID(name)
        TYPE = set(self.registry[ID]['Types'])

        for id, monster in self.registry.items():
            WEAK = set(monster['Weaknesses'])
            if TYPE.intersection(WEAK):
                #non empty intersection mean you're strong against it
                strongAgainst.append(monster['Name'])

        if strongAgainst:
            return strongAgainst
        else:
            return ["None"]

    def findWeakness(self, name):
        """
        You are strong against a monster that have your strength in THEIR weakness!
        """
        weakAgainst=[]
        ID = self.findID(name)
        WEAK = set(self.registry[ID]['Weaknesses'])

        for id, monster in self.registry.items():
            TYPE = set(monster['Types'])
            if WEAK.intersection(TYPE):
                #non empty intersection mean you're strong against it
                weakAgainst.append(monster['Name'])

        if weakAgainst:
            return weakAgainst
        else:
            return ['None']

    def findEvolutions(self, name):
        '''
        Return a list of string representations of a pokemons evolutions
        '''
        ID = self.findID(name)
        monsters = self.registry

        if not monsters[ID]['Evolution']:
            return ["None"]
        else:
            parents = self.search(ID)
            evolutions = self.traceback(ID, parents) 
        #return string message of evolutions
        strings = []
        for evolution in evolutions:
            evolution.reverse()
            strings.append(' > '.join(evolution))
        return strings


    # functions for findEvolutions
    def search(self, ID):
        '''
        Recursive search for all evolutions of a given monster
        identified by an ID
        '''
        #child = lambda x: search(self.registry, self.lineage, x)
        # if a monster does not decend from anyone return id
        if not self.registry[ID]['Evolution']:
            return ID
        else:
            return [self.search(neighbor) for neighbor in self.lineage[ID]]

    def flatten(self, items, seqtypes=(list, tuple)):
        '''
        Flatten an arbitrarily nested list from the output of search.
        '''
        for i, x in enumerate(items):
            while i < len(items) and isinstance(items[i], seqtypes):
                items[i:i+1] = items[i]
        return set(items)

    def traceback(self, ID, parents) -> list:
        '''
        Given all the root nodes for a given evolution, 
        make a list of all possible evolutions

        TODO: This function is probably not needed, 
        have search() return this output somehow,
        maybe a yield statement?
        '''
        evolutions = []
        monsters = self.registry
        lineage = self.lineage
        parents = self.flatten(parents)

        for parent in parents:
            evolution = [monsters[parent]['Name']]
            for key, val in lineage.items():
                if parent in val:
                    evolution.append(monsters[key]['Name'])
            evolution.append(monsters[ID]['Name'])
            evolutions.append(evolution)
        return evolutions

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='Print a Monster registry report.')
    _, database, monster = sys.argv

    myPokemon = PokeDex(database)
    myPokemon.attributes(monster)
