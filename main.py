import sys
import json
import os
from pathlib import Path

from dotenv import load_dotenv; load_dotenv()

from Core.Catalyst import selenium_make, CatalystLoader
from Core.Logger import Logger
from Core.FileManager import FileManager

from School.LoginCatalyst import LoginCatalyst
from School.BookTableCatalyst import BookTableCatalyst
from School.DataType import *
from School.FrameIOManager import FrameIOManager
from School.ClassNotifier import ClassNotifier
from School.BookTableScanner import BookTableScanner

from School.CommandConfiguration import CommandConfiguration

if __name__ == "__main__":
    command_name = "driveschool"
    logger = Logger(command_name, is_debug=False)
    filemanager = FileManager(command_name, Path(os.path.expanduser('~')), logger)

    config = CommandConfiguration.from_env()
    if config is None:
        logger.error("Command configuration not found in environmental values. Set ELICENSE_USERNAME (username), ELICENSE_PASSWORD (password), ELICENSE_LOGIN (login page URL) in environmental values or .env file.")
        exit(1)

    driver = selenium_make()
    loader = CatalystLoader(driver, logger)
    login_catalyst = LoginCatalyst(config, loader)
    booktable_catalyst = BookTableCatalyst(login_catalyst, loader)
    
    book_table = booktable_catalyst.run()
    frame_io = FrameIOManager(filemanager)
    
    scanner = BookTableScanner(frame_io, book_table)
    updated_frames = scanner.find_updated_frames()
    
    notifier = ClassNotifier(config, logger)
    if len(updated_frames) > 0:
        notifier.notify(updated_frames)