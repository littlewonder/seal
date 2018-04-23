from token import lex
from parser import parse
from symbol_table import build_symtab
from typecheck import typecheck
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

curr_tmp = 0
def codegen(ast, symtab):
    """
    Input : the AST and symbol table of a mini program
    Output: an equivalent C program

    codegen(ast) will generate code for our Minilang program.  The code
    is clearly not optimal, nor even really human readable, however it
    is (a) correct, and (b) translated easily.

    For expressions, we pass the expression to translate, and
    gen_expr() prints the code for generating the expression
    and returns the name of the variable in which
    the result is stored.

    The new_temp() function creates a new temporary variable for every
    time it's called.

    A typical code generator would return a structure that could then
    be manipulated for analysis and optimization.
    """
    def new_temp():
        """Return a new, unique temporary variable name."""
        global curr_tmp
        curr_tmp += 1
        return "t_" + str(curr_tmp)

    def gen_decl(decl):
        print("%s %s;" % (decl["type"], decl["id"]))

    def gen_stmt(stmt):
        if stmt["nodetype"] == AST_ASSIGN:
            if stmt["lhs"] not in symtab:
                error("undeclared variable: %s" % stmt["lhs"])
            expr_loc = gen_expr(stmt["rhs"])
            print("%s = %s;" % (stmt["lhs"], expr_loc))
        elif stmt["nodetype"] == AST_PRINT:
            expr_loc = gen_expr(stmt["expr"])
            if stmt["expr"]["type"] == "int":
                flag = "d"
            else:
                flag = "f"
            print('printf("%%%s\\n", %s);' % (flag, expr_loc))
        elif stmt["nodetype"] == AST_READ:
            id = stmt["id"]["value"]
            if symtab[id] == "int":
                flag = "d"
            else:
                flag = "f"
            print('scanf("%%%s", &%s);' % (flag, id))
        elif stmt["nodetype"] == AST_WHILE:
            expr_loc = gen_expr(stmt["expr"])
            print("while (%s) { " % expr_loc)
            for body_stmt in stmt["body"]:
                gen_stmt(body_stmt)
            gen_expr(stmt["expr"], expr_loc)
            print("}")

    def gen_expr(expr, loc_name=None):
        if expr["nodetype"] in (AST_INT, AST_FLOAT):
            loc = loc_name or new_temp()
            print("%s %s = %s;" % (expr["type"], loc, expr["value"]))
            return loc
        elif expr["nodetype"] == AST_ID:
            return expr["name"]
        elif expr["nodetype"] == AST_BINOP:
            lhs_loc = gen_expr(expr["lhs"])
            rhs_loc = gen_expr(expr["rhs"])
            loc = new_temp()
            print("%s %s = %s %s %s;" % (expr["type"], loc, lhs_loc, expr["op"], rhs_loc))
            return loc

    # Add the usual C headers and main declaration.
    print("#include <stdio.h>")
    print("int main(void) {")

    # Add the variable declarations at the beginning of main.
    for decl in ast["decls"]:
        gen_decl(decl)

    # Add the C statements to the main function.
    for stmt in ast["stmts"]:
        gen_stmt(stmt)

    print("}")

def main():
    src = sys.stdin.read()
    toks = lex(src)                      # source -> tokens
    ast = parse(toks)                    # tokens -> AST
    symtab = build_symtab(ast)           # AST -> symbol table
    typed_ast = typecheck(ast, symtab)   # AST * symbol table -> Typed AST
    codegen(typed_ast, symtab)  # Typed AST * symbol table -> C code


if __name__ == "__main__":
    main()