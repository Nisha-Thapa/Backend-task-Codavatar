from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app import logs
from src.app.config.generic_config import GenericConfig
from src.app.config.server_config import Servlet
from src.app.core.exception.router_exception import initiate_exception_handling

# Routes
from src.app.users.api import router as user_router_v1
from src.app.telephone.api import router as telephone_router_v1


class CloudTelephonyApplication:
    app: FastAPI

    def __init__(self):
        _cfgs = GenericConfig()
        self.app = FastAPI(
            debug=True,
            title="Cloud Telephony Services",
            description="Endpoints for CodAvatar (Cloud Telephony Services)",
            version="1.0",
            openapi_url=f"{_cfgs.get_context_root_path()}/apidoc/v1/openapi.json",
            docs_url=f"{_cfgs.get_context_root_path()}/apidoc/swagger-ui.html",
        )
        self.configure_cors()

    def configure_cors(self):
        """Configure CORS middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def patchRoutes(self, with_context: str):
        """return the configuration"""
        logs.info("Cloud Telephony Services v1.0 - STARTING")
        # Routers
        self.app.include_router(user_router_v1.route_controller, prefix=with_context)
        self.app.include_router(
            telephone_router_v1.route_controller, prefix=with_context
        )


if __name__ == "__main__":
    """All Operation starts from here"""
    global api
    api = CloudTelephonyApplication()
    initiate_exception_handling(api.app)
    servlet = Servlet()
    executor = servlet.configure_server(api)
    executor.run()

# # Uncomment for Hot reload while development
# # CMD-> uvicorn main:app --reload
# print("DEBUG")
# api = CloudTelephonyApplication()
# initiate_exception_handling(api.app)
# api.patchRoutes('/ca-ct')
# app = api.app
