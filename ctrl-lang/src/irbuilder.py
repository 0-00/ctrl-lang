class IRBuilder:
    def __init__(self):
        self.s = ""
        self.variable_count = 0
        self.temp_variables = dict()
        self.open_block = "entry"
        self.incoming_edges = {}

    def add_incoming(self, variable):
        self.incoming_edges[self.open_block] = variable

    def phi(self, type):
        self.s += "\t\t%%\".%s\" = phi %s %s\n" % (self.variable_count, type, ", ".join(["[%s, %%%s]" % edges[::-1] for edges in list(self.incoming_edges.items())]))
        self.variable_count += 1
        return "%%\".%s\"" % str(self.variable_count - 1)

    def label(self, label):
        self.s += "\t" + label + ":\n"
        self.open_block = label

    def branch(self, dest):
        self.s += "\t\tbr label %%%s\n" % dest

    def conditional_branch(self, condition, then, else_then):
        self.s += "\t\tbr i1 %s, label %%%s, label %%%s\n" % (condition, then, else_then)

    def assign(self, left):
        self.temp_variables[left] = "%%\".%s\"" % str(self.variable_count)
        return

    def alloca(self, type):
        self.s += "\t\t%%\".%s\" = alloca %s\n" % (str(self.variable_count), type)
        self.variable_count += 1
        return "%%\".%s\"" % str(self.variable_count - 1)

    def store(self):
        self.s += "store %s "
        return

    def gep(self):
        self.s += "getelementptr "
        return

    def fcmp(self, left, right):
        return self.binop("fcmp oeq", "double", left, right)

    def icmp(self, left, right):
        return self.binop("icmp eq", "i32", left, right)

    def fmul(self, left, right):
        return self.binop("fmul", "double", left, right)

    def fadd(self, left, right):
        return self.binop("fadd", "double", left, right)

    def fsub(self, left, right):
        return self.binop("fsub", "double", left, right)

    def fdiv(self, left, right):
        return self.binop("fdiv", "double", left, right)

    def mul(self, left, right):
        return self.binop("mul", "i32", left, right)

    def add(self, left, right):
        return self.binop("add", "i32", left, right)

    def sub(self, left, right):
        return self.binop("sub", "i32", left, right)

    def div(self, left, right):
        return self.binop("div", "i32", left, right)

    def binop(self, op, type, left, right):
        self.s += "\t\t%%\".%s\" = %s %s %s, %s\n" % (str(self.variable_count), op, type, self.get_variable(left), self.get_variable(right))
        self.variable_count += 1
        return "%%\".%s\"" % str(self.variable_count - 1)

    def get_variable(self, identifier):
        if identifier in self.temp_variables.keys():
            return self.temp_variables[identifier]
        return identifier

    def function_call(self, function_name, arg_list, type_expression):
        type_list = type_expression.to_list()
        arg_types = type_list[:-1]
        return_type = type_list[-1]
        self.s += "\t\t%%\".%s\" = call %s @\"%s\" (%s)\n" % (str(self.variable_count),
                                                             return_type.eval(self, None),
                                                             function_name.name,
                                                             ", ".join(["%s %s" % (arg[0].eval(self, None), self.get_variable(arg[1]))
                                                                        for arg in zip(arg_types, arg_list)]))
        self.variable_count += 1
        return "%%\".%s\"" % str(self.variable_count - 1)

    def build_partial(self):
        pass

    def get_return(self, type):
        return self.s + "\t\tret %s %%\".%s\"\n" % (type, str(self.variable_count - 1))