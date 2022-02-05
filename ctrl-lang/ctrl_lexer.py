from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add("TAB", r"\t|(    )")
        self.lexer.add("ENDL", r"\n")

        self.lexer.add("ELLIPSES", r"\.\.\.")

        self.lexer.add("ASSIGNMENT", r":\=")

        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        self.lexer.add('OPEN_BLOCK', r'\{')
        self.lexer.add('CLOSE_BLOCK', r'\}')

        self.lexer.add('OPEN_ARRAY', r'\[')
        self.lexer.add('CLOSE_ARRAY', r'\]')

        self.lexer.add('GRAVE', r'`')

        self.lexer.add('OPEN_VEC', r'\<')
        self.lexer.add('CLOSE_VEC', r'\>')

        self.lexer.add('OPEN_COMMENT', r'\/\*')
        self.lexer.add('CLOSE_COMMENT', r'\*\/')

        self.lexer.add('TYPE_DEF', r'::')
        self.lexer.add('COLON', r':')

        self.lexer.add('PIPE', r'\|\>')
        self.lexer.add('RIGHT_ARROW', r'->')
        self.lexer.add('THICK_RIGHT_ARROW', r'=>')

        self.lexer.add('VERT', r'\|')
        self.lexer.add('AND', r'\&')
        self.lexer.add('UNDER', r'\_')

        self.lexer.add('COMMA', r'\,')

        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\\')
        self.lexer.add('DOT', r'·')    # alt 250
        self.lexer.add('TIMES', r'×')  # alt 0215

        self.lexer.add('DOUBLE', r'\d+\.\d*D')
        self.lexer.add('FLOAT', r'\d+\.\d*')
        self.lexer.add('INTEGER', r'\d+')

        self.lexer.add('WORD', r'\w+')

        self.lexer.add("SPACE", r" ")

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
