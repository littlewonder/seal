# -*- coding: utf-8 -*-
from token import lex
from parser import parse
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

# AST nodes
AST_DECL   = 0
AST_ASSIGN = 1
AST_PRINT  = 2
AST_INT    = 3
AST_FLOAT  = 4
AST_ID     = 5
AST_BINOP  = 6
AST_WHILE  = 7
AST_READ   = 8

def error(msg):
    print("Error: " + msg)
    sys.exit(1)

def build_symtab(ast):

    symtab = {}
    for decl in ast["decls"]:
        # print decl["id"]
        if decl["id"] in symtab:
            error("%s is already declared" % decl["id"])
        else:
            symtab[decl["id"]] = decl["type"]
    return symtab


def main():
    src = sys.stdin.read()
    toks = lex(src)
    #printToken(toks)                   # source -> tokens
    ast = parse(toks)
    sym = build_symtab(ast)
    print("\n <------Symbol Table -------->\n")
    print("Scope : Global\n")
    print("Symbol\tType")
    for keys,values in sym.items():
        print("{}\t{}".format(keys,values))
    # print sym

if __name__ == "__main__":
    main()