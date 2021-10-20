A preprocessor for [brainfuck](https://en.wikipedia.org/wiki/Brainfuck) written in python. Makes the process of writing brainfuck (slightly) less painful

# Directives

| directive | description |
|----|------|
| `(+ n)` | insert `n` `+` characters |
| `(- n)` | insert `n` `-` characters |
| `(> n)` | insert `n` `>` characters |
| `(< n)` | insert `n` `<` characters |
| `(mv n)` | move the value at the pointer position to the current address + `n`|
| `(cp n)` | copy the value at the pointer position to the current address + `n`|
| `(if 'code')` | if the current value is not zero, execute the provided code |
| `(ifelse 'ifcode' 'elsecode' tmp_shift)` | if the current value is not zero, execute `ifcode` else execute `elsecode`. `tmp_shift` gives the shift at which to use a temporary value|

Parameters to directives do not need to be straight up literals like in the examples above, you can pass any arbitrary python expression as a parameter. For example:

```py
(+ ord('a'))
```

Increments the current position by the ascii representation of `a`

# Running

Simply run the provided `bfpp.py` script on the branifuck source file. This will output the pure brainfuck equivalent of your code.

```shell
./bfpp.py example.bf
```

# Todo

- Change `cp` directive to take the tmp byte location
- Use a CFG for parsing instead of regex in order to allow spaces in parameters
- Use a better format (non lisp) for directives



