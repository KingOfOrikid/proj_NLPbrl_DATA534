import unittest
from test_NLPbrl import TestProj

test_cases = (TestProj)

def test_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestProj))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
test_suite()