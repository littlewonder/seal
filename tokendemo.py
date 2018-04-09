import sys

# Token types
TOK_PRINT  = "print"
TOK_ID     = "id"
TOK_VAR    = "var"
TOK_INT    = "int"
TOK_FLOAT  = "float"
TOK_TYPE   = "type"
TOK_EQ     = "equal"
TOK_PLUS   = "+"
TOK_MINUS  = "-"
TOK_STAR   = "*"
TOK_SLASH  = "/"
TOK_LPAREN = "("
TOK_RPAREN = ")"
TOK_COLON  = ":"
TOK_WHILE  = "while"
TOK_DO     = "do"
TOK_DONE   = "done"
TOK_SEMI   = ";"
TOK_READ   = "read"



def error(msg):
    print("Error: " + msg)
    sys.exit(1)

def tok(ty, val):
    return { "toktype": ty, "value": val }


def lex(s):
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
    for line in toks:
        print(line)  

if __name__ == '__main__':
    main()