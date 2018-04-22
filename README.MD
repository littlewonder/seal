# Parser

    Input : a list of tokens
    Output: a list of statement nodes
    parse(toks) is a predictive, recursive-descent parser that will
    return a list of AST nodes (declarations and statements) from the
    token stream computer by lex() above.  We parse the tokens
    according to the following grammar.  Every non-terminal (left-hand
    side of a ::=) has its own local function definition.
        program  ::=  decls stmts
        decls    ::=  decl decls
                   |  ε
        decl     ::=  'var' ident ':' type ';'
        stmts    ::=  stmt stmts
                   |  ε
        stmt     ::=  ident '=' expr ';'
                   |  'read' ident ';'
                   |  'print' expr ';'
                   |  'while' expr 'do' stmts 'done'
        expr     ::=  term { '+' expr }
                   |  term { '-' expr }
                   |  term
        term     ::=  factor { '*' term }
                   |  factor { '-' term }
                   |  factor
        factor   ::=  '(' expr ')'
                   |  ident
                   |  int
                   |  float
    The AST nodes are represented with dicts as follows:
    - Declarations
        - var id: type         : { "nodetype": AST_DECL, "id": id, "type": type }
    - Statements
        - id = expr            : { "nodetype": AST_ASSIGN, "lhs": id, "rhs": expr }
        - print expr           : { "nodetype": AST_PRINT, "expr": expr }
        - read id              : { "nodetype": AST_READ, "id": id }
        - while e do stmts done: { "nodetype": AST_WHILE, "expr": e, "body": stmts }
    - Expressions
        - int                  : { "nodetype": AST_INT, "value": int }
        - float                : { "nodetype": AST_FLOAT, "value": float }
        - id                   : { "nodetype": AST_ID, "name": id }
        - e1 + e2              : { "nodetype": AST_BINOP, op: "+", "lhs": e1, "rhs": e2 }
    For example, here is a simple statement and its AST representation:
        x = 3 + y
        {
          "nodetype": AST_ASSIGN,
          "lhs": "x",
          "rhs": {
            "nodetype": AST_BINOP,
            "op": "+",
            "lhs": { "nodetype": AST_INT, "value": 3 },
            "rhs": { "nodetype": AST_ID, "name": "y" }
          }
        }


# Tokeniser

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
    
# Symbol Table

    Input : the AST of a mini program
    Output: a dictionary mapping variable names to types

    This procedure iterates over the declarations and adds them to a
    symbol table (here, a dictionary that maps variable names to their
    declared type).  If a variable is declared more than once, we
    report an error.
