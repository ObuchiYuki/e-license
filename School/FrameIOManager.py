import sys
import json
from pathlib import Path

from Core.FileManager import FileManager

from School.DataType import *
   
class FrameIOManager:
    filemanager: FileManager
    
    def __init__(self, filemanager: FileManager) -> None:
        self.filemanager = filemanager

    def old_frame_path(self) -> Path:
        return self.filemanager.command_directory() / "old_frames.json"

    def find_new_frames(self, new_frames: list[Frame]) -> list[Frame]:
        old_frame_path = self.old_frame_path()
        if old_frame_path.exists():
            old_frame_ids = self.read_frames(old_frame_path)
        else:
            old_frame_ids = []

        delta = self.frame_delta(new_frames, old_frame_ids)
        self.write_frames(new_frames, old_frame_path)
        return delta
    
    def reset_cache(self):
        old_frame_path = self.old_frame_path()
        old_frame_path.unlink(missing_ok=True)

    def write_frames(self, frames: list[Frame], path: Path):
        with open(path, 'w') as f:
            json_string = json.dumps({
                "frames": [frame.frame_id() for frame in frames]
            }, indent=4)

            f.write(json_string)
        
    def read_frames(self, path: Path) -> list[str]:
        with open(path, 'r') as f:
            ids = json.load(f)["frames"]
            return ids

    def frame_delta(self, new_frames: list[Frame], old_frame_ids: list[str]) -> list[Frame]:
        frames: list[Frame] = []
        for new_frame in new_frames:
            if not new_frame.frame_id() in old_frame_ids:
                frames.append(new_frame)

        return frames

