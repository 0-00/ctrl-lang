from colorama import Fore, Back, Style
from ctrl_lexer import Lexer
from ctrl_parser import *
from rply import Token
from ctrl_tree_drawing import *
import random
from functools import reduce


def identity(tokens, name):
    return True


def count_tokens(tokens, name):
    return sum(1 for token in tokens if token.name == name)


def assert_exception(function, input):
    try:
        function(input)
    except:
        return True
    else:
        return False


def assert_exception_if_output(condition):
    def x(function, input):
        try:
            output = function(input)
        except:
            return True
        else:
            return not condition(output)
    return x


def if_input(input_condition, then=identity, condition_unmet=identity):
    def x(function, input):
        if input_condition(input):
            return then(function, input)
        else:
            return condition_unmet(function, input)
    return x


def generate_expression_input():
    # build_expression Input assumptions:
    #        ~~~~~~~~~~~
    # - only contains valid token types and output of preprocessed literals

    # generated input currently missing preprocessed literals
    valid_token_list = ["OPEN_PAREN", "CLOSE_PAREN", "PIPE", "ADD", "SUB", "MUL", "DIV", "DOUBLE", "FLOAT", "INTEGER", "WORD"]
    return [Token(token_type, "a", None) for token_type in random.choices(valid_token_list, k=random.randrange(100))]


def generate_type_expression_input():
    # build_expression Input assumptions:
    #        ~~~~~~~~~~~
    # - only contains valid token types and output of preprocessed literals

    # generated input currently missing preprocessed literals
    valid_token_list = ["OPEN_PAREN", "CLOSE_PAREN", "DOUBLE", "INTEGER", "RIGHT_ARROW"]
    return [Token(token_type, "a", None) for token_type in random.choices(valid_token_list, k=random.randrange(100))]


def generate_statement_input():
    # build_statement Input assumptions:
    #        ~~~~~~~~~~~
    # - only contains valid token types and output of preprocessed literals

    # generated input currently missing preprocessed literals
    valid_token_list = ["OPEN_PAREN", "CLOSE_PAREN", "PIPE", "ADD", "SUB", "MUL", "DIV", "DOUBLE", "FLOAT", "INTEGER", "WORD", "ASSIGNMENT", "THICK_RIGHT_ARROW", "VERT"]
    return [Token(token_type, "a", None) for token_type in random.choices(valid_token_list, k=random.randrange(100))]


class TestingSuite:
    def __init__(self):
        self.children = []

    def add(self, category):
        self.children.append(category)
        return self

    def run_tests(self):
        length = max([child.get_length() for child in self.children])

        for child in self.children:
            child.run_tests(length)


class TestableUnit:
    def __init__(self, function_to_test, input_generator):
        self.function_to_test = function_to_test
        self.input_generator = input_generator
        self.children = []

    def add_tests(self, *tests):
        for test in tests:
            self.add_unit_test(test["function"], test["name"], test["iterations"])
        return self

    def add_unit_test(self, function, name, tests=10000):
        self.children.append(UnitTest(function, tests, name))

    def get_length(self):
        if len(self.children) == 0:
            return 0
        return max([child.get_length() for child in self.children])

    def run_tests(self, length):
        print(Back.LIGHTMAGENTA_EX + Fore.BLACK + self.function_to_test.__name__ + Style.RESET_ALL)
        i = 0
        for test in self.children:
            passed_count = 0
            failed_count = 0
            failed = []
            padding = length - test.get_length()
            inputs = [self.input_generator() for i in range(test.iterations)]
            for input in inputs:
                test_result = test.run(self.function_to_test, input)
                if test_result:
                    passed_count += 1
                else:
                    failed_count += 1
                    failed.append(input)
                print("\r", end="")
                print(Style.RESET_ALL + test.get_name() + ": " + " " * padding,
                      Fore.GREEN + str(passed_count), "passed", Style.RESET_ALL + "/",
                      Fore.RED + str(failed_count), "failed", Style.RESET_ALL + "/",
                      Style.RESET_ALL + str(test.get_iterations()), "total",
                      end=Style.RESET_ALL)
            i += 1
            print()
            # if False:
            for f in failed:
                print(Back.RED + str([token.gettokentype() for token in f]))
        print()


class UnitTest:
    def __init__(self, test_function, iterations, name):
        self.test_function = test_function
        self.iterations = iterations
        self.name = name

    def get_name(self):
        return self.name

    def get_function_name(self):
        return self.test_function.__name__

    def get_length(self):
        return len(self.name)

    def get_iterations(self):
        return self.iterations

    def run(self, function_to_test, input):
        return self.test_function(function_to_test, input)


# Assert that the below fail:
#
# For expressions:
# ✅ Input containing unbalanced parenthesis within an expression
# ✅ Output containing operations with null children
#
# For type expressions:
# ✅ Input containing unbalanced parenthesis within an expression
# ✅ Output containing operations with null children
#
# For statements:
# ✅ Input containing more than one assignment token
# ✅ Input containing more than one vert token
# ✅ Input containing more than one thick right arrow token
# ❌ Input contains one of vert token xor thick right arrow token
# ❌ Output not of assignment data type when input containing assignment token
# ❌ Does not pass vert, assignment, or thick right arrow tokens to build_expression
#    (might need to refactor build_statement to provide tokens for expression as an output?)

has_unbalanced_brackets = lambda input_tokens: count_tokens(input_tokens, "OPEN_PAREN") != count_tokens(input_tokens, "CLOSE_PAREN")
has_empty_brackets = lambda input_tokens: ("OPEN_PAREN", "CLOSE_PAREN") in [(input_tokens[i].gettokentype(), input_tokens[i+1].gettokentype()) for i in range(len(input_tokens)-1)]
has_null_children = lambda node: type(node) is BinaryOperator\
                                 and (node.left is None\
                                 or node.right is None\
                                 or has_null_children(node.left)\
                                 or has_null_children(node.right))
has_more_tokens_than = lambda token, count: lambda input_tokens: count_tokens(input_tokens, token) > count

test_suite = TestingSuite().add(TestableUnit(build_statement, generate_statement_input).add_tests(
    {
        "function": if_input(has_more_tokens_than("VERT", 1), then=assert_exception),
        "name": "No more than one | token",
        "iterations": 1000
    },
    {
        "function": if_input(has_more_tokens_than("ASSIGNMENT", 1), then=assert_exception),
        "name": "No more than one := token",
        "iterations": 1000
    },
    {
        "function": if_input(has_more_tokens_than("THICK_RIGHT_ARROW", 1), then=assert_exception),
        "name": "No more than one => token",
        "iterations": 1000
    }
)).add(TestableUnit(build_expression, generate_expression_input).add_tests(
    {
        "function": if_input(has_unbalanced_brackets, then=assert_exception),
        "name": "Parentheses balance",
        "iterations": 1000
    },
    {
        "function": if_input(has_empty_brackets, then=assert_exception),
        "name": "No empty brackets",
        "iterations": 1000
    },
    {
        "function": assert_exception_if_output(has_null_children),
        "name": "No null children",
        "iterations": 1000
    }
)).add(TestableUnit(build_type_expression, generate_type_expression_input).add_tests(
    {
        "function": if_input(has_unbalanced_brackets, then=assert_exception),
        "name": "Parentheses balance",
        "iterations": 1000
    },
    {
        "function": if_input(has_empty_brackets, then=assert_exception),
        "name": "No empty brackets",
        "iterations": 1000
    },
    {
        "function": assert_exception_if_output(has_null_children),
        "name": "No null children",
        "iterations": 1000
    }
))

test_suite.run_tests()
