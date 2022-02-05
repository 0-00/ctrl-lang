from ctrl_lexer import Lexer
from ctrl_parser import Parser
from ctrl_ast import AST
from ctrl_exec import Execute
from ctrl_compile import Compile

file = "examples/experiment/experiment"
with open(file + ".ctrl") as f:
    text_input = f.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

parse_tree = Parser().parse([token for token in tokens])
print(parse_tree)
ast = AST(parse_tree)
print(ast)
llvm_ir = ast.eval()

with open(file + ".ll", 'w', encoding="utf-8") as output_file:
    output_file.write(llvm_ir)

execute = Execute(llvm_ir)
comp = Compile(execute.mod)
comp.save_assembly(file + ".s")
comp.save_object(file + ".out")
execute.run()
