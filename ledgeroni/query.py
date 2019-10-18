import re
from dataclasses import dataclass, field
from typing import Tuple

def build_simple_or_query(strs):
    qs = tuple([RegexQuery(re.compile(s)) for s in strs])
    return Or(qs)

@dataclass(frozen=True)
class Query:
    pass


@dataclass(frozen=True)
class RegexQuery(Query):
    regex: re.Pattern

    def execute(self, data):
        return self.regex.match(data) is not None


@dataclass(frozen=True)
class Or(Query):
    qs: Tuple[Query]
    def execute(self, data):
        return any(q.execute(data) for q in self.qs)

