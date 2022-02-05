import ply.yacc as yacc
import ply.lex as lex
from ctrl_tree_drawing import *
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

tokens = (
   'ENDL',
   'NUMBER',
   'TYPEDEF',
   # 'PRIMITIVE',
   'CURRY',
   'ADD',
   'SUB',
   'MUL',
   'DIV',
   'LPAREN',
   'RPAREN',
   'ASSIGNMENT',
   'WORD',
   'SPACE',
   'TAB',
)

# Regular expression rules for simple tokens
t_ENDL = r'\n'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NUMBER = r'\d+'
t_ASSIGNMENT = r':\='
t_TYPEDEF = r'::'
t_CURRY = r"->"
# t_PRIMITIVE = r"double|int"
t_TAB = r'\t'
t_SPACE = r'\s'
t_WORD = r'\w+'
t_ignore = ""

# https://www.dabeaz.com/ply/ply.html#ply_nn23


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

module = []

def p_function(p):
    'function : function_declaration block ENDL'
    p[0] = TreeNode("ƒ", [p[1]] + p[2])


def p_function_declaration(p):
    'function_declaration : identifier arguments TYPEDEF type_expression ENDL'
    p[0] = TreeNode("::", [p[1], TreeNode(",", p[2]), p[4]])


def p_arguments_arguments(p):
    'arguments : arguments arguments'
    print("args_args:", str([a.text for a in p[1]]) + " " + str([a.text for a in p[2]]), sep='\t')
    p[0] = p[1] + p[2]


def p_arguments(p):
    'arguments : SPACE identifier'
    print("argument:", p[2].text, sep='\t')
    p[0] = [p[2]]


def p_block_block_block(p):
    'block : block block'
    print("block_bloc:", str([a.text for a in p[1]]) + " " + str([a.text for a in p[2]]), sep='\t')
    p[0] = p[1] + p[2]


def p_block_statement(p):
    'block : TAB statement ENDL'
    print("block_stmt:", p[2].text, sep='\t')
    p[0] = [p[2]]


def p_statement_assign(p):
    'statement : identifier ASSIGNMENT expression'
    print("stmt_ass:", p[1].text + " " + p[3].text, sep='\t')
    p[0] = TreeNode(":=", [p[1], p[3]])


def p_statement_expr(p):
    'statement : expression'
    print("expr_ret:", p[1].text, sep='\t')
    p[0] = TreeNode("ret", [p[1]])


def p_type_expression_curry(p):
    'type_expression : type_expression CURRY type_expression'
    print("type_curry:", p[1].text + " " + p[3].text, sep='\t')
    p[0] = TreeNode("->", [p[1], p[3]])


def p_type_expression_group(p):
    "type_expression : LPAREN type_expression RPAREN"
    print("type_group:", p[1].text, sep='\t')
    p[0] = p[2]


def p_type_expression_identifier(p):
    "type_expression : identifier"
    print("type_ident:", p[1].text, sep='\t')
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression'''
    if p[2] == '+':
        p[0] = TreeNode("+", [p[1], p[3]])
        print("expr_add:", p[1].text + " " + p[3].text, sep='\t')
    elif p[2] == '-':
        p[0] = TreeNode("-", [p[1], p[3]])
        print("expr_sub:", p[1].text + " " + p[3].text, sep='\t')
    elif p[2] == '*':
        p[0] = TreeNode("*", [p[1], p[3]])
        print("expr_mult:", p[1].text + " " + p[3].text, sep='\t')
    elif p[2] == '/':
        p[0] = TreeNode("//", [p[1], p[3]])
        print("expr_div:", p[1].text + " " + p[3].text, sep='\t')


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    print("expr_group:", p[2].text, sep='\t')
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    print("expr_num:", p[1], sep='\t')
    p[0] = TreeNode(p[1], [])


def p_expression_identifier(p):
    "expression : identifier"
    print("expr_ident:", p[1].text, sep='\t')
    p[0] = p[1]


def p_identifier(p):
    "identifier : WORD"
    print("identifier:", p[1], sep='\t')
    p[0] = TreeNode(p[1], [])


def p_error(p):
    if p:
        print()
        print(p)
        print("Syntax error at '%s'\n" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

# while True:
#     total_input = ""
#     user_input = input(">>>")
#     while user_input != "":
#         total_input += user_input + "\n"
#         user_input = input("...")
#     print(total_input)
#     yacc.parse(total_input)

test_input = "foo n m::int->int\n" \
             "\ta:=n+1+2\n" \
             "\tb:=(3+4)*5\n" \
             "\t6*7\n\n" \
             "bar i j k::double->double\n" \
             "\tc:=i+8+9\n" \
             "\td:=(10+11)*12\n" \
             "\t13*14\n\n"
print("input:", test_input, sep="\n")
x = yacc.parse(test_input)
print(TreeDrawing(x))
