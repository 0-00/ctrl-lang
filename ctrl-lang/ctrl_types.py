from ctrl_tree_drawing import *


class Curry:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + " -> " + str(self.right)

    def to_tree(self):
        return TreeNode("(->)", [self.left.to_tree(), self.right.to_tree()])

    def to_list(self):
        return self.left.to_list() + self.right.to_list()

    def get_return_type(self):
        return self.to_list()[-1]

    def is_completed_by(self, args):
        print(self.to_list()[:-1])
        print(args)
        return self.to_list()[:-1] == args


class ArrayType:
    def __init__(self, type, length):
        self.type = type
        self.length = length

    def __str__(self):
        return "[%s]" % str(self.type)

    def __eq__(self, other):
        return isinstance(other, DoubleType) and self.type == other.type

    def to_tree(self):
        return TreeNode(str(self), [])

    def to_list(self):
        return [self]

    def eval(self, builder, variable_map):
        return "[%s x %s]" % (self.length, self.type.eval(builder, variable_map))


class DoubleType:
    def __init__(self):
        pass

    def __str__(self):
        return "double"

    def __eq__(self, other):
        return isinstance(other, DoubleType)

    def to_tree(self):
        return TreeNode("double", [])

    def to_list(self):
        return [self]

    def eval(self, builder, variable_map):
        return "double"


class IntegerType:
    def __init__(self):
        pass

    def __str__(self):
        return "int"

    def __eq__(self, other):
        return isinstance(other, DoubleType)

    def to_tree(self):
        return TreeNode("int", [])

    def to_list(self):
        return [self]

    def eval(self, builder, variable_map):
        return "i32"
