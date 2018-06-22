import re
import sys
from token import Token
from scanner import Scanner

class Symbol_Table:
    '''A symbol table maps identifiers to locations.'''
    def __init__(self):
        self.symbol_table = {}
    def size(self):
        '''Returns the number of entries in the symbol table.'''
        return len(self.symbol_table)
    def location(self, identifier):
        '''Returns the location of an identifier.'''
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        index = len(self.symbol_table)
        self.symbol_table[identifier] = index
        return index

class Label:
    "Increments a label"
    def __init__(self):
        self.current_label = 0
    def next(self):
        '''Returns a new, unique label.'''
        self.current_label += 1
        return 'l' + str(self.current_label)

def indent(s, level):
    """ returns a string that displays the level of indentation"""
    return '    '*level + s + '\n'

# Each of the classes represents a node in the syntax tree
# indented method returns a string that displays its self in a tree like structure.
# code method returns a string with JVM bytecode for that section of the tree.
# true_code/false_code methods allow jumps in the bytecode depending on the intented use.

class Program_AST:
    """Base node"""
    def __init__(self, program):
        self.program = program
    def __repr__(self):
        return repr(self.program)
    def indented(self, level):
        return self.program.indented(level)
    def code(self):
        program = self.program.code()
        local = symbol_table.size()
        java_scanner = symbol_table.location('Java Scanner')
        return '.class public Program\n' + \
               '.super java/lang/Object\n' + \
               '.method public <init>()V\n' + \
               'aload_0\n' + \
               'invokenonvirtual java/lang/Object/<init>()V\n' + \
               'return\n' + \
               '.end method\n' + \
               '.method public static main([Ljava/lang/String;)V\n' + \
               '.limit locals ' + str(local) + '\n' + \
               '.limit stack 1024\n' + \
               'new java/util/Scanner\n' + \
               'dup\n' + \
               'getstatic java/lang/System.in Ljava/io/InputStream;\n' + \
               'invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V\n' + \
               'astore ' + str(java_scanner) + '\n' + \
               program + \
               'return\n' + \
               '.end method\n'

class Statements_AST:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        result = repr(self.statements[0])
        for st in self.statements[1:]:
            result += '; ' + repr(st)
        return result
    def indented(self, level):
        result = indent('Statements', level)
        for st in self.statements:
            result += st.indented(level+1)
        return result
    def code(self):
        result = ''
        for st in self.statements:
            result += st.code()
        return result

class If_AST:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' { ' + \
                       repr(self.then) + ' }'
    def indented(self, level):
        return indent('If', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        return self.condition.false_code(l1) + \
               self.then.code() + \
               l1 + ':\n'

class If_El_AST:
    def __init__(self, condition, then, _else):
        self.condition = condition
        self.then = then
        self._else = _else
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' { ' + \
                       repr(self.then) + ' } el { ' + repr(self._else) + ' }'
    def indented(self, level):
        return indent('If-El', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1) + \
               self._else.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next()
        return self.condition.false_code(l1) + \
               self.then.code() + \
               'goto ' + l2 + '\n' + \
               l1 + ':\n' + \
               self._else.code() + \
               l2 + ':\n'
        

class Wl_AST:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return 'wl ' + repr(self.condition) + ' { ' + \
                          repr(self.body) + ' }'
    def indented(self, level):
        return indent('Wl', level) + \
               self.condition.indented(level+1) + \
               self.body.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next()
        return l1 + ':\n' + \
               self.condition.false_code(l2) + \
               self.body.code() + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'

class Fr_AST:
    def __init__(self, assignment, body):
        self.assignment = assignment
        self.body = body
    def __repr__(self):
        return 'fr ' + repr(self.assignment) + ' { ' + \
                            repr(self.body) + ' }'
    def indented(self, level):
        return indent('Fr', level) + \
                self.assignment.indented(level+1) + \
                self.body.indented(level+1)
    def code(self):
        loc = symbol_table.location(self.assignment.identifier.identifier)
        l1 = label_generator.next()
        return self.assignment.code() + \
                l1 + ':\n' + \
                self.body.code() + \
                'iload ' + str(loc) + '\n' + \
                'sipush 1\n' + \
                'isub\n' + \
                'istore ' + str(loc) + '\n' + \
                'iload ' + str(loc) + '\n' + \
                'sipush 0\n' + \
                'if_icmpne ' + l1 + '\n'

class Assign_AST:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def __repr__(self):
        return repr(self.identifier) + ':' + repr(self.expression)
    def indented(self, level):
        return indent('Assign', level) + \
               self.identifier.indented(level+1) + \
               self.expression.indented(level+1)
    def code(self):
        loc = symbol_table.location(self.identifier.identifier)
        return self.expression.code() + \
               'istore ' + str(loc) + '\n'

class Ot_AST:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return 'ot ' + repr(self.expression)
    def indented(self, level):
        return indent('Ot', level) + self.expression.indented(level+1)
    def code(self):
        return 'getstatic java/lang/System/out Ljava/io/PrintStream;\n' + \
               self.expression.code() + \
               'invokestatic java/lang/String/valueOf(I)Ljava/lang/String;\n' + \
               'invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V\n'

class In_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return 'in ' + repr(self.identifier)
    def indented(self, level):
        return indent('In', level) + self.identifier.indented(level+1)
    def code(self):
        java_scanner = symbol_table.location('Java Scanner')
        loc = symbol_table.location(self.identifier.identifier)
        return 'aload ' + str(java_scanner) + '\n' + \
               'invokevirtual java/util/Scanner.nextInt()I\n' + \
               'istore ' + str(loc) + '\n'

class Comparison_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return repr(self.left) + self.op + repr(self.right)
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def true_code(self, label):
        op = { '<':'if_icmplt', '=':'if_icmpeq', '>':'if_icmpgt',
               '<=':'if_icmple', '!=':'if_icmpne', '>=':'if_icmpge' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'
    def false_code(self, label):
        # Invert operator to negate
        op = { '<':'if_icmpge', '=':'if_icmpne', '>':'if_icmple',
               '<=':'if_icmpgt', '!=':'if_icmpeq', '>=':'if_icmplt' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'

class BooleanExpression_AST:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return '(' + repr(self.left) + ' | ' + repr(self.right) + ')'
    def indented(self, level):
        return indent('|', level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def false_code(self, l1):
        l2 = label_generator.next()
        return self.left.true_code(l2) + \
               self.right.true_code(l2) + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'
    def true_code(self, l1):
        return self.left.true_code(l1) + \
               self.right.true_code(l1)
    
class BooleanTerm_AST:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return '(' + repr(self.left) + ' & ' + repr(self.right) + ')'
    def indented(self, level):
        return indent('&', level) + \
                self.left.indented(level+1) + \
                self.right.indented(level+1)
    def false_code(self, label):
        return self.left.false_code(label) + \
               self.right.false_code(label)
    def true_code(self, l1):
        l2 = label_generator.next()
        return self.left.false_code(l2) + \
               self.right.false_code(l2)  + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'
    
class BooleanFactor_AST:
    def __init__(self, bool_):
        self.bool_ = bool_
    def __repr__(self):
        return '(' + '& ' + repr(self.bool_) + ')'
    def indented(self, level):
        return indent('&', level) + \
                self.bool_.indented(level+1)
    def true_code(self, label):
        return self.bool_.false_code(label)
    def false_code(self, label):
        return self.bool_.true_code(label)
        
class Expression_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return '(' + repr(self.left) + self.op + repr(self.right) + ')'
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def code(self):
        op = { '+':'iadd', '-':'isub', '*':'imul', '/':'idiv' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + '\n'

class Number_AST:
    def __init__(self, number):
        self.number = number
    def __repr__(self):
        return self.number
    def indented(self, level):
        return indent(self.number, level)
    def code(self): # works only for short numbers
        return 'sipush ' + self.number + '\n'

class Identifier_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return self.identifier
    def indented(self, level):
        return indent(self.identifier, level)
    def code(self):
        loc = symbol_table.location(self.identifier)
        return 'iload ' + str(loc) + '\n'

# These functions make the recursive-descent parser.

def program():
    sts = statements()
    return Program_AST(sts)

def statements():
    result = [statement()]
    while scanner.lookahead() == Token.SEM:
        scanner.consume(Token.SEM)
        st = statement()
        result.append(st)
    return Statements_AST(result)


def statement():
    if scanner.lookahead() == Token.IF:
        return if_statement()
    elif scanner.lookahead() == Token.WL:
        return wl_statement()
    elif scanner.lookahead() == Token.FR:
        return fr_statement()
    elif scanner.lookahead() == Token.ID:
        return assignment()
    elif scanner.lookahead() == Token.OT:
        return ot_statement()
    elif scanner.lookahead() == Token.IN:
        return in_statement()    
    else: # error
        return scanner.consume(Token.IF, Token.FR, Token.WL, Token.ID, Token.IN,
                               Token.OT)

def if_statement():
    scanner.consume(Token.IF)
    condition = boolean_expression()
    scanner.consume(Token.LCRL)
    then = statements()
    scanner.consume(Token.RCRL)
    if scanner.lookahead() == Token.EL:
        scanner.consume(Token.EL)
        scanner.consume(Token.LCRL)
        _else = statements()
        scanner.consume(Token.RCRL)
        return If_El_AST(condition, then, _else)
    return If_AST(condition, then)

def wl_statement():
    scanner.consume(Token.WL)
    condition = boolean_expression()
    scanner.consume(Token.LCRL)
    body = statements()
    scanner.consume(Token.RCRL)
    return Wl_AST(condition, body)

def fr_statement():
    scanner.consume(Token.FR)
    ass = assignment()
    scanner.consume(Token.LCRL)
    body = statements()
    scanner.consume(Token.RCRL)
    return Fr_AST(ass, body)

def ot_statement():
    scanner.consume(Token.OT)
    ex = expression()
    return Ot_AST(ex)

def in_statement():
    scanner.consume(Token.IN)
    _id = identifier()
    return In_AST(_id)

def assignment():
    ident = identifier()
    scanner.consume(Token.BEC)
    expr = expression()
    return Assign_AST(ident, expr)

operator = { Token.LESS:'<', Token.EQ:'=', Token.GRTR:'>',
             Token.LEQ:'<=', Token.NEQ:'!=', Token.GEQ:'>=',
             Token.ADD:'+', Token.SUB:'-', Token.MUL:'*', Token.DIV:'/' }

def comparison():
    left = expression()
    op = scanner.consume(Token.LESS, Token.EQ, Token.GRTR,
                         Token.LEQ, Token.NEQ, Token.GEQ)
    right = expression()
    return Comparison_AST(left, operator[op], right)

def boolean_factor():
    if scanner.lookahead() == Token.NT:
        not_ = scanner.consume(Token.NT)
        bool_ = boolean_factor()
        result = BooleanFactor_AST(bool_)
    else:
        result = comparison()
    return result

def boolean_term():
    result = boolean_factor()
    while scanner.lookahead() == Token.AND:
        scanner.consume(Token.AND)
        right = boolean_factor()
        result = BooleanTerm_AST(result, right)
    return result

def boolean_expression():
    result = boolean_term()
    while scanner.lookahead() == Token.OR:
        scanner.consume(Token.OR)
        right = boolean_term()
        result = BooleanExpression_AST(result, right)
    return result

def expression():
    result = term()
    while scanner.lookahead() in [Token.ADD, Token.SUB]:
        op = scanner.consume(Token.ADD, Token.SUB)
        tree = term()
        result = Expression_AST(result, operator[op], tree)
    return result

def term():
    result = factor()
    while scanner.lookahead() in [Token.MUL, Token.DIV]:
        op = scanner.consume(Token.MUL, Token.DIV)
        tree = factor()
        result = Expression_AST(result, operator[op], tree)
    return result

def factor():
    if scanner.lookahead() == Token.LPAR:
        scanner.consume(Token.LPAR)
        result = expression()
        scanner.consume(Token.RPAR)
        return result
    elif scanner.lookahead() == Token.NUM:
        value = scanner.consume(Token.NUM)[1]
        return Number_AST(value)
    elif scanner.lookahead() == Token.ID:
        return identifier()
    else: # error
        return scanner.consume(Token.LPAR, Token.NUM, Token.ID)

def identifier():
    value = scanner.consume(Token.ID)[1]
    return Identifier_AST(value)

# Initialise objects

scanner = Scanner(sys.stdin)
symbol_table = Symbol_Table()
symbol_table.location('Java Scanner') # fix a location for the Java Scanner
label_generator = Label()

ast = program()
if scanner.lookahead() != None:
    print('syntax error: end of input expected but token ' +
          repr(scanner.lookahead()) + ' found')
    sys.exit()


# Uncomment follwing lines to to test the parser
# and display the syntax tree
#
# print(ast.indented(0), end='')
# sys.exit()

# Call the code generator.
print(ast.code(), end='')

