from rply import Token
from util.tree_drawing import *
from ctrl_lang_types import Curry, DoubleType, IntegerType
from util.compile_error import CompileException


def print_tokens(tokens):
    print("|", end=" ")
    for token in tokens:
        if type(token) is Token:
            tok_str = token.getstr()
            if tok_str == "\n":
                tok_str = "\\n"
            if tok_str == "\t" or tok_str == "    ":
                tok_str = "\\t"
            print(tok_str, "|", end=" ")
        else:
            print(type(token), "|", end=" ")
    print()


def split(tokens, token_type):
    indices = find_all(tokens, token_type)
    left_indices = [0] + [i + 1 for i in indices]
    right_indices = indices + [len(tokens)]
    ret = []
    for i in range(len(left_indices)):
        ret.append(tokens[left_indices[i]: right_indices[i]])
    return ret


def find_all(tokens, token_type):
    ret = []
    for i in range(len(tokens)):
        token = tokens[i]
        if type(token) is Token:
            if token.gettokentype() == token_type:
                ret.append(i)
    return ret


def lfind(tokens, token_type):
    index = 0
    for token in tokens:
        if type(token) is Token:
            if token.gettokentype() == token_type:
                return index
        index += 1
    return -1


def rfind(tokens, token_type):
    index = len(tokens) - 1
    for token in tokens[::-1]:
        if type(token) is Token:
            if token.gettokentype() == token_type:
                return index
        index -= 1
    return -1


def get_enclosed_expression(tokens, start_token, end_token):
    openings = 1
    ret = []
    for token in tokens:
        if token.gettokentype() == start_token:
            openings += 1
        elif token.gettokentype() == end_token:
            openings -= 1
            if openings == 0:
                if not ret:
                    raise CompileException("Empty parenthesis",
                                           tokens[0].getsourcepos().lineno,
                                           tokens[0].getsourcepos().colno,
                                           len(tokens[0].getstr()))
                return ret
        ret.append(token)
    raise CompileException("Cannot resolve parenthesis",
                           tokens[0].getsourcepos().lineno,
                           tokens[0].getsourcepos().colno,
                           len(tokens[0].getstr()))


def preprocess_spaces(tokens):
    ret = [token for token in tokens if token.gettokentype() != "SPACE"]
    return ret


def preprocess_comments(tokens):
    lp = lfind(tokens, "OPEN_COMMENT")
    while lp != -1:
        rp = lfind(tokens, "CLOSE_COMMENT")
        tokens = tokens[:lp] + tokens[rp + 1:]
        lp = lfind(tokens, "OPEN_COMMENT")
    return tokens


def preprocess_literals_expr(tokens):
    def preprocess_arrays(array_tokens):
        lp = lfind(array_tokens, "OPEN_ARRAY")
        while lp != -1:
            enclosed = get_enclosed_expression(array_tokens[lp + 1:], "OPEN_ARRAY", "CLOSE_ARRAY")
            args = split(enclosed, "COMMA")
            if args == [[]]:
                vector = ArrayEmptyLiteral()
            else:
                vector = ArrayLiteral([build_expression(preprocess_literals_expr(expr)) for expr in args])
            array_tokens = array_tokens[:lp] + [vector] + array_tokens[lp + len(enclosed) + 1:][1:]
            lp = lfind(array_tokens, "OPEN_ARRAY")
        return array_tokens

    tokens = preprocess_arrays(tokens)
    return tokens


def preprocess_literals_type(tokens):
    def preprocess_arrays(array_tokens):
        lp = lfind(array_tokens, "OPEN_ARRAY")
        while lp != -1:
            enclosed = get_enclosed_expression(array_tokens[lp + 1:], "OPEN_ARRAY", "CLOSE_ARRAY")
            vector = ArrayType(build_type_expression(preprocess_literals_type(enclosed)), 1)
            array_tokens = array_tokens[:lp] + [vector] + array_tokens[lp + len(enclosed) + 1:][1:]
            lp = lfind(array_tokens, "OPEN_ARRAY")
        return array_tokens

    tokens = preprocess_arrays(tokens)
    return tokens


def get_indent(line):
    line_iter = iter(line)
    tabs = 0
    spaces = 0
    n = next(line_iter).gettokentype()
    while n == "TAB" or n == "SPACE":
        if n == "TAB":
            tabs += 1
        else:
            spaces += 1
        n = next(line_iter).gettokentype()
    return tabs + (spaces // 4)


def get_function_arg_count(name, functions):
    for function in functions:
        if function.name == name:
            return len(function.arg_list)
    return -1


def build_type_expression(tokens):
    if len(tokens) == 1:
        token = tokens[0]
        if type(token) is Token:
            if token.getstr() == "double":
                return DoubleType()
            elif token.getstr() == "int":
                return IntegerType()
            else:
                raise CompileException("Unknown type: " + token.getstr(),
                                       token.getsourcepos().lineno,
                                       token.getsourcepos().colno,
                                       len(token.getstr()))
        else:
            return token

    lp = lfind(tokens, "OPEN_PAREN")
    if lp != -1:
        enclosed = get_enclosed_expression(tokens[lp + 1:], "OPEN_PAREN", "CLOSE_PAREN")
        if not enclosed:
            raise Exception()
        tokens = tokens[:lp] + [build_type_expression(enclosed)] + tokens[lp + len(enclosed) + 2:]
    elif rfind(tokens, "CLOSE_PAREN") != -1:
        raise Exception()

    operator_index = lfind(tokens, "RIGHT_ARROW")
    if operator_index != -1:
        left = build_type_expression(tokens[:operator_index])
        right = build_type_expression(tokens[operator_index + 1:])
        return Curry(right, left)
    else:
        # as len > 1 but no right arrow, that means you have something similar to  ... double double ...
        raise Exception()


def build_expression(tokens):
    if len(tokens) == 0:
        raise Exception("No tokens to build expression")

    lp = lfind(tokens, "OPEN_PAREN")
    rp = rfind(tokens, "CLOSE_PAREN")
    if lp != -1 and rp != -1 and lp + 1 < len(tokens) - 1:
        enclosed = get_enclosed_expression(tokens[lp + 1:], "OPEN_PAREN", "CLOSE_PAREN")

        if not enclosed:
            raise CompileException("Empty parenthesis",
                                   tokens[lp].getsourcepos().lineno,
                                   tokens[lp].getsourcepos().colno,
                                   2)

        prefix = tokens[:lp]
        body = [build_expression(enclosed)]
        postfix = tokens[lp + len(enclosed) + 2:]

        tokens = prefix + body + postfix
    elif lp == -1 and rp != -1:
        raise CompileException("No opening parenthesis",
                               tokens[rp].getsourcepos().lineno,
                               tokens[rp].getsourcepos().colno,
                               len(tokens[rp].getstr()))
    elif lp != -1 and rp == -1:
        raise CompileException("No closing parenthesis",
                               tokens[lp].getsourcepos().lineno,
                               tokens[lp].getsourcepos().colno,
                               len(tokens[lp].getstr()))

    if len(tokens) == 1:
        token = tokens[0]
        if type(token) is Token:
            if token.getstr() == "double":
                return DoubleType()
            elif token.getstr() == "int":
                return IntegerType()
            elif token.gettokentype() == "DOUBLE":
                return DoubleLiteral(token.getstr())
            elif token.gettokentype() == "FLOAT":
                return FloatLiteral(token.getstr())
            elif token.gettokentype() == "INTEGER":
                return IntLiteral(token.getstr())
            elif token.gettokentype() == "UNDER":
                return WildcardLiteral()
            elif token.gettokentype() == "REST":
                return RestIdentifier(token.getstr())
            elif token.gettokentype() == "WORD":
                return Identifier(token.getstr())
            else:
                raise CompileException("Unexpected token",
                                       token.getsourcepos().lineno,
                                       token.getsourcepos().colno,
                                       len(token.getstr()))
        elif type(token) is DoubleType \
                or type(token) is IntegerType \
                or type(token) is DoubleLiteral \
                or type(token) is FloatLiteral \
                or type(token) is IntLiteral \
                or type(token) is WildcardLiteral \
                or type(token) is RestIdentifier \
                or type(token) is Identifier \
                or type(token) is BinaryOperator:
            return token
        else:
            raise Exception("'%s' type found where token or literal expected" % type(token))

    binops = [('SUB', '-'), ('ADD', '+'), ('MUL', '*'), ('DIV', '/'), ('PIPE', '->')]
    for pair in binops:
        binop_text = pair[0]
        operator_symbol = pair[1]
        operator_index = lfind(tokens, binop_text)
        if operator_index != -1:
            if 0 < operator_index < len(tokens) - 1:
                left = build_expression(tokens[:operator_index])
                right = build_expression(tokens[operator_index + 1:])
                return BinaryOperator(left, right, operator_symbol)
            else:
                raise CompileException("Operation %s missing operands" % operator_symbol,
                                       tokens[operator_index].getsourcepos().lineno,
                                       tokens[operator_index].getsourcepos().colno,
                                       len(tokens[operator_index].getstr()))

    return BinaryOperator(build_expression(tokens[:-1]),
                          build_expression([tokens[-1]]), "->")


def build_assignment(tokens):
    assignment_operator = lfind(tokens, "ASSIGNMENT")
    return BinaryOperator(Identifier(tokens[0].getstr()), build_expression(tokens[assignment_operator + 1:]), "=")


def build_pattern_match(tokens):
    right_arrow_operator = lfind(tokens, "THICK_RIGHT_ARROW")
    vert_operator = lfind(tokens, "VERT")

    if vert_operator != 0:
        raise CompileException("Tokens before case unexpected",
                               tokens[vert_operator].getsourcepos().lineno,
                               0,
                               vert_operator)

    if vert_operator + 1 >= right_arrow_operator:
        raise CompileException("No pattern to match",
                               tokens[vert_operator].getsourcepos().lineno,
                               tokens[vert_operator].getsourcepos().colno,
                               len(tokens[vert_operator].getstr()))

    if right_arrow_operator >= len(tokens) - 2:
        raise CompileException("No pattern expression",
                               tokens[right_arrow_operator].getsourcepos().lineno,
                               tokens[right_arrow_operator].getsourcepos().colno,
                               len(tokens[right_arrow_operator].getstr()))

    pattern = build_expression(tokens[vert_operator + 1:right_arrow_operator])
    block = build_expression(tokens[right_arrow_operator + 1:])
    case = Case(pattern, block)
    if vert_operator > 0:
        control_variable = build_expression(tokens[:vert_operator])
        return Match(control_variable, [case])
    else:
        return case


def build_statement(tokens):
    contains = lambda x: x != -1

    tokens = preprocess_literals_expr(tokens)

    assignment_operator = lfind(tokens, "ASSIGNMENT")
    right_arrow_operator = lfind(tokens, "THICK_RIGHT_ARROW")
    vert_operator = lfind(tokens, "VERT")

    print(assignment_operator, right_arrow_operator, vert_operator)

    if contains(assignment_operator) and not contains(right_arrow_operator):
        return build_assignment(tokens)

    if contains(right_arrow_operator) and contains(
            vert_operator) and vert_operator < right_arrow_operator and not contains(assignment_operator):
        return build_pattern_match(tokens)

    return build_expression(tokens)


class Match:
    def __init__(self, control_variable, cases):
        self.control_variable = control_variable
        self.cases = cases

    def to_tree(self):
        return TreeNode("?", [self.control_variable.to_tree()] + [case.to_tree() for case in self.cases])


class Case:
    def __init__(self, pattern, block):
        self.pattern = pattern
        self.block = block

    def to_tree(self):
        return TreeNode("|", [self.pattern.to_tree(), self.block.to_tree()])


class ArrayLiteral:
    def __init__(self, entries):
        self.entries = entries

    def to_tree(self):
        return TreeNode("[]", [entry.to_tree() for entry in self.entries])


class WildcardLiteral:
    def __init__(self):
        pass

    def to_tree(self):
        return TreeNode("_", [])


class ArrayEmptyLiteral:
    def __init__(self):
        pass

    def to_tree(self):
        return TreeNode("[]", [])


class ArrayHeadTailLiteral:
    def __init__(self):
        pass

    def to_tree(self):
        return TreeNode("[x,...xs]", [])


class NumberLiteral:
    def __init__(self, value):
        self.value = value

    def to_tree(self):
        return TreeNode(self.value, [])


class DoubleLiteral(NumberLiteral):
    pass


class FloatLiteral(NumberLiteral):
    pass


class IntLiteral(NumberLiteral):
    pass


class BinaryOperator:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

    def to_tree(self):
        return TreeNode("(" + self.operator + ")", [self.left.to_tree(), self.right.to_tree()])


class Identifier:
    def __init__(self, name):
        self.name = name

    def to_tree(self):
        return TreeNode("`" + self.name + "`", [])


class RestIdentifier:
    def __init__(self, name):
        self.name = name.replace("...", "")

    def to_tree(self):
        return TreeNode("`" + self.name + "`", [])


class Function:
    def __init__(self, name, arg_list, type_expression):
        self.name = name
        self.arg_list = arg_list
        self.type_expression = type_expression
        self.block = []

    def add_block(self, block):
        self.block = block

    def to_tree(self):
        type_expr_node = TreeNode("(:)", [self.type_expression.to_tree()])
        child_nodes = [statement.to_tree() for statement in self.block]
        return TreeNode(self.name, [type_expr_node] + child_nodes)

    def is_definition(self):
        return self.block


class ModuleParseTree:
    def __init__(self):
        self.children = []

    def __str__(self):
        return "\nPARSE TREE\n\n" + str(
            TreeDrawing(TreeNode("module", [child.to_tree() for child in self.children]))) + "\n\n"


class Parser:
    def __init__(self):
        pass
        # tree = TreeNode("Alpha", [TreeNode("Beta",  [TreeNode("Epsilon", []),
        #                                              TreeNode("Zeta",    []),
        #                                              TreeNode("Eta",     []),
        #                                              TreeNode("Theta",   [TreeNode("Mu", []),
        #                                                                   TreeNode("Nu", [])])]),
        #                           TreeNode("Gamma", [TreeNode("Xi",      [TreeNode("Omicron", [])])]),
        #                           TreeNode("Delta", [TreeNode("Iota",    []),
        #                                              TreeNode("Kappa",   []),
        #                                              TreeNode("Lambda",  [])])])
        # drawing = TreeDrawing(tree)
        # self.module = "; ModuleID = \"%s\"\n" % __file__
        # self.module += "target triple = \"%s\"\n" % binding.targets.get_default_triple()
        # self.module += "target datalayout = \"%s\"\n\n" % ""

    def parse(self, tokens):
        tokens = preprocess_comments(tokens)
        lines = split(tokens, "ENDL")
        while [] in lines:
            lines.remove([])

        mod = ModuleParseTree()

        current_function = None

        open_match = None

        for line in lines:
            indent = get_indent(line)
            line = preprocess_spaces(line)
            if indent == 0:
                colon = lfind(line, "TYPE_DEF")
                if colon > 1:  # is function declaration
                    name = line[0].getstr()
                    arg_names = [arg.getstr() for arg in line[1:colon]]
                    type_expression = build_type_expression(preprocess_literals_type(line[colon + 1:]))
                    current_function = Function(name, arg_names, type_expression)
                    mod.children.append(current_function)
                elif colon == 1:  # is type declaration
                    pass
            else:
                statement = build_statement(line)

                if type(statement) is Match:
                    current_function.block.append(statement)
                    open_match = statement
                elif type(statement) is Case:
                    open_match.cases.append(statement)
                else:
                    current_function.block.append(statement)
                    open_match = None
        return mod

    # def save(self, filename):
    #     with open(filename, 'w', encoding="utf-8") as output_file:
    #         output_file.write(self.module)
