from dataclasses import dataclass
from typing import Dict


@dataclass
class AuthContext:
    name: str
    cookies: Dict[str, str]