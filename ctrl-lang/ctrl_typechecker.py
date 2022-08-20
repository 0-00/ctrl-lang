from ctrl_ast import *
from functools import reduce


def pprint(a, indent=0):
    if type(a) is list:
        print("\t" * indent, "[", sep="")
        for element in a:
            pprint(element, indent+1)
        print("\t" * indent, "]", sep="")
    else:
        print("\t" * indent, a, sep="")


class UndirectedPair:
    def __init__(self, x, y):
        b = hash(repr(x)) > hash(repr(y))
        self.x = x if b else y
        self.y = y if b else x

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __hash__(self):
        return hash(self.x) * hash(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class TypeChecker:
    def __init__(self, ast):
        self.ast = ast

    def check(self):
        def filter_empty(a):
            return list(filter(lambda x: x is not None and x != [], a))

        def scope_traversal(node):
            if type(node) is AST:
                ret = []
                for child in node.children:
                    ret.append(scope_traversal(child))
                return ret
            elif type(node) is FunctionDefinitionAST:
                return [node, node.arg_list
                        + scope_traversal(list(filter(lambda x: type(x) is not PatternMatchAST, node.block)))
                        + sum(scope_traversal(list(filter(lambda x: type(x) is PatternMatchAST, node.block))), [])
                        ]
            elif type(node) is PatternMatchAST:
                return filter_empty([scope_traversal(block) for block in node.blocks])
            elif type(node) is list:
                return filter_empty(map(scope_traversal, node))
            elif type(node) is AssignmentAST:
                return node.left

        # print("SCOPES")
        scopes = scope_traversal(self.ast)
        # print(scopes)

        def flatten(a):
            if type(a) is list:
                return sum([flatten(element) for element in a], [])
            return [a]

        # print(flatten(scopes))

        type_dependency_pairs = set()

        def type_dependency_traversal(node, assigned_variable=None, current_function=None):
            if type(node) is AST:
                for child in node.children:
                    type_dependency_traversal(child)
            elif type(node) is FunctionDefinitionAST:
                for statement in node.block:
                    type_dependency_traversal(statement, None, node)
            elif type(node) is PatternMatchAST:
                for block in node.blocks:
                    for statement in block:
                        type_dependency_traversal(statement, None, current_function)
            elif type(node) is AssignmentAST:
                type_dependency_traversal(node.right, node.left, current_function)
            elif type(node) is FunctionCallAST:
                if assigned_variable:
                    type_dependency_pairs.add(UndirectedPair(node, assigned_variable))
                elif current_function:
                    type_dependency_pairs.add(UndirectedPair(node, current_function))
            elif isinstance(node, BinaryOperatorAST):
                type_dependency_traversal(node.left, assigned_variable, current_function)
                type_dependency_traversal(node.right, assigned_variable, current_function)
            elif type(node) is VariableAST\
                    or type(node) is IntegerLiteralAST\
                    or type(node) is ArrayDefinitionAST\
                    or type(node) is ArraySliceAST\
                    or type(node) is ArrayIndexAST:
                if assigned_variable:
                    type_dependency_pairs.add(UndirectedPair(node, assigned_variable))
                elif current_function:
                    type_dependency_pairs.add(UndirectedPair(node, current_function))
            else:
                print(type(node))
                if type(node) is list:
                    print("\t", node)

        type_dependency_traversal(self.ast)

        def padleft(text, number):
            return " " * (number - len(str(text))) + str(text)

        print("TYPE DEPENDENCIES")
        for pair in type_dependency_pairs:
            print(padleft("(%s :: %s)" % (pair.x, pair.x.get_type()), 30), "<==>", "(%s :: %s)" % (pair.y, pair.y.get_type()), sep="     ")
        return self.ast
