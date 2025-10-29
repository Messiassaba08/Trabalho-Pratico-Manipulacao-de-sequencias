import re

class Term:
    def __init__(self, term):
        self.term = term.lower()

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

TOKEN_RE = re.compile(r'\(|\)|AND|OR|[^\s()]+', re.IGNORECASE)

def tokenize(q):
    for m in TOKEN_RE.finditer(q):
        tok = m.group(0)
        if tok.upper() in ("AND", "OR"):
            yield tok.upper()
        else:
            yield tok

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        t = self.peek()
        if t is None:
            return None
        if expected and t != expected:
            raise ValueError(f"Expected {expected}, got {t}")
        self.pos += 1
        return t

    def parse(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while self.peek() == "OR":
            self.consume("OR")
            right = self.parse_and()
            node = Or(node, right)
        return node

    def parse_and(self):
        node = self.parse_factor()
        while self.peek() == "AND":
            self.consume("AND")
            right = self.parse_factor()
            node = And(node, right)
        return node

    def parse_factor(self):
        tok = self.peek()
        if tok == "(":
            self.consume("(")
            node = self.parse()
            self.consume(")")
            return node
        if tok is None:
            raise ValueError("Unexpected end of query")
        self.consume()
        return Term(tok)

def parse_query(q):
    tokens = list(tokenize(q))
    if not tokens:
        return None
    parser = Parser(tokens)
    return parser.parse()

def extract_terms(ast):
    terms = []
    if ast is None:
        return terms
    if isinstance(ast, Term):
        terms.append(ast.term.lower())
    elif isinstance(ast, And) or isinstance(ast, Or):
        terms += extract_terms(ast.left)
        terms += extract_terms(ast.right)
    return list(dict.fromkeys(terms))