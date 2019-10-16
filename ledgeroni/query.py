from dataclasses import dataclass, field


class Query:
    pass


class RegexQuery(Query):
    def __init__(self, re):
        self.re = re

    def execute(self, data):
        return self.re.match(data) is not None


class BinaryQuery(Query):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class And(BinaryQuery):
    def execute(self, data):
        return self.a.execute(data) and self.b.execute(data)


class Or(BinaryQuery):
    def execute(self, data):
        return self.a.execute(data) or self.b.execute(data)


class Not(Query):
    def __init__(self, q):
        self.q = q

    def execute(self, data):
        return not self.q.execute(data)
