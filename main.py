import unittest
import coverage
import faktöriyel
import test_faktöriyel

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_faktöriyel.TestRekursifFaktoriyel)
    unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    cov = coverage.Coverage()

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(faktöriyel.a))

    result = unittest.TestResult()
    suite.run(result)

    print("Test Başarılı" if result.wasSuccessful() else "Test Başarısız")

    cov.start()
    run_tests()
    cov.stop()
    cov.xml_report()
    cov.report()


