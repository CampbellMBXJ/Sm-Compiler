"""
Tokens and regular expressions for matching
in input
"""

__author__ = "Campbell Mercer-Butcher"

class Token:
    # The following enumerates all tokens.
    EL    = 'EL'
    IF    = 'IF'
    WL    = 'WL'
    FR    = 'FR'
    SEM   = 'SEM'
    BEC   = 'BEC'
    LESS  = 'LESS'
    EQ    = 'EQ'
    GRTR  = 'GRTR'
    LEQ   = 'LEQ'
    NEQ   = 'NEQ'
    GEQ   = 'GEQ'
    AND   = 'AND'
    NT    = 'NT'
    OR    = 'OR'
    ADD   = 'ADD'
    SUB   = 'SUB'
    MUL   = 'MUL'
    DIV   = 'DIV'
    LPAR  = 'LPAR'
    RPAR  = 'RPAR'
    LCRL  = 'LCRL'
    RCRL  = 'RCRL'
    NUM   = 'NUM'
    ID    = 'ID'
    IN    = 'IN'
    OT    = 'OT'    
    
    # Regular expression for matching tokens.
    token_regexp = [
        (EL,    'el'),
        (IF,    'if'),
        (WL,    'wl'),
        (FR,    'fr'),
        (IN,    'in'),
        (OT,    'ot'),
        (AND,   '&'),
        (NT,    'nt'),
        (OR,    '\\|'), # | is special in regular expressions
        (SEM,   ';'),
        (BEC,   ':'),
        (LESS,  '<'),
        (EQ,    '='),
        (MUL,   '\*'),
        (DIV,   '/'),
        (NEQ,   '!='),        
        (GRTR,  '>'),
        (LEQ,   '<='),
        (GEQ,   '>='),
        (ADD,   '\\+'), # + is special in regular expressions
        (SUB,   '-'),
        (LPAR,  '\\('), # ( is special in regular expressions
        (RPAR,  '\\)'), # ) is special in regular expressions
        (LCRL,  '{'), 
        (RCRL,  '}'), 
        (ID,    '[a-z]+'),
        (NUM,   '[0-9]+')
    ]