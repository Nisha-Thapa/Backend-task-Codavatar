#!usr/bin/python3
from src.app.config.log_config import getServiceLogger
from src.app.util.init_prints import *  # noqa: F401, F403

global logs
logs = getServiceLogger()
