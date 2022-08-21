from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
        self.rules = []
        self._add_tokens()

    def token_name_list(self):
        return list(zip(*self.rules))[0]

    def _add_tokens(self):
        self.rules.append(("TAB", r"\t"))
        self.rules.append(("ENDL", r"\n"))

        self.rules.append(("REST", r"\.\.\.\w+"))
        self.rules.append(("ELLIPSES", r"\.\.\."))

        self.rules.append(("ASSIGNMENT", r":\="))

        self.rules.append(('OPEN_PAREN', r'\('))
        self.rules.append(('CLOSE_PAREN', r'\)'))

        self.rules.append(('OPEN_BLOCK', r'\{'))
        self.rules.append(('CLOSE_BLOCK', r'\}'))

        self.rules.append(('OPEN_ARRAY', r'\['))
        self.rules.append(('CLOSE_ARRAY', r'\]'))

        self.rules.append(('GRAVE', r'`'))

        self.rules.append(('OPEN_VEC', r'\<'))
        self.rules.append(('CLOSE_VEC', r'\>'))

        self.rules.append(('OPEN_COMMENT', r'\/\*'))
        self.rules.append(('CLOSE_COMMENT', r'\*\/'))

        self.rules.append(('TYPE_DEF', r'::'))
        self.rules.append(('COLON', r':'))

        self.rules.append(('PIPE', r'\|\>'))
        self.rules.append(('RIGHT_ARROW', r'->'))
        self.rules.append(('THICK_RIGHT_ARROW', r'=>'))

        self.rules.append(('VERT', r'\|'))
        self.rules.append(('AND', r'\&'))
        self.rules.append(('UNDER', r'\_'))

        self.rules.append(('COMMA', r'\,'))

        self.rules.append(('ADD', r'\+'))
        self.rules.append(('SUB', r'\-'))
        self.rules.append(('MUL', r'\*'))
        self.rules.append(('DIV', r'\\'))
        self.rules.append(('DOT', r'·'))    # alt 250
        self.rules.append(('TIMES', r'×'))  # alt 0215

        self.rules.append(('DOUBLE', r'\d+\.\d*D'))
        self.rules.append(('FLOAT', r'\d+\.\d*'))
        self.rules.append(('INTEGER', r'\d+'))

        self.rules.append(('WORD', r'\w+'))

        self.rules.append(("SPACE", r" "))

        for pair in self.rules:
            self.lexer.add(pair[0], pair[1])

    def build_lexer(self):
        return self.lexer.build()
