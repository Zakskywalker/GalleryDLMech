import logging
from pathlib import Path


class AppLogger:
    def __init__(self, log_file="app.log"):
        Path(log_file).touch(exist_ok=True)

        self.logger = logging.getLogger("GalleryDL")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)