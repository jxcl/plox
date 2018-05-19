from .token import TokenType, Token, RESERVED_KEYWORDS

class Scanner:
    def __init__(self, source):
        self.errors = []

        self.source = source
        self.token_list = []

        self.start = 0
        self.current = 0
        self.line = 1

    def error(self, line, message):
        self.errors.append((line, "", message))

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()

        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)

        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            elif self.match('*'):
                self.multiline_comment()
            else:
                self.add_token(TokenType.SLASH)
        elif c in [' ', '\r', '\t']:
            pass
        elif c == '\n':
            self.line += 1

        elif c == '"':
            self.string()

        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()

        else:
            self.error(self.line, "Unexpected character: {}".format(c))

    def multiline_comment(self):
        while (
                self.peek() != '*' and
                self.peek_next() != '/' and
                not self.is_at_end()
        ):
            if self.peek() == '\n':
                self.line += 1

            self.advance()

        if self.is_at_end():
            self.error(self.line, "Unterminated multiline comment")
            return

        # consume trailing */
        self.advance()
        self.advance()

    def is_alpha(self, c):
        return (
            ('a' <= c <= 'z') or
            ('A' <= c <= 'Z') or
            c == '_'
        )

    def is_digit(self, c):
        return '0' <= c <= '9'

    def is_alphanumeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        name = self.source[self.start:self.current]

        if name in RESERVED_KEYWORDS.keys():
            self.add_token(RESERVED_KEYWORDS[name])
        else:
            self.add_token(TokenType.IDENTIFIER)


    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(
            TokenType.NUMBER,
            float(self.source[self.start:self.current])
        )


    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error(self.line, "Unterminated string")
            return

        # consume the closing "
        self.advance()

        # Trim surrounding quote marks
        value = self.source[self.start + 1:self.current - 1]

        self.add_token(TokenType.STRING, value)

    def peek(self):
        if self.is_at_end():
            return '\0'

        return self.source[self.current]

    def peek_next(self):
        if (self.current + 1) > len(self.source):
            return '\0'

        return self.source[self.current + 1]

    def match(self, expected):
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal=None):
        text = ''

        if literal is not None:
            text = self.source[self.start:self.current]

        self.token_list.append(Token(token_type, text, literal, self.line))

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.token_list.append(Token(TokenType.EOF, '', None, self.line))
        return self.token_list
