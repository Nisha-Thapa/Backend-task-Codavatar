""" Configuration generation for reading the Application Configurations """
from dotenv import load_dotenv
import yaml
import os
import re


class GenericConfig:
    profile: str

    def __init__(self):
        load_dotenv()
        config_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "resources",
            "config.yml",
        )
        with open(config_file_path) as config_file:
            config_content = config_file.read()

        # Replacing config placeholders with environment variable values
        self.config_dict = yaml.safe_load(self.replace_env_vars(config_content))
        self.profile = os.environ.get("CLOUD_TELEPHONY_ACTIVE_PROFILE", "dev")

    def replace_env_vars(self, config_str):
        """Replace ${VAR_NAME} placeholders with actual environment variables."""
        pattern = re.compile(r"\$\{(\w+)\}")
        return pattern.sub(
            lambda match: os.getenv(match.group(1), match.group(0)), config_str
        )

    def get_app_name(self):
        return self.config_dict["app"]["application-name"]

    def get_connection_details(self, db_name: str):
        """Send details of the DB connections back
        as a dictionary for proper operations"""
        return {
            "conn_string": self.config_dict["app"]["datasource"][self.profile][db_name][
                "conn_string"
            ],
            "driver_name": self.config_dict["app"]["datasource"][self.profile][db_name][
                "driver-name"
            ],
            "host": self.config_dict["app"]["datasource"][self.profile][db_name][
                "host"
            ],
            "port": self.config_dict["app"]["datasource"][self.profile][db_name][
                "port"
            ],
            "username": self.config_dict["app"]["datasource"][self.profile][db_name][
                "username"
            ],
            "database": self.config_dict["app"]["datasource"][self.profile][db_name][
                "database-name"
            ],
            "password": self.config_dict["app"]["datasource"][self.profile][db_name][
                "password"
            ],
        }

    def get_server_port(self):
        """Pulls the Server port from the Config file"""
        return self.config_dict["server"]["port"]

    def get_server_host(self):
        """Pulls the Server hosted URL from the Config file"""
        return self.config_dict["server"]["host"]

    def get_context_root_path(self):
        """Pulls the Server hosted URL context path from the Config file"""
        return self.config_dict["server"]["context-path"]

    def get_logging_levels(self):
        """Pulls the Logging level for Application"""
        return self.config_dict["logging"]["level"]

    def get_logging_max_file_size(self):
        """Pulls the max file size from the Config file"""
        return self.config_dict["logging"]["max_file_size"]

    def get_logging_backup_count(self):
        """Pulls the max backup count from the Config file"""
        return self.config_dict["logging"]["backup_count"]

    def get_logging_format(self):
        """Pulls the Logging formats"""
        return self.config_dict["logging"]["format"]

    def get_logging_filename(self):
        """Pulls the filename for the Logging file"""
        return self.config_dict["logging"]["filename"]

    def get_logging_config(self):
        """Get the whole Logging Config"""
        return self.config_dict["logging"]
