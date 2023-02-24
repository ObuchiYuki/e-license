from dataclasses import dataclass

@dataclass
class CommandConfiguration:
    loginurl: str
    username: str
    password: str