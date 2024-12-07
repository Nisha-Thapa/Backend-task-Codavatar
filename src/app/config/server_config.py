import uvicorn
from src.app.config.generic_config import GenericConfig


class Servlet:
    host: str
    port: int
    context_root: str
    server: uvicorn.Server

    def __init__(self):
        _get_Config = GenericConfig()
        self.host = _get_Config.get_server_host()
        self.port = _get_Config.get_server_port()
        self.context_root = _get_Config.get_context_root_path()

    def configure_server(self, api) -> uvicorn.Server:
        """Configure server to host the required API"""
        api.patchRoutes(self.context_root)
        config = uvicorn.Config(api.app, host=self.host, port=self.port)
        self.server = uvicorn.Server(config)
        return self.server
