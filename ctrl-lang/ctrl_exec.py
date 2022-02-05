from __future__ import print_function
from ctypes import CFUNCTYPE, c_float, c_double, c_int
import llvmlite.binding as llvm


def create_execution_engine():
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = llvm.parse_assembly("")
    llvm.load_library_permanently("D:\\Downloads\\pthreads-w32-2-9-1-release\\Pre-built.2\\dll\\x86\\pthreadGC2.dll")
    llvm.load_library_permanently("D:\\Downloads\\glfw-3.3.2.bin.WIN32\\glfw-3.3.2.bin.WIN32\\lib-vc2019\\glfw3.dll")
    return llvm.create_mcjit_compiler(backing_mod, target_machine)


def compile_ir(engine, llvm_ir):
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod


class Execute:
    def __init__(self, ir):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.engine = create_execution_engine()
        self.mod = compile_ir(self.engine, ir)

    def run(self):
        func_ptr = self.engine.get_function_address("main")
        cfunc = CFUNCTYPE(c_int, c_int)(func_ptr)
        input_arg = 5
        res = cfunc(input_arg)
        print("main("+ str(input_arg) + ") =", res)

    def mod(self):
        return self.mod
