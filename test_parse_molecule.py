import unittest
from parse_molecule import parse_molecule

#to push the test further we can use a seed for a random to make a test
class TestParseMolecule(unittest.TestCase):
    def test_simple(self):
        water = 'H2O'
        magnesium_hydroxide = 'Mg(OH)2'
        fremy_salt = 'K4[ON(SO3)2]2'
        emerald = 'Al2Be3(Si6O18)'
        multiple_atome = 'HH[H2H]'
        complex_multiple_atome = 'H2H[H2H]3'

        self.assertEqual(parse_molecule(water),{'H': 2, 'O': 1})
        self.assertEqual(parse_molecule(magnesium_hydroxide),{'Mg': 1, 'H': 2, 'O': 2})
        self.assertEqual(parse_molecule(fremy_salt),{'K': 4, 'O': 14, 'N': 2, 'S': 4})
        self.assertEqual(parse_molecule(multiple_atome),{'H':5})
        self.assertEqual(parse_molecule(complex_multiple_atome),{'H':12})

    def test_bracket(self):
        round_bracket = '(He)'
        curly_bracket = '{U}'
        square_bracket = '[K]'
        all_kind_bracket = '(H{H[H]})'
        multiple_same_bracket = '({H}{H})'
        multiple_same_nested_bracket = '{H{H{H}}}'
        bad_overlapping_bracket = '({H)2}2'

        self.assertEqual(parse_molecule(round_bracket),{'He':1})
        self.assertEqual(parse_molecule(curly_bracket),{'U':1})
        self.assertEqual(parse_molecule(square_bracket),{'K':1})
        self.assertEqual(parse_molecule(all_kind_bracket),{'H':3})
        self.assertEqual(parse_molecule(multiple_same_bracket),{'H':2})
        self.assertEqual(parse_molecule(multiple_same_nested_bracket),{'H':3})

        with self.assertRaises(Exception):
            parse_molecule(bad_overlapping_Bracket)
 
    def test_empty_string(self):
        self.assertEqual(parse_molecule(""),{})

    def test_not_molecule(self):
        word_string = 'azerty'
        not_title_atome = 'h2O'
        space_in_string = 'H2 O'
        quantifier_without_atome = '2H2O'
        with self.assertRaises(Exception):
            parse_molecule(word_string)
        with self.assertRaises(Exception):
            parse_molecule(not_title_atome)
        with self.assertRaises(Exception):
            parse_molecule(space_in_string)
        with self.assertRaises(Exception):
            parse_molecule(quantifier_without_atome)



if __name__ == '__main__':
    unittest.main(verbosity=2)
