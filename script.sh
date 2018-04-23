seal () {
    if [ -z "$1" ]; then
        echo "none"
    else
        if [ "$1" = "demo.seal" ]; then
            python2 code_gen.py < demo.seal  > demo.c 
            gcc demo.c
            ./a.out
        fi
    fi
}
