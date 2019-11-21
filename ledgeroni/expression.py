import re
from collections import deque

from ledgeroni.query import RegexQuery, Or, Not, And, PayeeQuery

TOKEN_REGEX = re.compile(r'(?P<token>\(|\)|@|[^\s\(\)\@]+)')

def tokenize_expression(expr_str):
    expr_str = expr_str.lstrip()
    match = TOKEN_REGEX.match(expr_str)
    while match is not None:
        token = match.group('token')
        yield token
        expr_str = expr_str[len(token):].lstrip()
        match = TOKEN_REGEX.match(expr_str)


PRECEDENCE = {'and': 1, 'or': 1, 'not': 2, '@': 2, 'payee': 3, '(': 0}

def build_postfix_expression(expr_str):
    operator_stack = []
    output = deque()
    last_was_expr = False
    for token in tokenize_expression(expr_str):
        if token == '(':
            if last_was_expr:
                flush_op_stack('or', operator_stack, output)
                operator_stack.append('or')
            operator_stack.append(token)
        elif token == ')':
            while operator_stack:
                op = operator_stack.pop()
                if op == '(':
                    break
                output.append(op)
            if op != '(':
                raise ValueError
        elif token in ('and', 'or', 'not', '@', 'payee'):
            flush_op_stack(token, operator_stack, output)
            operator_stack.append(token)
        else:
            if last_was_expr:
                flush_op_stack('or', operator_stack, output)
                operator_stack.append('or')
            output.append(token)

        last_was_expr = token not in PRECEDENCE.keys()

    output += list(operator_stack[::-1])

    return output


def flush_op_stack(operator, operator_stack, output):
    while (operator_stack 
           and PRECEDENCE[operator_stack[-1]] >= PRECEDENCE[operator]):
        output.append(operator_stack.pop())


def build_expression(expr_str):
    postfix_expr = build_postfix_expression(expr_str)
    expr = build_expr_from_postfix(postfix_expr)

    return expr


def build_expr_from_postfix(postfix_expr):
    operand_stack = deque()
    for token in postfix_expr:
        if token == 'and':
            op1, op2 = operand_stack.pop(), operand_stack.pop()
            operand_stack.append(And((op1, op2)))
        elif token == 'or':
            op1, op2 = operand_stack.pop(), operand_stack.pop()
            operand_stack.append(Or((op1, op2)))
        elif token == 'not':
            operand = operand_stack.pop()
            operand_stack.append(Not(operand))
        elif token in ('payee', '@'):
            operand = operand_stack.pop()
            if not isinstance(operand, RegexQuery):
                raise ValueError
            operand_stack.append(PayeeQuery(operand))
        else:
            operand = RegexQuery.from_string(token)
            operand_stack.append(operand)

    if len(operand_stack) != 1:
        raise ValueError

    return operand_stack[0]


