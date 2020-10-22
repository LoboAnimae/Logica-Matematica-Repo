from os import system
import ply.lex as lex
import ply.yacc as yacc


class console_manager(object):
  def __init__(self):
    from os import name
    self.os = name
    self.clear()
  def clear(self):
    system('cls') if self.os == 'nt' else system('clear')



cm = console_manager()
print('Hello')
input('Press enter to continue\n>>> ')
cm.clear()

input('Cleared the screen!')

tokens = (
  'VARIABLE',
  'NOT',
  'AND',
  'OR',
  'IMPLIES', 
  'DOUBLEIMPLIES',
  'LBRACKET',
  'RBRACKET',
  'TRUE',
  'FALSE',
  'EQUALS'
)

t_NOT = r'\~'
t_AND = r'\^'
t_OR = r'o'
t_IMPLIES = r'\=>'
t_DOUBLEIMPLIES = r'\<=>'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_EQUALS = r'\='


t_ignore = r' '

def t_VARIABLE(t):
  r'[q-z]'
  t.type = 'VARIABLE'
  return t

def t_error(t):
  print('Caracter no inválido encontrado: %s' % t.value)
  t.lexer.skip(1)

def t_False(t):
  r'[0]'
  if t.value == '0': t.value = False
  return t

def t_True(t):
  r'[1]'
  if t.value == '1': t.value = True
  return t



current_lexer = lex.lex()

def p_create(p):
  """
  create : parameter
         | equal_var
         | empty 
  """
  print("FOUND", p[1])
  print(use(p[1]))

def p_equal_var(p):
  """
  equal_var : VARIABLE EQUALS parameter
  """
  p[0] = ('=', p[1], p[3])

def parameter(p):
  """
  parameter : parameter AND parameter
            | parameter OR parameter
            | parameter IMPLIES parameter
            | parameter DOUBLEIMPLIES parameter
  """
  p[0] = (p[2], p[1], p[3])

def p_character_not(p):
  """
  parameter : NOT TRUE
            | NOT FALSE
            | NOT parameter
  """
  p[0] = (p[1], p[2])
  

def p_brackets(p):
  """
  parameter : LBRACKET parameter RBRACKET
  """
  p[0] = (p[2])

def p_VARIABLE(p):
  """
  parameter : VARIABLE
  """
  p[0] = ('VARIABLE', p[1])

def p_bool(p):
  """
  parameter : TRUE
            | FALSE
  """
  p[0] = p[1]

def p_empty(p):
  """
  empty :  
  """
  p[0] = None

parser = yacc.yacc()
env = {}

def use(p):
  