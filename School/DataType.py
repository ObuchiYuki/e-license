import sys
from dataclasses import dataclass
from enum import Enum

class FrameStatus(Enum):
    reserved = 1
    reservable = 2
    none = 3

    @staticmethod
    def from_str(value: str) -> "FrameStatus":
        if value == "status0": return FrameStatus.none
        if value == "status1": return FrameStatus.reservable
        if value == "status3": return FrameStatus.reserved

        return FrameStatus.none
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        if self == FrameStatus.reserved: return "reserved"
        if self == FrameStatus.reservable: return "reservable"
        return "none"
        

@dataclass 
class Frame:
    date_name: str
    start_time: int
    status: FrameStatus

    def frame_id(self) -> str:
        return f"{self.date_name}:{self.start_time}"

    def __str__(self) -> str:
        return f"({self.start_time}, {self.status})"

@dataclass
class Date:
    name: str
    frames: list[Frame]

    def __str__(self) -> str:
        inner = ", ".join(str(frame) for frame in self.frames)
        return f"[{self.name}: {inner}]" 

@dataclass 
class BookTable:
    dates: list[Date]

    def __str__(self) -> str:
        return "\n".join(str(date) for date in self.dates)

