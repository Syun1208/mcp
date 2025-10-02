import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class WASAKnowledge:
    question: str
    contexts: List[Dict[str, Any]]
    scores: List[float]
