import unittest
import make_database #make a random database to test
from pokedex import PokeDex

class TestPokeDex(unittest.TestCase):

    def setUp(self):
        '''
        test1.csv is a database with different field order than test0.csv
        random capital cases and a three evolutions for Lapronyte
        '''   
        self.mixed_case = PokeDex('tests\\test1.csv')
        self.capital_case = PokeDex('tests\\test0.csv')
        self.random_case = PokeDex('tests\\random_database.csv')

    
    def test_findID(self):

        # id should be found independent of string case
        result = self.mixed_case.findID('Banub')
        real = self.capital_case.findID('Banub')
        self.assertEqual(result, real)

        # in mixed_case it is ocTonYte
        result = self.mixed_case.findID('Octonyte')
        real = self.capital_case.findID('Octonyte')
        self.assertEqual(result, real)

        # False if pokemon is not in registry
        result = self.mixed_case.findID('imaginary')
        self.assertFalse(result)

    def test_attributes(self):
        # print the attributes of every Pokemon to catch errors 

        for key, pokemon in self.mixed_case.registry.items():
            result = self.mixed_case.attributes(pokemon['Name'])
            self.assertTrue(result)


    # findEvolution is the most problematic function try to catch errors in random case
    def test_findEvolutions(self):
        for key, pokemon in self.random_case.registry.items():
            result = self.random_case.attributes(pokemon['Name'])
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
