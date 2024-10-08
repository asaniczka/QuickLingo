"""
Contain all core db operations
"""

import os

from psycopg_pool import ConnectionPool, NullConnectionPool
from dotenv import load_dotenv

load_dotenv()

POSTGRES_POOL = NullConnectionPool(os.getenv("AZ_POSTGRES_URL"), open=True, min_size=0)


if __name__ == "__main__":
    with POSTGRES_POOL.connection() as conn:
        print("We're connected")
