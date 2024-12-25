import unittest
from faktöriyel import FaktoriyelCalculator


class TestRekursifFaktoriyel(unittest.TestCase):
    def test_rekursif_faktoriyel_5(self):
        calculator = FaktoriyelCalculator()
        self.assertEqual(calculator.rekursif(5), 120)
        self.assertEqual(calculator.basic(5), 120)

    def test_rekursif_faktoriyel_0_and_1(self):
        calculator = FaktoriyelCalculator()
        self.assertEqual(calculator.rekursif(0), 1)
        self.assertEqual(calculator.rekursif(1), 1)
        self.assertEqual(calculator.basic(0), 1)
        self.assertEqual(calculator.basic(1), 1)

    def test_negative_values(self):
        calculator = FaktoriyelCalculator()
        with self.assertRaises(ValueError):
            calculator.rekursif(-5)
        with self.assertRaises(ValueError):
            calculator.basic(-5)

    def test_large_values(self):
        calculator = FaktoriyelCalculator()
        self.assertEqual(calculator.rekursif(10), 3628800)
        self.assertEqual(calculator.basic(10), 3628800)

if __name__ == "__main__":
    unittest.main()