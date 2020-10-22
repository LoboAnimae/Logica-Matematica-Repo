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
  r'[p-z]'
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

precedence = (
  ('left', 'DOUBLEIMPLIES'),
  ('left', 'IMPLIES'),
  ('left', 'OR'),
  ('left', 'AND'),
  ('left', 'NOT'),
  ('left', 'LBRACKET')
)

current_lexer = lex.lex()

def p_create(p):
  """
  create : parameter
         | equal_var
         | empty 
  """
  print("TREE", p[1])
  print('Status: ' + str(use(p[1])))

def p_equal_var(p):
  """
  equal_var : VARIABLE EQUALS parameter
  """
  p[0] = ('=', p[1], p[3])

def p_parameter(p):
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
  try:
    if type(p) == tuple:
      global env
      if p[0] == '=>': return False if use(p[1]) == True and not (use(p[2])) else True
      elif p[0] == '<=>': return True if use(p[1]) == use(p[2]) else False
      elif p[0] == '^': return (use(p[1]) and use(p[2]))
      elif p[0] == 'o': return (use(p[1]) or use(p[2]))
      elif p[0] == '~': return not use(p[1])
      elif p[0] == '=': env[p[1]] = use(p[2])
      elif p[0] == 'VARIABLE': return 'Syntax error: VARIABLE NOT FOUND' if p[1] not in env else env[p[1]]
    else: return p
  except: print('Invalid Statement')

while True:
    try: 
      s = input('>>> ')
      console_manager().clear()
    except EOFError: break
    parser.parse(s)