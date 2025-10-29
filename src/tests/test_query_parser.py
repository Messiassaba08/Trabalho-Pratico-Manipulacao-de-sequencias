import unittest
from src.ri.query_parser import parse_query

class TestQueryParser(unittest.TestCase):

    def test_simple_query(self):
        query = "economy"
        expected_output = ["economy"]
        self.assertEqual(parse_query(query), expected_output)

    def test_and_query(self):
        query = "economy AND politics"
        expected_output = ["economy", "politics"]
        self.assertEqual(parse_query(query), expected_output)

    def test_or_query(self):
        query = "economy OR politics"
        expected_output = ["economy", "politics"]
        self.assertEqual(parse_query(query), expected_output)

    def test_complex_query(self):
        query = "(economy AND politics) OR sports"
        expected_output = ["economy", "politics", "sports"]
        self.assertEqual(parse_query(query), expected_output)

    def test_empty_query(self):
        query = ""
        expected_output = []
        self.assertEqual(parse_query(query), expected_output)

if __name__ == '__main__':
    unittest.main()