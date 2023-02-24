import sys
import json
import os
from pathlib import Path

from Core.Catalyst import selenium_make, CatalystLoader
from Core.Logger import Logger
from Core.FileManager import FileManager

from School.LoginCatalyst import LoginCatalyst
from School.BookTableCatalyst import BookTableCatalyst
from School.DataType import *
from School.FrameIOManager import FrameIOManager
from School.ClassNotifier import ClassNotifier
from School.BookTableScanner import BookTableScanner

if __name__ == "__main__":
    command_name = "driveschool"
    logger = Logger(command_name, is_debug=False)
    filemanager = FileManager(command_name, Path(os.path.expanduser('~')), logger)
    driver = selenium_make()
    loader = CatalystLoader(driver, logger)
    login_catalyst = LoginCatalyst("23949", "KTYobuchi3", loader)
    booktable_catalyst = BookTableCatalyst(login_catalyst, loader)
    
    book_table = booktable_catalyst.run()
    frame_io = FrameIOManager(filemanager)
    
    scanner = BookTableScanner(frame_io, book_table)
    updated_frames = scanner.find_updated_frames()
    
    notifier = ClassNotifier(logger)
    if len(updated_frames) > 0:
        notifier.notify(updated_frames)