from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from src.auth.router import auth_router
from src.database import database
from starlette.middleware.cors import CORSMiddleware
import structlog

class server:
    def __init__(self) -> None:
        # Load environment variables
        load_dotenv(dotenv_path=".env")
        
        # Initialize FastAPI and other components
        self.app = FastAPI()
        self.setup_logger()
        self.setup_middlewares()
        self.setup_routes()
        
        # Event handlers
        self.app.add_event_handler("startup", self.on_startup)
        self.app.add_event_handler("shutdown", self.on_shutdown)

    def setup_routes(self) -> None:
        v1_router = APIRouter(prefix="/api/v1")
        v1_router.include_router(auth_router)
        self.app.include_router(v1_router)
        
    def setup_middlewares(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
    def setup_logger(self) -> None:
        structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
    )

    async def on_startup(self) -> None:
        await database.create_pool()
        
    async def on_shutdown(self) -> None:
        await database.pool.close()

server = server()
app = server.app
