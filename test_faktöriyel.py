import unittest
from faktöriyel import a

class TestRekursifFaktoriyel(unittest.TestCase):
    # Test case 1
    def test_rekursif_faktoriyel_5(self):
        faktoriyel_calculator = a()
        result = faktoriyel_calculator.rekursif(5)
        #expected = faktoriyel_calculator.basic(5)
        self.assertEqual(result)
    # Test case 2
    def test_rekursif_faktoriyel_3(self):
        faktoriyel_calculator = a()
        result = faktoriyel_calculator.rekursif(3)
        #expected = faktoriyel_calculator.basic(3)
        self.assertEqual(result)
    #Test case 3
    def test_rekursif_faktoriyel_2(self):
        faktoriyel_calculator = a()
        result = faktoriyel_calculator.rekursif(2)
        #expected = faktoriyel_calculator.basic(2)
        self.assertEqual(result)

if __name__ == "__main__":
    unittest.main()
