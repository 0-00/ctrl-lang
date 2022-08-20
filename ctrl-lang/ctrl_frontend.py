from ctrl_lexer import Lexer
from ctrl_parser import Parser
from ctrl_ast import AST
from ctrl_typechecker import TypeChecker
# from ctrl_exec import Execute
# from ctrl_compile import Compile


def main():
    file = "examples/experiment/experiment"
    with open(file + ".ctrl") as f:
        text_input = f.read()

    lexer = Lexer().build_lexer()
    tokens = lexer.lex(text_input)

    parse_tree = Parser().parse([token for token in tokens])
    if parse_tree is None:
        return
    print(parse_tree)
    ast = AST(parse_tree)
    print(ast)
    TypeChecker(ast).check()
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
