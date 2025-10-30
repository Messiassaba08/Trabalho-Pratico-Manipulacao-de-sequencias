import unittest
from src.ri.query_parser import parse_query, extract_terms, Term, And, Or


class TestQueryParser(unittest.TestCase):

    def test_simple_query_ast(self):
        ast = parse_query("economy")
        self.assertIsInstance(ast, Term)
        self.assertEqual(ast.term, "economy")
        self.assertEqual(extract_terms(ast), ["economy"])

    def test_and_or_precedence_with_parentheses(self):
        ast = parse_query("(economy AND politics) OR sports")
        # OR no topo
        self.assertIsInstance(ast, Or)
        self.assertIsInstance(ast.left, And)
        self.assertIsInstance(ast.right, Term)
        self.assertEqual(ast.right.term, "sports")
        self.assertEqual(extract_terms(ast), ["economy", "politics", "sports"])

    def test_and_chain(self):
        ast = parse_query("a AND b AND c")
        # Deve encadear como And(And(a,b),c)
        self.assertIsInstance(ast, And)
        self.assertIsInstance(ast.left, And)
        self.assertIsInstance(ast.right, Term)
        self.assertEqual(extract_terms(ast), ["a", "b", "c"])

    def test_empty_query_returns_none(self):
        self.assertIsNone(parse_query(""))


if __name__ == '__main__':
    unittest.main()