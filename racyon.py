"""
A RExp is one of:
    - Number
    - Variable
    - ['quote' SExp]
    - ['lambda' Parameters RExp]
    - ['if' RExp RExp RExp]
    - ['define' Variable RExp]
    - ['define-struct' Variable SExp]
    - [RExp RExp ...]
A Variable is a String
A Value is one of:
    - SExp
    - Procedure
A Procedure is one of:
    - pythOP
    - closure
A pythOP is a pythOP(handler=[ListOf Value]->Value)
A closure is a closure([ListOf Variables], RExp, Env)
An environment is a dictionary mapping from a Variable to a Value
"""

import collections
import operator
import re
import racket_functions

pythOP = collections.namedtuple("pythOP", "handler")
closure = collections.namedtuple("closure", "params body env")

topLevelEnv = { "+": operator.add,
                "-": operator.sub,
                "/": operator.truediv,
                "*": operator.mul,
                "or": racket_functions.racket_or,
                "and": racket_functions.racket_and,
                "equal?": operator.eq,
                ">": operator.gt,
                "<": operator.lt,
                ">=": operator.ge,
                "<=": operator.le,
                "list": racket_functions.racket_list,
                "cons": racket_functions.racket_cons,
                "empty?": racket_functions.racket_empty_huh,
                "empty": [],
                "first": racket_functions.racket_first,
                "second": racket_functions.racket_second,
                "third": racket_functions.racket_third,
                "rest": racket_functions.racket_rest,
                "#true": True,
                "#false": False,
                "map": racket_functions.racket_map,
                "filter": racket_functions.racket_filter,
                "foldr": racket_functions.racket_foldr,
                "foldl": racket_functions.racket_foldl,
                "odd?": lambda x: x%2==1,
                "even?": lambda x: x%2==0,}

def eval(rexp, env):
    # If it is a number, then return that
    if isinstance(rexp, (int, float)):
        return rexp
    # If it is a string aka a variable, then look it up in the environment and return that
    if isinstance(rexp, str):
        return env[rexp]
    if rexp[0] == 'quote':
        return rexp[2]
    if rexp[0] == 'if':
        if eval(rexp[1], env):
            return eval(rexp[2], env)
        else:
            return eval(rexp[3], env)
    if rexp[0] == 'lambda':
        return closure(rexp[1], rexp[2], env)
    if rexp[0] == 'define-struct':
        nt=racket_functions.racket_make_struct(rexp[1:])
        env["make-"+rexp[1]] = lambda *args: nt(*args)
        for index,id in enumerate(rexp[2]):
            env[rexp[1]+"-"+id] = racket_functions.racket_access_struct(index)
        env[rexp[1]+"?"] = racket_functions.racket_struct_huh(nt)
        return
    if rexp[0] == 'define':
        env[rexp[1]] = eval(rexp[2], env)
    else:
        functionValue = eval(rexp[0], env)
        argsValue = [eval(a, env) for a in rexp[1:]]
        return apply(functionValue, argsValue)

def apply(function, args):
    if type(function) is closure:
        params = function.params
        body = function.body
        env = function.env
        for param,arg in zip(params, args):
            env[param] = arg
        return eval(body, env)
    else:
        return function(*args)

def parseAtom(strRexp):
    try:
        return int(strRexp)
    except:
        try:
            return float(strRexp)
        except:
            return strRexp

def parseRExpr(split):
    first = split.pop(0)
    if '(' == first:
        expr = []
        while split[0] != ')':
            expr.append(parseRExpr(split))
        split.pop(0)
        return expr
    else:
        return parseAtom(first)

def run(strRexp):
    strRexp = strRexp.lstrip().rstrip()
    split = ' '.join(re.split("(\(|\)|\ )", strRexp)).split()
    split = parseRExpr(split)
    return eval(split, topLevelEnv)

if __name__ == "__main__":
    while True:
        print(run(input(">")))
