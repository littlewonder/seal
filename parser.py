# -*- coding: utf-8 -*-
from token import lex
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


def astnode(nodetype, **args):
    return dict(nodetype=nodetype, **args)

def parse(toks):
    
    def consume(tok_type):
        if tok_type == toks[0]["toktype"]:
            t = toks.pop(0)
            return t
        else:
            error("expected %d, found %d" % (tok_type, toks[0]["toktype"]))

    def peek():
        if toks:
            return toks[0]["toktype"]
        else:
            return None

    def decls():
        decls = []
        while peek() == TOK_VAR:
            decls.append(decl())
        return decls

    def decl():
        if peek() == TOK_VAR:
            consume(TOK_VAR)
            id = consume(TOK_ID)
            consume(TOK_COLON)
            ty = consume(TOK_TYPE)
            consume(TOK_SEMI)
            return astnode(AST_DECL, id=id["value"], type=ty["value"])
        else:
            error("not a valid declaration")

    def stmts():
        stmts = []
        while peek() in (TOK_PRINT, TOK_READ, TOK_ID, TOK_WHILE):
            stmts.append(stmt())
        return stmts

    def stmt():
        next_tok = peek()
        if next_tok == TOK_ID:
            id = consume(TOK_ID)
            consume(TOK_EQ)
            e = expr()
            consume(TOK_SEMI)
            return astnode(AST_ASSIGN, lhs=id["value"], rhs=e)
        elif next_tok == TOK_PRINT:
            consume(TOK_PRINT)
            e = expr()
            consume(TOK_SEMI)
            return astnode(AST_PRINT, expr=e)
        elif next_tok == TOK_READ:
            consume(TOK_READ)
            id = consume(TOK_ID)
            consume(TOK_SEMI)
            return astnode(AST_READ, id=id)
        elif next_tok == TOK_WHILE:
            consume(TOK_WHILE)
            e = expr()
            consume(TOK_DO)
            body = stmts()
            consume(TOK_DONE)
            return astnode(AST_WHILE, expr=e, body=body)
        else:
            error("illegal statement")

    def expr():
        t = term()
        next_tok = peek()
        while next_tok in (TOK_PLUS, TOK_MINUS):
            if next_tok == TOK_PLUS:
                consume(TOK_PLUS)
                t2 = term()
                t = astnode(AST_BINOP, op="+", lhs=t, rhs=t2)
            elif next_tok == TOK_MINUS:
                consume(TOK_MINUS)
                t2 = term()
                t = astnode(AST_BINOP, op="-", lhs=t, rhs=t2)
            next_tok = peek()
        return t

    def term():
        f = factor()
        next_tok = peek()
        while next_tok in (TOK_STAR, TOK_SLASH):
            if next_tok == TOK_STAR:
                consume(TOK_STAR)
                f2 = factor()
                f = astnode(AST_BINOP, op="*", lhs=f, rhs=f2)
            elif next_tok == TOK_SLASH:
                consume(TOK_SLASH)
                f2 = factor()
                f = astnode(AST_BINOP, op="/", lhs=f, rhs=f2)
            next_tok = peek()
        return f

    def factor():
        next_tok = peek()
        if next_tok == TOK_LPAREN:
            consume(TOK_LPAREN)
            e = expr()
            consume(TOK_RPAREN)
            return e
        elif next_tok == TOK_INT:
            tok = consume(TOK_INT)
            return astnode(AST_INT, value=tok["value"])
        elif next_tok == TOK_FLOAT:
            tok = consume(TOK_FLOAT)
            return astnode(AST_FLOAT, value=tok["value"])
        elif next_tok == TOK_ID:
            tok = consume(TOK_ID)
            return astnode(AST_ID, name=tok["value"])
        else:
            error("illegal token %d" % next_tok)

    ds = decls()
    sts = stmts()
    return {
        "decls": ds,
        "stmts": sts,
    }

def main():
    src = sys.stdin.read()
    toks = lex(src)
    #printToken(toks)                   # source -> tokens
    ast = parse(toks)
    printAST(ast)
        
def printAST(ast):
    print('\n')
    print('AST')                    # tokens -> AST
    for idx in ast:
        print(idx)
        print('-------------------')
        for i in ast[idx]:
            print(i)

def printToken(toks):
    print('Tokens')                    # tokens -> AST
    print('-------------------')
    for elm in toks:
        print(elm)
    


if __name__ == "__main__":
    main()