from token import lex
from parser import parse
from symbol_table import build_symtab
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

def astnode(nodetype, **args):
    return dict(nodetype=nodetype, **args)

def typecheck(ast, symtab):
    def check_stmt(stmt):
        if stmt["nodetype"] == AST_PRINT:
            typed_expr = check_expr(stmt["expr"])
            return astnode(AST_PRINT, expr=typed_expr)
        elif stmt["nodetype"] == AST_READ:
            return astnode(AST_READ, id=stmt["id"])
        elif stmt["nodetype"] == AST_ASSIGN:
            typed_rhs = check_expr(stmt["rhs"])
            if typed_rhs["type"] == symtab[stmt["lhs"]]:
                return astnode(AST_ASSIGN, lhs=stmt["lhs"], rhs=typed_rhs)
            else:
                error("expected %s, got %s" % (symtab[stmt["lhs"]], typed_rhs["type"]))
        elif stmt["nodetype"] == AST_WHILE:
            typed_expr = check_expr(stmt["expr"])
            if typed_expr["type"] != "int":
                error("loop condition must be an int")
            typed_body = [check_stmt(body_stmt) for body_stmt in stmt["body"]]
            return astnode(AST_WHILE, expr=typed_expr, body=typed_body)

    def check_expr(expr):
        if expr["nodetype"] == AST_INT:
            return astnode(AST_INT, value=expr["value"], type="int")
        elif expr["nodetype"] == AST_FLOAT:
            return astnode(AST_FLOAT, value=expr["value"], type="float")
        elif expr["nodetype"] == AST_ID:
            if expr["name"] not in symtab:
                error("undeclared variable: %s" % expr["name"])
            return astnode(AST_ID, name=expr["name"], type=symtab[expr["name"]])
        elif expr["nodetype"] == AST_BINOP:
            typed_e1 = check_expr(expr["lhs"])
            typed_e2 = check_expr(expr["rhs"])
            if typed_e1["type"] == typed_e2["type"]:
                return astnode(AST_BINOP, op=expr["op"], lhs=typed_e1, rhs=typed_e2, type=typed_e1["type"])
            else:
                error("operands must have the same type")

    updated_stmts = []
    for stmt in ast["stmts"]:
        updated_stmts.append(check_stmt(stmt))
    return { "decls": ast["decls"], "stmts": updated_stmts }

def main():
    src = sys.stdin.read()
    toks = lex(src)
    #printToken(toks)                   # source -> tokens
    ast = parse(toks)
    sym = build_symtab(ast)
    type_check = typecheck(ast,sym)
    # print type_check

if __name__ == "__main__":
    main()