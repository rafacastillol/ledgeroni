from arrow.arrow import Arrow
from dataclasses import dataclass
from typing import List

@dataclass
class Transaction:
    date: Arrow
    description: str

@dataclass
class Posting:
    account: List[str]
    
