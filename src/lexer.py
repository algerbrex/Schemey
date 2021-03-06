"""
lexer.py
----------------------------------------

A simple lexer based upon the "maximal munch" rule.
Because of this, the lexer is not generic and must
be created anew for each specific language.

"""

from collections import namedtuple
from ._builtins import builtin_map

ADDITIONAL_BUILTIN_CHARS = {'?', '!', '.'}
GARBAGE_CHARS = {' ', '\n', '\t', '\r'}
TRUE_OR_FALSE_CHARS = {'t', 'f'}
COMMENT_CHAR = ';'

# Sometimes we need to return the current position
# the lexer is on to raise an appropriate error. That
# is what this class holds. Whenever there is an error,
# an instance is returned to the parser.
Error = namedtuple('Error', 'pos')


def is_identifier(char):
    """
    Test if `char` is a valid Scheme identifier.
    """
    return char.isalnum() or char in builtin_map.keys() or char in ADDITIONAL_BUILTIN_CHARS


class Token:
    """
    A simple Token structure.
    Contains the token type, value,
    and the position of the token.
    """

    def __init__(self, token_type, val, pos):
        # copy the attributes of the Character object
        # to this class instance.
        self.token_type = token_type
        self.val = val
        self.pos = pos

    def __str__(self):
        return "{}({}) at {}".format(self.token_type, self.val, self.pos)


class TokenTypes:
    """
    A Structure for each possible type
    of token.
    """
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    QUOTE = 'QUOTE'


class Lexer:
    """
    A simple lexer based upon the "maximal munch" rule.
    """

    def __init__(self, buffer):
        """
        Initialize the lexer with buffer as input.
        """
        self.buffer = buffer
        self.pos = 0

    def next_token(self):
        """
        Return the next token(Which is a token object.)
        found in the input buffer. None is returned if we've
        reached the end of the buffer.
        If a lexing error occurs(The current character
        is not known), a LexerError is raised.
        """
        char = self._get_char()

        # Continue to skip past garbage characters.
        while char in GARBAGE_CHARS or char == COMMENT_CHAR:
            self._skip_comments()
            self._skip_whitespace()
            char = self._get_char()

        if char is None:
            return None
        elif char == '#' and self._get_char(self.pos + 1) in TRUE_OR_FALSE_CHARS:
            return self._process_boolean()
        elif char.isdigit():
            return self._process_number()
        elif char == '"':
            return self._process_string()
        elif is_identifier(char):
            return self._process_identifier()
        elif char == '(':
            return self._process_lparen()
        elif char == ')':
            return self._process_rparen()
        elif char == "'":
            return self._process_quote()
        else:
            return Error(self.pos)

    def _skip_whitespace(self):
        """
        Skip past all characters which are whitespace.
        """
        while self._get_char():
            if self._get_char() in GARBAGE_CHARS:
                self.pos += 1
            else:
                break

    def _skip_comments(self):
        """
        Skip past all characters in the comment.
        """
        if self._get_char() == COMMENT_CHAR:
            while self._get_char() and self._get_char() != '\n':
                self.pos += 1

    def _process_boolean(self):
        """
        Construct a boolean Token.
        """
        retval = Token(TokenTypes.BOOLEAN, self.buffer[self.pos:self.pos + 2], self.pos)
        self.pos += 2
        return retval

    def _process_number(self):
        """
        Construct a numeric Token.
        """
        endpos = self.pos + 1
        while self._get_char(endpos) and self._get_char(endpos).isdigit():
            endpos += 1
        retval = Token(TokenTypes.NUMBER, self.buffer[self.pos:endpos], self.pos)
        self.pos = endpos
        return retval

    def _process_string(self):
        """
        Construct a string token.
        """
        endpos = self.pos + 1
        while self._get_char(endpos) != '"':
            # If we've reached EOF, or hit a newline then
            # this is an unterminated string. Return an error
            # with the position of where the string began.
            if not self._get_char(endpos) or self._get_char(endpos) == '\n':
                return Error(self.pos)
            endpos += 1
        retval = Token(TokenTypes.STRING, self.buffer[self.pos + 1:endpos], self.pos)
        self.pos = endpos + 1
        return retval

    def _process_identifier(self):
        """
        Construct an identifier Token.
        """
        endpos = self.pos + 1
        while self._get_char(endpos) and is_identifier(self._get_char(endpos)):
            endpos += 1
        retval = Token(TokenTypes.IDENTIFIER, self.buffer[self.pos:endpos], self.pos)
        self.pos = endpos
        return retval

    def _process_lparen(self):
        """
        Construct a left parenthesis Token.
        """
        retval = Token(TokenTypes.LPAREN, self.buffer[self.pos], self.pos)
        self.pos += 1
        return retval

    def _process_rparen(self):
        """
        Construct a right parenthesis Token.
        """
        retval = Token(TokenTypes.RPAREN, self.buffer[self.pos], self.pos)
        self.pos += 1
        return retval

    def _process_quote(self):
        """
        Construct a quote Token.
        """
        retval = Token(TokenTypes.QUOTE, self.buffer[self.pos], self.pos)
        self.pos += 1
        return retval

    def _get_char(self, pos=None):
        """
        Try and get the next character from the buffer.
        If an IndexError is raised, return None.
        """
        offset = pos or self.pos
        try:
            return self.buffer[offset]
        except IndexError:
            return None
