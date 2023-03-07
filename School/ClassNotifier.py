import os
from pathlib import Path
from sys import platform

from Core.Logger import Logger

from School.DataType import *
from School.CommandConfiguration import CommandConfiguration

class Notifier:
    def notify(self, title: str, message: str, link: str):
        raise NotImplementedError()

class ClassNotifier:
    logger: Logger
    notifier: Notifier
    config: CommandConfiguration

    def __init__(self, config: CommandConfiguration, logger: Logger) -> None:
        self.logger = logger
        self.config = config
        self.notifier = self.notifier_for_platform()

    def notify(self, updates: list[Frame]):
        message = "、".join(map(self.format_frame, updates)) 
        title = "新しい予約が可能になりました。"
        self.logger.log(f"{title}: {message}")
        self.notifier.notify(title, message, self.config.loginurl)

    def notifier_for_platform(self) -> Notifier:
        if platform == "linux" or platform == "linux2":
            raise NotImplementedError("Notifier for Linux is not implemented.")
        elif platform == "darwin":
            return MacOSNotifier(self.logger)
        elif platform == "win32":
            raise NotImplementedError("Notifier for Widnows is not implemented.")
        else:
            raise NotImplementedError(f"Notifier for {platform} is not implemented.")

    def format_frame(self, frame: Frame):
        return f"{frame.date_name} {frame.start_time}時" 

class MacOSNotifier(Notifier):
    terminal_notifier: bool

    def __init__(self, logger: Logger) -> None:
        tf_found = Path("/usr/local/bin/terminal-notifier").exists()
        self.terminal_notifier = tf_found
        if not tf_found:
            logger.error("terminal-notifier not found. Please install via brew. Using osascript as fallback.")

    def notify(self, title: str, message: str, link: str):
        print(self.terminal_notifier)
        if self.terminal_notifier:
            os.system(f"""
                /usr/local/bin/terminal-notifier -title "{title}" -message "{message}" -open "{link}"
            """)
        else:
            os.system(f"""
                osascript -e 'display notification "{message}" with title "{title}"'
            """)


