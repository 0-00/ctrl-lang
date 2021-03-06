
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftADDSUBleftMULDIVADD ASSIGNMENT CURRY DIV ENDL LPAREN MUL NUMBER RPAREN SPACE SUB TAB TYPEDEF WORDfunction : function_declaration block ENDLfunction_declaration : identifier arguments TYPEDEF type_expression ENDLarguments : arguments argumentsarguments : SPACE identifierblock : block blockblock : TAB statement ENDLstatement : identifier ASSIGNMENT expressionstatement : expressiontype_expression : type_expression CURRY type_expressiontype_expression : LPAREN type_expression RPARENtype_expression : identifierexpression : expression ADD expression\n                  | expression SUB expression\n                  | expression MUL expression\n                  | expression DIV expressionexpression : LPAREN expression RPARENexpression : NUMBERexpression : identifieridentifier : WORD'
    
_lr_action_items = {'WORD':([0,6,8,14,17,20,21,22,23,24,29,37,],[4,4,4,4,4,4,4,4,4,4,4,4,]),'$end':([1,10,],[0,-1,]),'TAB':([2,5,9,19,36,],[6,6,6,-6,-2,]),'SPACE':([3,4,7,16,18,],[8,-19,8,8,-4,]),'ASSIGNMENT':([4,12,],[-19,20,]),'ADD':([4,12,13,15,25,26,30,31,32,33,34,35,],[-19,-18,21,-17,21,-18,21,-12,-13,-14,-15,-16,]),'SUB':([4,12,13,15,25,26,30,31,32,33,34,35,],[-19,-18,22,-17,22,-18,22,-12,-13,-14,-15,-16,]),'MUL':([4,12,13,15,25,26,30,31,32,33,34,35,],[-19,-18,23,-17,23,-18,23,23,23,-14,-15,-16,]),'DIV':([4,12,13,15,25,26,30,31,32,33,34,35,],[-19,-18,24,-17,24,-18,24,24,24,-14,-15,-16,]),'ENDL':([4,5,9,11,12,13,15,19,26,27,28,30,31,32,33,34,35,39,40,],[-19,10,-5,19,-18,-8,-17,-6,-18,-11,36,-7,-12,-13,-14,-15,-16,-9,-10,]),'TYPEDEF':([4,7,16,18,],[-19,17,-3,-4,]),'RPAREN':([4,15,25,26,27,31,32,33,34,35,38,39,40,],[-19,-17,35,-18,-11,-12,-13,-14,-15,-16,40,-9,-10,]),'CURRY':([4,27,28,38,39,40,],[-19,-11,37,37,37,-10,]),'LPAREN':([6,14,17,20,21,22,23,24,29,37,],[14,14,29,14,14,14,14,14,29,29,]),'NUMBER':([6,14,20,21,22,23,24,],[15,15,15,15,15,15,15,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'function':([0,],[1,]),'function_declaration':([0,],[2,]),'identifier':([0,6,8,14,17,20,21,22,23,24,29,37,],[3,12,18,26,27,26,26,26,26,26,27,27,]),'block':([2,5,9,],[5,9,9,]),'arguments':([3,7,16,],[7,16,16,]),'statement':([6,],[11,]),'expression':([6,14,20,21,22,23,24,],[13,25,30,31,32,33,34,]),'type_expression':([17,29,37,],[28,38,39,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> function","S'",1,None,None,None),
  ('function -> function_declaration block ENDL','function',3,'p_function','ctrl_parser3.py',71),
  ('function_declaration -> identifier arguments TYPEDEF type_expression ENDL','function_declaration',5,'p_function_declaration','ctrl_parser3.py',76),
  ('arguments -> arguments arguments','arguments',2,'p_arguments_arguments','ctrl_parser3.py',81),
  ('arguments -> SPACE identifier','arguments',2,'p_arguments','ctrl_parser3.py',87),
  ('block -> block block','block',2,'p_block_block_block','ctrl_parser3.py',93),
  ('block -> TAB statement ENDL','block',3,'p_block_statement','ctrl_parser3.py',99),
  ('statement -> identifier ASSIGNMENT expression','statement',3,'p_statement_assign','ctrl_parser3.py',105),
  ('statement -> expression','statement',1,'p_statement_expr','ctrl_parser3.py',111),
  ('type_expression -> type_expression CURRY type_expression','type_expression',3,'p_type_expression_curry','ctrl_parser3.py',117),
  ('type_expression -> LPAREN type_expression RPAREN','type_expression',3,'p_type_expression_group','ctrl_parser3.py',123),
  ('type_expression -> identifier','type_expression',1,'p_type_expression_identifier','ctrl_parser3.py',129),
  ('expression -> expression ADD expression','expression',3,'p_expression_binop','ctrl_parser3.py',135),
  ('expression -> expression SUB expression','expression',3,'p_expression_binop','ctrl_parser3.py',136),
  ('expression -> expression MUL expression','expression',3,'p_expression_binop','ctrl_parser3.py',137),
  ('expression -> expression DIV expression','expression',3,'p_expression_binop','ctrl_parser3.py',138),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','ctrl_parser3.py',154),
  ('expression -> NUMBER','expression',1,'p_expression_number','ctrl_parser3.py',160),
  ('expression -> identifier','expression',1,'p_expression_identifier','ctrl_parser3.py',166),
  ('identifier -> WORD','identifier',1,'p_identifier','ctrl_parser3.py',172),
]
