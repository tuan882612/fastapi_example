import structlog
from asyncpg.pool import create_pool, Pool
from asyncpg.connection import Connection
import os

class database:
    pool: Pool = None
    logger = structlog.get_logger()

    @classmethod
    async def create_pool(cls):
        cls.logger.info("Creating database pool")
        try:
            cls.pool = await create_pool(dsn=os.environ.get("DATABASE_URL"), min_size=1)
        except Exception as e:
            cls.logger.error(f"Failed to create database pool: {e}")
            raise

    @classmethod
    async def release_connection(cls, conn: Connection):
        await cls.pool.release(conn)
        cls.logger.info("Released database connection")
        
    @classmethod
    async def get_conn(cls):
        conn = await cls.pool.acquire()
        try:
            yield conn
        finally:
            await cls.pool.release(conn)