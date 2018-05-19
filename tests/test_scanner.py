from ..scanner import Scanner
from ..token import TokenType, Token

def test_parens():
    source = '()'
    expected_output = [
        Token(TokenType.LEFT_PAREN, '', None, 1),
        Token(TokenType.RIGHT_PAREN, '', None, 1),
        Token(TokenType.EOF, '', None, 1),
    ]

    tokens = Scanner(source).scan_tokens()

    assert expected_output == tokens

def test_singleline_comments():
    source = "/ //this is a test"
    expected_output = [
        Token(TokenType.SLASH, '', None, 1),
        Token(TokenType.EOF, '', None, 1),
    ]

    tokens = Scanner(source).scan_tokens()

    assert expected_output == tokens

def test_complex():

    source = """
(thing = 23.7) // comment
/* multiline
comment */
23 >= test
"""

    expected_output = [
        Token(TokenType.LEFT_PAREN, '', None, 2),
        Token(TokenType.IDENTIFIER, '', None, 2),
        Token(TokenType.EQUAL, '', None, 2),
        Token(TokenType.NUMBER, '23.7', 23.7, 2),
        Token(TokenType.RIGHT_PAREN, '', None, 2),
        Token(TokenType.NUMBER, '23', 23.0, 5),
        Token(TokenType.GREATER_EQUAL, '', None, 5),
        Token(TokenType.IDENTIFIER, '', None, 5),
        Token(TokenType.EOF, '', None, 6),
    ]

    tokens = Scanner(source).scan_tokens()

    assert expected_output == tokens
