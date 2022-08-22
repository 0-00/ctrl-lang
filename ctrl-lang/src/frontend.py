from lexer import Lexer
from parser import Parser
from ast import AST
from typechecker import TypeChecker
from util.compile_error import CompileException

from colorama import Fore, Style

# from ctrl_exec import Execute
# from ctrl_compile import Compile


def main():
    file = "examples/experiment/experiment"
    file += ".ctrl"
    with open(file) as f:
        text_input = f.read()

    lexer = Lexer().build_lexer()
    tokens = lexer.lex(text_input)

    try:
        parse_tree = Parser().parse([token for token in tokens])
        print(parse_tree)
        ast = AST(parse_tree)
        print(ast)
        TypeChecker(ast).check()
    except CompileException as e:
        lines = text_input.split('\n')
        error_line = e.src_pos_line - 1
        error_coln = e.src_pos_col - 1

        if len(lines) > error_line:
            print(Fore.RED, end="")
            print("Error compiling", file, "at line", error_line + 1)
            print(lines[error_line])
            print(" " * error_coln, "^" * e.src_pos_length, sep="")
            print("Syntax Error:", e.msg, '\n', end=Style.RESET_ALL)
    except Exception as e:
        print("Unexpected error!")
        print(e)
    # llvm_ir = ast.eval()
    # print("LLVM IR\n\n", llvm_ir, sep="")

    # with open(file + ".ll", 'w', encoding="utf-8") as output_file:
    #     output_file.write(llvm_ir)

    # execute = Execute(llvm_ir)
    # comp = Compile(execute.mod)
    # comp.save_assembly(file + ".s")
    # comp.save_object(file + ".out")
    # execute.run()

main()
