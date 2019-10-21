import re
from ledgeroni import expression
from ledgeroni.query import Or, And, Not, RegexQuery


def test_tokenize_expression():
    expr = 'not (Expense and Reddit) or Asset'
    tokens = list(expression.tokenize_expression(expr))
    assert tokens == ['not', '(', 'Expense', 'and', 'Reddit', ')', 'or', 'Asset']


class TestBuildPostfixExpression:
    def test_binary(self):
        expr = 'x and y'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'and']

        expr = 'x and y and z'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'and', 'z', 'and']

        expr = 'x or y or z'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'or', 'z', 'or']

    def test_unary(self):
        expr = 'not x'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'not']

    def test_precedence(self):
        expr = 'not x and y'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'not', 'y', 'and']

    def test_parens(self):
        expr = 'not (x and y)'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'and', 'not']

    def test_implicit_or(self):
        expr = 'x y'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'or']

        expr = 'x y z'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'or', 'z', 'or']

        expr = '(x y) z'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'or', 'z', 'or']

        expr = 'x (y or z)'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'z', 'or', 'or']


class TestBuildExprFromPostfix:
    def test_binary(self):
        postfix = ['x', 'y', 'or']
        result = expression.build_expr_from_postfix(postfix)
        query = Or((RegexQuery(re.compile('y')),
                    RegexQuery(re.compile('x'))))

        assert result == query

        postfix = ['x', 'y', 'and']
        result = expression.build_expr_from_postfix(postfix)
        query = And((RegexQuery(re.compile('y')),
                     RegexQuery(re.compile('x'))))

        assert result == query

    def test_unary(self):
        postfix = ['x', 'not']
        result = expression.build_expr_from_postfix(postfix)
        query = Not(RegexQuery(re.compile('x')))

        assert result == query

    def test_single(self):
        postfix = ['x']
        result = expression.build_expr_from_postfix(postfix)
        query = RegexQuery(re.compile('x'))

        assert result == query


class TestBuildExpression:
    def test_binary(self):
        postfix = 'x or y'
        result = expression.build_expression(postfix)
        query = Or((RegexQuery(re.compile('y')),
                    RegexQuery(re.compile('x'))))

        assert result == query

        postfix = 'x and y'
        result = expression.build_expression(postfix)
        query = And((RegexQuery(re.compile('y')),
                     RegexQuery(re.compile('x'))))

        assert result == query

    def test_unary(self):
        postfix = 'not x'
        result = expression.build_expression(postfix)
        query = Not(RegexQuery(re.compile('x')))

        assert result == query

    def test_single(self):
        postfix = 'x'
        result = expression.build_expression(postfix)
        query = RegexQuery(re.compile('x'))

        assert result == query

    def test_implicit_or(self):
        postfix = 'x y'
        result = expression.build_expression(postfix)
        query = Or((RegexQuery(re.compile('y')),
                    RegexQuery(re.compile('x'))))

        assert result == query

