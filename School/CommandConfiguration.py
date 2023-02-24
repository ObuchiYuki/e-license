import os
from typing import Union

from dataclasses import dataclass

@dataclass
class CommandConfiguration:
    username: str
    password: str
    loginurl: str

    @staticmethod
    def from_env() -> Union["CommandConfiguration", None]:
        ELICENSE_USERNAME = os.getenv("ELICENSE_USERNAME")
        if ELICENSE_USERNAME is None: return None
        
        ELICENSE_PASSWORD = os.getenv("ELICENSE_PASSWORD")
        if ELICENSE_PASSWORD is None: return None
        
        ELICENSE_LOGIN = os.getenv("ELICENSE_LOGIN")
        if ELICENSE_LOGIN is None: return None

        return CommandConfiguration(ELICENSE_USERNAME, ELICENSE_PASSWORD, ELICENSE_LOGIN)

        
