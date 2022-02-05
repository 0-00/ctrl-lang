from rply import LexerGenerator
from rply import ParserGenerator
from ctrl_tree_drawing import *

accepted_tokens = {
    'ENDL': r'\n+',
    'NUMBER': r'\d+',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MUL': r'\*',
    'DIV': r'/',
    'OPEN_PARENS': r'\(',
    'CLOSE_PARENS': r'\)',
    'ASSIGNMENT': r':\=',
    'WORD': r'\w+'
}

lg = LexerGenerator()
for key, entry in accepted_tokens.items():
    lg.add(key, entry)

# lg.ignore(r'\s+')
lexer = lg.build()

pg = ParserGenerator(accepted_tokens.keys(), precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ])


@pg.production('block : statement ENDL')
def block(p):
    return TreeNode("</>", [p[0]])


@pg.production('statement : identifier ASSIGNMENT expression')
def statement(p):
    return TreeNode(":=", [p[0], p[2]])


# @pg.production('statement : expression')
# def statement(p):
#     # return TreeNode("return", [p[0]])
#     return p[0]


@pg.production('identifier : WORD')
def expression_word(p):
    return TreeNode(p[0].getstr(), [])


@pg.production('expression : NUMBER')
def expression_number(p):
    return TreeNode(p[0].getstr(), [])


@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(p):
    return p[1]


@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return TreeNode("+", [left, right])
    elif p[1].gettokentype() == 'MINUS':
        return TreeNode("-", [left, right])
    elif p[1].gettokentype() == 'MUL':
        return TreeNode("*", [left, right])
    elif p[1].gettokentype() == 'DIV':
        return TreeNode("\\", [left, right])
    else:
        raise AssertionError('Oops, this should not be possible!')


parser = pg.build()

while True:
    expression = ""
    user_input = input(">>>")
    while user_input != "":
        expression += user_input + "\n"
        user_input = input("...")
    print(expression)
    root = parser.parse(lexer.lex(expression))
    print(TreeDrawing(root))
