"""
Scanner and Tokens for Small
"""

__author__ = "Campbell Mercer-Butcher"

import re
import sys
from token import Token

class Scanner:
    '''Matches tokens through out provided file'''

    def __init__(self, input_file):
        '''Reads the whole input_file'''
        # source code
        self.input_string = input_file.read()
        # Current index in source
        self.current_char_index = 0
        # Most recently matched token and sub string
        self.current_token = self.get_token()

    def skip_white_space(self):
        '''Consumes all characters in input_string up to the next
           non-white-space character.'''
        try:
            #loop till there is no more white spaces
            while True:
                if self.input_string[self.current_char_index] in [' ','\t','\n']:
                    self.current_char_index += 1
                else:
                    break
        except:
            pass

    def no_token(self):
        '''Raise error if the input cannot be matched to a token.'''
        raise LexicalError(self.input_string[self.current_char_index:])
        

    def get_token(self):
        '''Returns the next token and the part of input_string it matched.'''
        self.skip_white_space()
        # find the longest prefix of input_string that matches a token
        token, longest = None, ''
        for (t, r) in Token.token_regexp:
            match = re.match(r, self.input_string[self.current_char_index:])
            if match and match.end() > len(longest):
                token, longest = t, match.group()
                
        if token == None and self.current_char_index+1 < len(self.input_string):
            self.no_token()
        # consume the token by moving the index to the end of the matched part
        self.current_char_index += len(longest)
        return (token, longest)

    def lookahead(self):
        '''Returns the next token without consuming it'''
        return self.current_token[0]

    def unexpected_token(self, found_token, expected_tokens):
        '''Stop execution because an unexpected token was found'''
        raise SyntaxError(repr(sorted(expected_tokens)), repr(found_token))

    def consume(self, *expected_tokens):
        '''Returns the next token and consumes it'''
        #if token isnt in the expected tokens raise an error
        if self.current_token[0] in expected_tokens:
            old_token = self.current_token
            self.current_token = self.get_token()
            if old_token[0] in [Token.NUM, Token.ID]:
                return old_token[0], old_token[1]
            else:
                return old_token[0]
        else:
            self.unexpected_token(self.current_token[0],expected_tokens)

class ScannerError(Exception):
    """Base exception for errors raised by Scanner"""
    def __init__(self, msg=None):
        if msg is None:
            msg = "An error occured in the Scanner"
        super().__init__(msg)

class LexicalError(ScannerError):
    """Token cant be matched"""
    def __init__(self, token):
        msg = "No token found at the start of {0}".format(token)
        super().__init__(msg)

class SyntaxError(ScannerError):
    """Unexpected token"""
    def __init__(self, expected, found):
        msg = "token in {0} expected but {1} found".format(expected, found)
        super().__init__(msg)


#Test Code

# # Initialise scanner.

# scanner = Scanner(sys.stdin)

# # Show all tokens in the input.

# token = scanner.lookahead()
# while token != None:
#     if token in [Token.NUM, Token.ID]:
#         token, value = scanner.consume(token)
#         print(token, value)
#     else:
#         print(scanner.consume(token))
#     token = scanner.lookahead()
    

