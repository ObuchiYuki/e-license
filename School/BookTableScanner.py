from School.DataType import *
from School.FrameIOManager import FrameIOManager
   
class BookTableScanner:
    frame_io: FrameIOManager
    book_table: BookTable

    def __init__(self, frame_io: FrameIOManager, book_table: BookTable) -> None:
        self.frame_io = frame_io
        self.book_table = book_table

    def find_updated_frames(self) -> list[Frame]:
        new_frames = self.looks_good()
        updated_frames = self.frame_io.find_new_frames(new_frames)
        return updated_frames

    def looks_good(self) -> list[Frame]:
        frames: list[Frame] = []
        
        for date in self.book_table.dates:
            for frame in date.frames:
                if frame.start_time <= 10: continue
                if frame.status == FrameStatus.reservable:
                    frames.append(frame)

        return frames   