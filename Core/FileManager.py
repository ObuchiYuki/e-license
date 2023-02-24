import shutil
import atexit
from pathlib import Path

from uuid import uuid4 as uuid

from Core.Logger import Logger
from Core.Error import *

class FileManager:
    command_name: str
    logger: Logger
    root: Path

    def __init__(self, command_name: str, root: Path, logger: Logger) -> None:
        self.command_name = command_name
        self.logger = logger    
        self.root = root
        self.__cleanup_tmp_dir()
        
        atexit.register(self.__cleanup_tmp_dir)

    def noduplicate_path(self, directory: Path, basename: str, ext: str|None) -> Path:
        return directory / self.noduplicate_filename(directory, basename, ext)

    def noduplicate_filename(self, directory: Path, basename: str, ext: str|None) -> str:
        if ext is None:
            filename = basename
        else:
            filename = f"{basename}.{ext}"
        couter = 2
        while (directory / filename).exists():
            if ext is None:
                filename = f"{basename} ({couter})"
            else:
                filename = f"{basename} ({couter}).{ext}"
            couter += 1
        return filename

    def command_directory(self) -> Path:
        self.__create_command_dir()
        return self.__command_path

    def temporary_directory(self) -> Path:
        self.__create_tmp_dir()
        return self.__tmp_path

    def unique_temporary_directory(self) -> Path:
        dirname = uuid()
        dirpath = self.temporary_directory() / str(dirname.hex)
        dirpath.mkdir(parents=True, exist_ok=True)
        return dirpath

    @property
    def __command_path(self) -> Path:
        return self.root / f".{self.command_name}"

    @property
    def __tmp_path(self) -> Path:
        return self.root / f".tmp_{self.command_name}"

    def __cleanup_tmp_dir(self):
        try:
            if self.__tmp_path.exists():
                shutil.rmtree(self.__tmp_path)
        except Exception as e:
            raise InternalError("Cleanup temporary directory failed.")
        self.logger.debug("Cleanup temporary directory end.")

    def __create_tmp_dir(self):
        try:
            self.__tmp_path.mkdir(exist_ok=True)
        except Exception as e:
            raise InternalError("Create temporary directory failed.")

    def __create_command_dir(self):
        try:
            self.__command_path.mkdir(exist_ok=True)
        except Exception as e:
            raise InternalError("Create command directory failed.")
