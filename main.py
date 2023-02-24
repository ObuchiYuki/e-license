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

from argparse import ArgumentParser

class DriveSchoolCommand:
    command_name: str
    logger: Logger
    filemanager: FileManager
    config: CommandConfiguration

    def __init__(self, command_name: str, config: CommandConfiguration, logger: Logger) -> None:
        self.command_name = command_name
        self.logger = logger
        self.filemanager = FileManager(command_name, Path(os.path.expanduser('~')), self.logger)
        self.config = config

    def run(self, args: list[str]):
        parser = ArgumentParser(prog=self.command_name)
        subparsers = parser.add_subparsers()

        fetch_command = subparsers.add_parser("fetch")
        fetch_command.set_defaults(handler=self.run_fetch)
        
        reset_command = subparsers.add_parser("reset")
        reset_command.set_defaults(handler=self.run_reset)

        res = parser.parse_args(args)
        if hasattr(res, "handler"):
            res.handler(args)
        else:
            parser.print_help()

    def run_reset(self, args: list[str]):
        frame_io = FrameIOManager(self.filemanager)
        frame_io.reset_cache()

    def run_fetch(self, args: list[str]):
        driver = selenium_make()
        loader = CatalystLoader(driver, self.logger)
        login_catalyst = LoginCatalyst(self.config, loader)
        booktable_catalyst = BookTableCatalyst(login_catalyst, loader)
        
        book_table = booktable_catalyst.run()
        frame_io = FrameIOManager(self.filemanager)
        
        scanner = BookTableScanner(frame_io, book_table, self.logger)
        updated_frames = scanner.find_updated_frames()
        
        notifier = ClassNotifier(self.config, self.logger)
        if len(updated_frames) > 0:
            notifier.notify(updated_frames)
        else:
            self.logger.log("No updated frame found.")


if __name__ == "__main__":
    command_name = "driveschool"
    logger = Logger(command_name, is_debug=True)

    config = CommandConfiguration.from_env()
    if config is None:
        logger.error("Command configuration not found in environmental values. Set ELICENSE_USERNAME (username), ELICENSE_PASSWORD (password), ELICENSE_LOGIN (login page URL) in environmental values or .env file.")
        exit(1)

    command = DriveSchoolCommand(command_name=command_name, config=config, logger=logger)
    command.run(sys.argv[1:])
