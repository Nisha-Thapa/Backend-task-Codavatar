""" GENERIC LOGGING CONFIG FOR ALL SERVICES """
import logging
from logging.handlers import RotatingFileHandler
from src.app.config.generic_config import os, GenericConfig


class ServiceLogger:
    log_definition: dict
    log_levels: dict
    log_filename: str
    log_formats: str
    logger: logging.Logger

    def __init__(self):
        _get_Config = GenericConfig()
        self.log_definition = _get_Config.get_logging_config()
        self.log_filename = _get_Config.get_logging_filename()
        self.log_levels = _get_Config.get_logging_levels()
        self.log_max_file_size = _get_Config.get_logging_max_file_size()
        self.log_backup_count = _get_Config.get_logging_backup_count()
        self.log_formats = _get_Config.get_logging_format()
        self.logger = logging.getLogger(_get_Config.get_app_name())

    def logging_setup_console(self):
        """SETS UP LOGGING FOR THE CONSOLE"""
        fmt = logging.Formatter(self.log_formats)
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, self.log_levels["console"]))
        ch.setFormatter(fmt)
        self.logger.addHandler(ch)

    def logging_setup_file(self):
        log_dir = self.log_filename.split("/")[0]
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        fmt = logging.Formatter(self.log_formats)
        fh = RotatingFileHandler(
            self.log_filename,
            mode="a",
            maxBytes=self.log_max_file_size,
            backupCount=self.log_backup_count,
        )
        fh.setLevel(getattr(logging, self.log_levels["file"]))
        fh.setFormatter(fmt)
        self.logger.addHandler(fh)

    def set_logger(self):
        self.logging_setup_console()
        self.logging_setup_file()
        self.logger.setLevel(logging.DEBUG)
        print(self.logger)
        return self.logger


def getServiceLogger():
    """Returns Service Logger"""
    log_obj = ServiceLogger()
    logs = log_obj.set_logger()
    return logs
