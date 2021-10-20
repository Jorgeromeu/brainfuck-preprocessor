#!/usr/bin/env python3

import sys
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="The brainfuck++ file to preprocess", type=str)
parser.add_argument("-o", "--out", help="File to output the brainfuck", type=str)
args = parser.parse_args()

inputfile = open(args.file)

def shft(n):
    if n > 0:
        return ''.join('>' for _ in range(n))
    elif n < 0:
        return ''.join('<' for _ in range(-n))
    else:
        return ''

def inc(n):
    if n > 0:
        return ''.join('+' for _ in range(n))
    elif n < 0:
        return ''.join('-' for _ in range(-n))
    else:
        return ''


def argument_validator(directive, args: list, expected: list[type]):
    arg_types = list(map(lambda e: type(e), args))
    if arg_types != expected:
        sys.stderr.write(f'Invalid arguments: directive "{directive}" expects arguments of type {expected}. You gave: {arg_types}')

def stateful_if(args):
    """
    conditionally evaluate the provided code
    in doing this, the current cell is wiped
    """
    body = str(args[0])
    return f'[{body}[-]]'

def stateful_ifelse(args):
    """
    conditionally evaluate the provided code
    - in doing this, the current cell is wiped
    - params: ifbody, elsebody, tmp_shift
    """
    ifbody, elsebody, tmp = args[0], args[1], int(args[2])

    code = f'{shft(tmp)}[-]+{shft(-tmp)}' # set else flag
    code += f'[{ifbody}[-]{shft(tmp)}-{shft(-tmp)}]' # if block
    code += f'{shft(tmp)}' # go to else flag
    code += f'[{shft(-tmp)}{elsebody}-]' # return to A and execute else block
    code += f'{shft(-tmp)}' # return to A

    return code

def print_str(args):
    string = args[0]
    code = ''
    for char in string:
        code += inc(ord(char))
        code += '.'
        code += inc(-ord(char))
    return code

def read_bytes(args):
    n = int(args[0])
    code = []
    for _ in range(n):
        code.append(',>')
    return ''.join(code)

def move(args):
    """
    move current value up to the cell "n" positions away
    - pointer stays in same position
    """
    n = int(args[0])
    code = f'[-{shft(n)}+{shft(n)}]'
    return code

def copy(args):
    """
    copy current value to to the cell n positions away
    - pointer stays in same position
    - requires the cell at n+1 to be free
    """
    n = int(args[0])
    code = f'[-{shft(n)}+>+{shft(n+1)}]' # double move
    code += f'{shft(n+1)}[-{shft(n+1)}+{shft(n+1)}]' # move back
    code += f'{shft(n+1)}' # restore pointer
    return code

def make_arr(args):
    lst = args[0]
    code = '>'
    for val in lst:
        code += f'{inc(val)}>'
    code += shft(-len(lst)-1)
    return code

callbacks = {
    '+': lambda args: inc(args[0]),
    '-': lambda args: inc(-args[0]),
    '>': lambda args: shft(args[0]),
    '<': lambda args: shft(-args[0]),
    'print': print_str,
    'read_bytes': read_bytes,
    'mv': move,
    'cp': copy,
    'if': stateful_if,
    'ifelse': stateful_ifelse,
    'make_arr': make_arr,
    'arr_end_bd': lambda args: '>[>]',
    'arr_beg_bd': lambda args: '<[<]',
    'arr_end_in': lambda args: '[>]<',
    'arr_beg_in': lambda args: '>[<]',
}


def parse_directive(directive: str):
    parsed = directive[1:-1].split(' ')
    identifier = parsed[0]
    args = parsed[1:]
    args = list(map(lambda e: eval(e), args))
    return (identifier, args)

for line in inputfile.readlines():
    match = re.search(r'\(.*\)', line)

    if match:
        identifier, args = parse_directive(match.group())

        try:
            new_txt = callbacks[identifier](args)
        except KeyError:
            sys.stderr.write(f'bfPP: directive "{identifier}" does not exist\n')

        line = re.sub(r'\(.*\)', new_txt, line)

    print(line, end='')
