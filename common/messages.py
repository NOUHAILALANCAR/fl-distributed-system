from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Message:
    round: int
    weights: Dict[str, Any]
    timestamp: int
    client_id: str
    data_size: int
