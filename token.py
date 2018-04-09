import sys

# Token types
TOK_PRINT  = 0
TOK_ID     = 1
TOK_VAR    = 2
TOK_INT    = 3
TOK_FLOAT  = 4
TOK_TYPE   = 5
TOK_EQ     = 6
TOK_PLUS   = 7
TOK_MINUS  = 8
TOK_STAR   = 9
TOK_SLASH  = 10
TOK_LPAREN = 11
TOK_RPAREN = 12
TOK_COLON  = 13
TOK_WHILE  = 14
TOK_DO     = 15
TOK_DONE   = 16
TOK_SEMI   = 17
TOK_READ   = 18


def error(msg):
    print("Error: " + msg)
    sys.exit(1)

def tok(ty, val):
    return { "toktype": ty, "value": val }


def lex(s):
    """
    Input : a string representing a mini program
    Output: a list of tokens
    lex(s) will produce a sequence of tokens, which are dicts with two
    bindings: the type of the token (as defined above) and a semantic
    value.  The semantic value (also called lexeme) is a piece of
    information associated with the token, such as the name of an
    identifier or the value of an integer literal.  Some tokens, like
    the plus symbol, do not have an associated semantic value.
    Example:
    x = x + dx;
    =>
    { "toktype": TOK_ID   , "value": "x" }
    { "toktype": TOK_EQ   , "value": None }
    { "toktype": TOK_ID   , "value": "x" }
    { "toktype": TOK_PLUS , "value": None }
    { "toktype": TOK_ID   , "value": "dx" }
    { "toktype": TOK_SEMI , "value": None }
    alpha   ::= ['a'-'z'  'A'-'Z'  '_']
    digit   ::= ['0'-'9']
    alnum   ::= alpha | digit
    int     ::= digit+
    float   ::= digit+ '.' digit*
    keyword ::= "var" | "print" | "read" | "while" | "do" | "done" | "int" | "float"
    ident   ::= alpha alnum*
    """
    i = 0
    tokens = []
    while i < len(s):
        c = s[i]

        # Skip spaces
        if c.isspace():
            pass

        # Skip comments
        elif c == "#":
            while s[i] != "\n":
                i += 1

        # Operators and punctuation
        elif c == "=":
            tokens.append(tok(TOK_EQ, None))
        elif c == "+":
            tokens.append(tok(TOK_PLUS, None))
        elif c == "-":
            tokens.append(tok(TOK_MINUS, None))
        elif c == "*":
            tokens.append(tok(TOK_STAR, None))
        elif c == "/":
            tokens.append(tok(TOK_SLASH, None))
        elif c == "(":
            tokens.append(tok(TOK_LPAREN, None))
        elif c == ")":
            tokens.append(tok(TOK_RPAREN, None))
        elif c == ":":
            tokens.append(tok(TOK_COLON, None))
        elif c == ";":
            tokens.append(tok(TOK_SEMI, None))

        # Integer and float literals
        elif c.isdigit():
            num = ""
            while s[i].isdigit():
                num += s[i]
                i += 1
            if s[i] == ".":
                num += "."
                i += 1
                while s[i].isdigit():
                    num += s[i]
                    i += 1
                tokens.append(tok(TOK_FLOAT, float(num)))
            else:
                tokens.append(tok(TOK_INT, int(num)))
            i -= 1 # Read one char too many, readjust.

        # Identifiers and keywords
        elif c.isalpha() or c == "_":
            ident = ""
            while s[i].isalnum() or s[i] == "_":
                ident += s[i]
                i += 1
            i -= 1 # Read one char too many, readjust.
            if ident == "print":
                tokens.append(tok(TOK_PRINT, None))
            elif ident == "read":
                tokens.append(tok(TOK_READ, None))
            elif ident == "var":
                tokens.append(tok(TOK_VAR, None))
            elif ident == "while":
                tokens.append(tok(TOK_WHILE, None))
            elif ident == "do":
                tokens.append(tok(TOK_DO, None))
            elif ident == "done":
                tokens.append(tok(TOK_DONE, None))
            elif ident in ("int", "float"):
                tokens.append(tok(TOK_TYPE, ident))
            else:
                tokens.append(tok(TOK_ID, ident))
        else:
            error("invalid character: %r" % c)
        i += 1
    return tokens


def main():
    src = sys.stdin.read()
    toks = lex(src)    
    print(toks)  

if __name__ == '__main__':
    main()