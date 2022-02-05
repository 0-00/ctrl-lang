import llvmlite.binding as llvm


class Compile:
    def __init__(self, mod):
        # target = llvm.Target.from_triple(mod.triple)
        # target_machine = target.create_target_machine()
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        self.object = target_machine.emit_object(mod)
        self.assembly = target_machine.emit_assembly(mod)

    def save_object(self, filename):
        with open(filename, "wb") as o:
            o.write(self.object)

    def save_assembly(self, filename):
        with open(filename, 'w') as output_file:
            output_file.write(self.assembly)
