# PokeDex!
This script is prints an `attribute` for a given PokeMon. The PokeDex is created from a `database.csv` file. Once an instance of a PokeDex is established methods can then be applied to it. This program has a **cli** syntax,
```
$ python pokedex.py <database file> <Pokemon Name>
```
The `database file` must be a `.csv` for the program to work. To keep things as they were in the code exam as well I have included a copy file named `solution.py` that runs with the same command line interface syntax. An example use would be
```
$ python pokedex.py database.py Banub
ID:
    004
Strong against:
    Octopeat
    Octoplat
    Octonyte
    Bibyss
Weak against:
    None
Evolution:
    Banub > Banubeleon > Banubizard
```

## Class Methods
Our main methods is `PokeDex.attribute(<Pokemon Name>)` this prints out all the relevant information for a PokeMon with the given input name. This class allows one to import pokedex into a python REPL and play around and experiment
```
>>> from pokedex import PokeDex
>>> mypokemon = PokeDex('database.csv')
>>> print(mypokemon)
>>>PokeDex(database.csv)
****************
Name:
    Banub
ID:
    004
Types:
    Fire
Weaknesses:
    Ground
    Rock
    Water
Evolution:
    005
----------------
...
```
The class has an implemented `__str__` method which prints all the fields of a given database in a formatted string format.


## Running Tests
You can run test directly from the command line with 
```
$ python test_pokedex.py
```
We have implemented some unittests in the script `test_pokedex.py`. This script tests for mixed ordering of `ID, Name, Types, Weaknesses, Evolutions` and random capital letters in fields. The final test creates a random database using the script `make_database.csv` and then determines the attributes of every pokemon in the pokedex. This test was developed in an attempt to discover breakage in the program. 