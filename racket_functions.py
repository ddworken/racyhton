from collections import namedtuple
from functools import reduce

def racket_list(*args):
    return list(args)

def racket_cons(first, rest):
    rest.insert(0,first)
    return rest

def racket_empty_huh(list):
    return not bool(list)

def racket_or(*args):
    return any(args)

def racket_and(*args):
    return all(args)

def racket_first(list):
    return list[0]

def racket_second(list):
    return list[1]

def racket_third(list):
    return list[2]

def racket_rest(list):
    return list[1:]

def racket_make_struct(args):
    arg = ' '.join(args[1])
    return namedtuple(args[0], arg)

def racket_access_struct(index):
    return lambda nt: nt[index]

def racket_struct_huh(nt):
    return lambda int: isinstance(int, nt)

def racket_map(function, list):
    return [function(x) for x in list]

def racket_filter(function, lst):
    return list(filter(function, lst))

def racket_foldl(function, base, lst):
    return reduce(function, lst, base)

def racket_foldr(function, base, lst):
    acc = base
    for elem in lst[::-1]:
        acc = function(elem, acc)
    return acc
