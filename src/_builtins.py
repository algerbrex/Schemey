"""
builtins.py
----------------------------------------

An implementation of builtin procedures
and variables in Scheme.

"""

import operator as op
from functools import reduce
from .expressions import *
from .utils import get_number_of_params


class ProcedureError(Exception):
    pass


class Procedure:
    """
    A simple representation of procedures in Scheme.
    """

    def __init__(self, name, builtin_proc):
        self.name = name
        self.builtin_proc = builtin_proc

    def __repr__(self):
        return '#<Procedure {}>'.format(self.name)

    def apply(self, *args):
        argc = get_number_of_params(self.builtin_proc)
        if argc != 'positional' and argc != len(args):
            raise ProcedureError(
                'Procedure "{}" expected {} argument(s).'
                ' Got {} instead'.format(self.name, argc, len(args))
            )
        return self.builtin_proc(*args)


def check_type(expected_type, objs, msg):
    # sometimes `objs` is one object and not a tuple of arguments.
    # deal with theses cases by wrapping single objects in a list.
    objs = objs if isinstance(objs, tuple) else [objs]
    if any(not isinstance(obj, expected_type) for obj in objs):
        raise ProcedureError(msg)


def arith_op(op_func, unary_func):
    def op(*args):
        if len(args) == 1:
            return Number(unary_func(args[0].value))
        check_type(Number, args, "Expected numbers only")
        return Number(reduce(op_func, [el.value for el in args]))
    return op


def comp_op(op_func):
    def op(*args):
        it = iter(args)
        value = next(it)
        for element in it:
            if op_func(value.value, element.value):
                value = element
            else:
                return Boolean(False)
        return Boolean(True)
    return op


def builtin_list(*args):
    pair = Nil()
    for el in reversed(args):
        pair = Pair(el, pair)
    return pair


def builtin_cons(obj1, obj2):
    return Pair(obj1, obj2)


def builtin_car(pair):
    check_type(Pair, pair, "Expected pair or list.")
    if pair.first is None:
        raise ProcedureError("attempted car on empty list")
    return pair.first


def builtin_cdr(pair):
    check_type(Pair, pair, "Expected pair or list.")
    if pair.first is None:
        raise ProcedureError("attempted cdr on empty list")
    return pair.second


def builtin_cadr(pair):
    check_type(Pair, pair, "Expected pair of list")
    if pair.second.first is None:
        raise ProcedureError("attempted cadr on empty list")
    return pair.second.first


def builtin_caddr(pair):
    check_type(Pair, pair, "Expected pair of list")
    if pair.second.second.first is None:
        raise ProcedureError("attempted caddr on empty list")
    return pair.second.second.first


def builtin_set_car(pair, obj):
    check_type(Pair, pair, "Expected pair or list.")
    pair.first = obj
    return pair


def builtin_set_cdr(pair, obj):
    check_type(Pair, pair, "Expected pair or list.")
    pair.second = obj
    return pair


def builtin_string_length(string):
    check_type(String, string, "Expected string.")
    str_len = len(string.value)
    return Number(str_len)


def builtin_eqv(*args):
    left, right = args[0], args[1]
    if isinstance(left, Pair) and isinstance(right, Pair):
        return Boolean(id(left) == id(right))
    else:
        return Boolean(left == right)


def builtin_and(*args):
    for el in args:
        if el == Boolean(False):
            return el
    if len(args) > 0:
        return args[-1]
    else:
        return Boolean(True)


def builtin_or(*args):
    for el in args:
        if el == Boolean(True):
            return el
    if len(args) > 0:
        return args[-1]
    else:
        return Boolean(False)


def builtin_not(obj):
    if isinstance(obj, Boolean) and obj.value == False:
        return Boolean(True)
    else:
        return Boolean(False)


def builtin_quotient(a, b):
    return Number(a.value // b.value)


def builtin_mod(a, b):
    return Number(a.value % b.value)


def builtin_is_pair(obj):
    return Boolean(isinstance(obj, Pair))


def builtin_is_zero(number):
    return Boolean(number.value == 0)


def builtin_is_boolean(obj):
    return Boolean(isinstance(obj, Boolean))


def builtin_is_symbol(obj):
    return Boolean(isinstance(obj, Symbol))


def builtin_is_number(obj):
    return Boolean(isinstance(obj, Number))


def builtin_is_null(obj):
    return Boolean(isinstance(obj, Nil))


def builtin_is_string(obj):
    return Boolean(isinstance(obj, String))


builtin_map = {
    'eq?': builtin_eqv,
    'eqv?': builtin_eqv,
    'pair?': builtin_is_pair,
    'zero?': builtin_is_zero,
    'boolean?': builtin_is_boolean,
    'symbol?': builtin_is_symbol,
    'number?': builtin_is_number,
    'null?': builtin_is_null,
    'string?': builtin_is_string,

    '+': arith_op(op.add, lambda x: +x),
    '-': arith_op(op.sub, lambda x: -x),
    '*': arith_op(op.mul, lambda x: x),
    # divison and modulation always need exactly
    # two arguments. Because of this, we must implement
    # them as functions instead.
    'quotient': builtin_quotient,
    'modulo': builtin_mod,

    '=': comp_op(op.eq),
    '>': comp_op(op.gt),
    '<': comp_op(op.lt),
    '>=': comp_op(op.ge),
    '<=': comp_op(op.le),
    'and': builtin_and,
    'or': builtin_or,
    'not': builtin_not,

    'list': builtin_list,
    'cons': builtin_cons,
    'car': builtin_car,
    'cdr': builtin_cdr,
    'cadr': builtin_cadr,
    'caddr': builtin_caddr,
    'set-car!': builtin_set_car,
    'set-cdr!': builtin_set_cdr,

    'string-length': builtin_string_length,
}
