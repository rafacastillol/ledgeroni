import pytest
from ledgeroni import expression
from ledgeroni.query import Or, And, Not, RegexQuery, PayeeQuery


def test_tokenize_expression():
    expr = 'not (Expense and Reddit) or Asset'
    tokens = list(expression.tokenize_expression(expr))
    assert tokens == [
        'not', '(', 'Expense', 'and', 'Reddit', ')', 'or', 'Asset']


class TestBuildPostfixExpression:
    def test_and(self):
        expr = 'x and y'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'and']

        expr = 'x and y and z'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'and', 'z', 'and']

    def test_or(self):
        expr = 'x or y or z'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'y', 'or', 'z', 'or']

    def test_not(self):
        expr = 'not x'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'not']

    def test_payee(self):
        expr = 'payee x'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'payee']

    def test_unary_precedence(self):
        expr = 'not payee x'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', 'payee', 'not']

    def test_payee_at(self):
        expr = '@x'
        postfix = list(expression.build_postfix_expression(expr))
        assert postfix == ['x', '@']

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
        query = Or((RegexQuery.from_string('y'),
                    RegexQuery.from_string('x')))

        assert result == query

        postfix = ['x', 'y', 'and']
        result = expression.build_expr_from_postfix(postfix)
        query = And((RegexQuery.from_string('y'),
                     RegexQuery.from_string('x')))

        assert result == query

    def test_unary(self):
        postfix = ['x', 'not']
        result = expression.build_expr_from_postfix(postfix)
        query = Not(RegexQuery.from_string('x'))

        assert result == query

    def test_single(self):
        postfix = ['x']
        result = expression.build_expr_from_postfix(postfix)
        query = RegexQuery.from_string('x')

        assert result == query

    def test_payee(self):
        postfix = ['x', 'payee']
        result = expression.build_expr_from_postfix(postfix)
        query = PayeeQuery(RegexQuery.from_string('x'))

        assert result == query

    def test_payee_at(self):
        postfix = ['x', '@']
        result = expression.build_expr_from_postfix(postfix)
        query = PayeeQuery(RegexQuery.from_string('x'))

        assert result == query

    def test_payee_validation(self):
        postfix = ['x', 'not', '@']
        with pytest.raises(ValueError):
            expression.build_expr_from_postfix(postfix)

    def test_precedence(self):
        postfix = ['y', 'not', 'x', '@', 'and']
        result = expression.build_expr_from_postfix(postfix)
        query = And((PayeeQuery(RegexQuery.from_string('x')),
                     Not(RegexQuery.from_string('y'))))

        assert result == query


class TestBuildExpression:
    def test_binary(self):
        postfix = 'x or y'
        result = expression.build_expression(postfix)
        query = Or((RegexQuery.from_string('y'),
                    RegexQuery.from_string('x')))

        assert result == query

        postfix = 'x and y'
        result = expression.build_expression(postfix)
        query = And((RegexQuery.from_string('y'),
                     RegexQuery.from_string('x')))

        assert result == query

    def test_unary(self):
        postfix = 'not x'
        result = expression.build_expression(postfix)
        query = Not(RegexQuery.from_string('x'))

        assert result == query

    def test_single(self):
        postfix = 'x'
        result = expression.build_expression(postfix)
        query = RegexQuery.from_string('x')

        assert result == query

    def test_implicit_or(self):
        postfix = 'x y'
        result = expression.build_expression(postfix)
        query = Or((RegexQuery.from_string('y'),
                    RegexQuery.from_string('x')))

        assert result == query

