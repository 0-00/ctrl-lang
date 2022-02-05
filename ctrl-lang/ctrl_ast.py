from ctrl_tree_drawing import *
from ctrl_parser import *
from ctrl_irbuilder import IRBuilder


class BinaryOperatorAST:
    def __init__(self, left, right, type):
        self.left = left
        self.right = right
        self.type = type

    def get_type(self):
        return self.left.get_type()

    def get_return_type(self):
        return self.left.get_type()


class AssignmentAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        builder.assign(self.left.eval(builder, variable_map))
        return self.right.eval(builder, variable_map)

    def to_tree(self):
        return TreeNode("(=)", [self.left.to_tree(), self.right.to_tree()])


class AddfAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.fadd(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(+)", [self.left.to_tree(), self.right.to_tree()])


class MulfAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.fmul(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(*)", [self.left.to_tree(), self.right.to_tree()])


class DivfAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.fdiv(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(/)", [self.left.to_tree(), self.right.to_tree()])


class SubfAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.fsub(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(-)", [self.left.to_tree(), self.right.to_tree()])


class AddiAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.add(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(+)", [self.left.to_tree(), self.right.to_tree()])


class MuliAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.mul(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(*)", [self.left.to_tree(), self.right.to_tree()])


class DiviAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.div(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(/)", [self.left.to_tree(), self.right.to_tree()])


class SubiAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.sub(self.left.eval(builder, variable_map),
                            self.right.eval(builder, variable_map))

    def to_tree(self):
        return TreeNode("(-)", [self.left.to_tree(), self.right.to_tree()])


class PatternMatchAST:
    def __init__(self, patterns, blocks):
        self.patterns = patterns
        self.blocks = blocks

    def to_tree(self):
        patterns_node = TreeNode("Patterns", [pattern.to_tree() for pattern in self.patterns])
        blocks_node = TreeNode("Blocks", [block.to_tree() for block in self.blocks])
        return TreeNode("Match", [patterns_node, blocks_node])

    def eval(self, builder, variable_map):
        pattern_labels = ["pattern." + str(i) for i in range(len(self.patterns))] + ["pattern.error"]
        block_labels = ["case." + str(i) for i in range(len(self.patterns))]

        i = 0
        for pattern in self.patterns:
            ret = pattern.eval(builder, variable_map)
            builder.conditional_branch(ret, block_labels[i], pattern_labels[i+1])
            builder.label(pattern_labels[i+1])
            i += 1

        builder.branch(block_labels[0])
        i = 0
        for block in self.blocks:
            builder.label(block_labels[i])
            builder.add_incoming(block.eval(builder, variable_map))
            builder.branch("end")
            i += 1
        builder.label("end")
        builder.phi(self.blocks[0].get_type().eval(builder, variable_map))


class PatternLiteralAST:
    def __init__(self, conditional_variable, value):
        self.value = value
        self.conditional_variable = conditional_variable

    def to_tree(self):
        return TreeNode(str(self.value), [])

    def eval(self, builder, variable_map):
        if isinstance(self.conditional_variable.get_type(), IntegerType):
            return builder.icmp(self.conditional_variable.eval(builder, variable_map), self.value)
        elif isinstance(self.conditional_variable.get_type(), DoubleType):
            return builder.fcmp(self.conditional_variable.eval(builder, variable_map), self.value)


class PatternWildcardAST:
    def __init__(self, conditional_variable):
        self.conditional_variable = conditional_variable

    def to_tree(self):
        return TreeNode("_", [])

    def eval(self, builder, variable_map):
        if isinstance(self.conditional_variable.get_type(), IntegerType):
            return builder.icmp(self.conditional_variable.eval(builder, variable_map), self.conditional_variable.eval(builder, variable_map))
        elif isinstance(self.conditional_variable.get_type(), DoubleType):
            return builder.fcmp(self.conditional_variable.eval(builder, variable_map), self.conditional_variable.eval(builder, variable_map))


class VariableAST:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def eval(self, builder, variable_map):
        return "%\"" + self.name + "\""

    def to_tree(self):
        return TreeNode(self.name, [])

    def get_type(self):
        return self.type

    def get_return_type(self):
        return self.get_type()

    def __str__(self):
        return self.name


class LiteralAST:
    def __init__(self, value):
        self.value = value

    def to_tree(self):
        return TreeNode(self.value, [])


class DoubleLiteralAST(LiteralAST):
    def get_type(self):
        return DoubleType()

    def get_return_type(self):
        return self.get_type()

    def eval(self, builder, variable_map):
        return builder.fadd(0.0, self.value)    # self.value


class IntegerLiteralAST(LiteralAST):
    def get_type(self):
        return IntegerType()

    def get_return_type(self):
        return self.get_type()

    def eval(self, builder, variable_map):
        return builder.add(0, self.value)    # self.value


class ArrayDefinitionAST:
    def __init__(self, member_type, length, initial_block):
        self.member_type = member_type
        self.length = length
        self.type = ArrayType(member_type, length)
        self.initial_block = initial_block

    def eval(self, builder, variable_map):
        builder.alloca(self.type.eval(builder, variable_map))
        for statement in self.initial_block:
            statement.eval(builder, variable_map)

    def get_type(self):
        self.type

    def get_return_type(self):
        return self.get_type()

    def to_tree(self):
        child_statements = [statement.to_tree() for statement in self.initial_block]
        return TreeNode("[]", child_statements)


class FunctionApplicationAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        if type(self.left) is FunctionApplicationAST:
            self.left.eval(builder, variable_map)
        else:
            return builder.function_call(self.left, [self.right])

    def to_tree(self):
        if type(self.left) is FunctionApplicationAST:
            left_node = self.left.to_tree()
        else:
            left_node = TreeNode(self.left, [])
        return TreeNode("(->)", [left_node, TreeNode(self.right, [])])

class FunctionCallAST(BinaryOperatorAST):
    def eval(self, builder, variable_map):
        return builder.function_call(self.left, [arg.eval(builder, variable_map) for arg in self.right], self.get_type())

    def to_tree(self):
        return TreeNode(self.left.name, [arg.to_tree() for arg in self.right])

    def get_return_type(self):
        return self.get_type().get_return_type()


class FunctionDefinition:
    def __init__(self, function):
        self.name = function.name
        self.arg_list = function.arg_list
        self.type_expression = function.type_expression
        self.block = []    # function.block

    def to_tree(self):
        return TreeNode(self.name, [statement.to_tree() for statement in self.block])

    def eval(self, types, variables):
        block = ""
        builder = IRBuilder()
        type_list = self.type_expression.to_list()
        arg_types = type_list[:-1]
        return_type = type_list[-1]
        if len(self.arg_list) > 1:
            args = ""
            for arg in zip(arg_types, self.arg_list):
                args += "%s %%\"%s\", " % arg
            if len(args) > 2:
                args = args[:-2]
            block += "define %s @\"%s\"(%s) nounwind\n{\n" % (return_type.eval(builder, variables), self.name, args)
            builder.label("entry")
            # type_list_str = ""
            # for t in arg_types:
            #     type_list_str += str(t) + ", "
            #
            # arg_type_name = "%%\"%s.args\"" % self.name
            #
            # block += "%s = type {%s}\n"\
            #          % (arg_type_name, type_list_str[:-2])
            #
            # block += "define %s @\"%s\"(%s* %%\".args\")\n"\
            #          % (return_type, self.name, arg_type_name)
            #
            # block += "{\nentry:\n"
            # i = 0
            # for arg in self.arg_list:
            #     block += "%%\"%s\" = getelementptr %s, %s* %%\".args\", i32 0, i32 %s\n"\
            #              % (i, arg_type_name, arg_type_name, i)
            #
            #     block += "%%\"%s\" = load %s, %s* %%\"%s\"\n"\
            #              % (arg, type_list[i], type_list[i], i)
            #     i += 1
        else:
            block += "define %s @\"%s\"(%s)\n{\n" % (return_type.eval(builder, variables), self.name,
                                                     ", ".join(["%s %%\"%s\"" % (arg[0].eval(builder, variables), arg[1])
                                                                for arg in zip(arg_types, self.arg_list)]))
            builder.label("entry")
        for statement in self.block:
            statement.eval(builder, variables)
        # builder.ret(ret)
        block += builder.get_return(return_type.eval(builder, variables))
        block += "}\n\n"
        return block


class AST:
    def __init__(self, parse_tree):
        self.children = []

        def create_pattern(conditional_variable, pattern):
            if isinstance(pattern, NumberLiteral):
                return PatternLiteralAST(conditional_variable, pattern.value)
            elif isinstance(pattern, WildcardLiteral):
                return PatternWildcardAST(conditional_variable)

        def traverse_pipe(node, variable_scope):
            if isinstance(node.left, BinaryOperator) and node.operator == "->":
                return traverse_pipe(node.left, variable_scope) + [traverse(node.right, variable_scope)]
            else:
                return [traverse(node.left, variable_scope), (traverse(node.right, variable_scope))]

        def traverse(node, variable_scope):
            if isinstance(node, ModuleParseTree):
                ret = []
                for child in node.children:
                    traversal = traverse(child, variable_scope)
                    ret.append(traversal)
                return ret

            if isinstance(node, Function):
                if node.block:
                    ret = FunctionDefinition(node)
                    local_vars = dict(zip(node.arg_list, node.type_expression.to_list()[:-1]))
                    total_vars = {**local_vars, **variables}
                    # print(total_vars)
                    for child in node.block:
                        ret.block.append(traverse(child, total_vars))
                    return ret

            if isinstance(node, Identifier):
                return VariableAST(node.name, variable_scope[node.name])

            if isinstance(node, FloatLiteral):  # yikes
                return DoubleLiteralAST(node.value)

            if isinstance(node, IntLiteral):
                return IntegerLiteralAST(node.value)

            if isinstance(node, ArrayLiteral):
                entries = [traverse(entry, variable_scope) for entry in node.entries]
                return ArrayDefinitionAST(entries[0].get_return_type(), len(node.entries), entries)

            if isinstance(node, Match):
                patterns = []
                blocks = []
                control = traverse(node.control_variable, variable_scope)
                for case in node.cases:
                    patterns.append(create_pattern(control, case.pattern))
                    blocks.append(traverse(case.block, variable_scope))
                return PatternMatchAST(patterns, blocks)

            if isinstance(node, BinaryOperator):
                if node.operator == "=":
                    right = traverse(node.right, variable_scope)
                    variable_scope[node.left.name] = right.get_return_type()
                    left = traverse(node.left, variable_scope)
                    return AssignmentAST(left, right, DoubleType())
                elif node.operator == "*":
                    left = traverse(node.left, variable_scope)
                    right = traverse(node.right, variable_scope)
                    left_type = left.get_return_type()
                    right_type = right.get_return_type()
                    if isinstance(left_type, DoubleType) and isinstance(right_type, DoubleType):
                        return MulfAST(left, right, DoubleType())
                    elif isinstance(left_type, IntegerType) and isinstance(right_type, IntegerType):
                        return MuliAST(left, right, IntegerType())
                    else:
                        print("* NODE INCONSISTENT TYPES ERROR : ", node, "left : ", left_type, "right : ", right_type)
                        # if types differ, inject cast to double
                        return None
                elif node.operator == "+":
                    left = traverse(node.left, variable_scope)
                    right = traverse(node.right, variable_scope)
                    left_type = left.get_return_type()
                    right_type = right.get_return_type()
                    if isinstance(left_type, DoubleType) and isinstance(right_type, DoubleType):
                        return AddfAST(left, right, DoubleType())
                    elif isinstance(left_type, IntegerType) and isinstance(right_type, IntegerType):
                        return AddiAST(left, right, IntegerType())
                    else:
                        print("+ NODE INCONSISTENT TYPES ERROR : ", node)
                        # if types differ, inject cast to double
                        return None
                elif node.operator == "-":
                    left = traverse(node.left, variable_scope)
                    right = traverse(node.right, variable_scope)
                    left_type = left.get_return_type()
                    right_type = right.get_return_type()
                    if isinstance(left_type, DoubleType) and isinstance(right_type, DoubleType):
                        return SubfAST(left, right, DoubleType())
                    elif isinstance(left_type, IntegerType) and isinstance(right_type, IntegerType):
                        return SubiAST(left, right, IntegerType())
                    else:
                        print("- NODE INCONSISTENT TYPES ERROR : ", node)
                        # if types differ, inject cast to double
                        return None
                elif node.operator == "\\":
                    left = traverse(node.left, variable_scope)
                    right = traverse(node.right, variable_scope)
                    left_type = left.get_return_type()
                    right_type = right.get_return_type()
                    if isinstance(left_type, DoubleType) and isinstance(right_type, DoubleType):
                        return DivfAST(left, right, DoubleType())
                    elif isinstance(left_type, IntegerType) and isinstance(right_type, IntegerType):
                        return DiviAST(left, right, IntegerType())
                    else:
                        print("\\ NODE INCONSISTENT TYPES ERROR : ", node)
                        # if types differ, inject cast to double
                        return None
                elif node.operator == "->":
                    pipe = traverse_pipe(node, variable_scope)
                    function_name = pipe[0]
                    function_args = pipe[1:]
                    return FunctionCallAST(function_name, function_args, variable_scope[function_name.name])
                    # print("funname:", function_name)
                    # print("funargs:", [arg.name for arg in function_args])
                    # if variable_scope[function_name.name].is_completed_by([variable_scope[arg.name] for arg in function_args]):
                    #     return FunctionCallAST(function_name, function_args, variable_scope[function_name.name])
                    # else:
                    #     print("PartialFunctionCall")
                    #     return None #PartialFunctionCall
                print("NODE NOT IDENTIFIED ERROR : ", node)
                return None

        variables = dict([(node.name, node.type_expression) for node in parse_tree.children])
        self.children = traverse(parse_tree, variables)

    def __str__(self):
        return "\nAST TREE\n\n" + str(TreeDrawing(TreeNode("module", [child.to_tree() for child in self.children]))) + "\n\n"

    def eval(self):
        body = ""

        for child in self.children:
            body += child.eval([], {}) + "\n"
        return body
