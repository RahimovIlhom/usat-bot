import datetime
from uuid import uuid4

import aiomysql
from environs import Env

env = Env()
env.read_env()


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=env.str("DB_HOST"),
                user=env.str("DB_USER"),
                password=env.str("DB_PASSWORD"),
                db=env.str("DB_NAME"),
                autocommit=True
            )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def execute_query(self, query, *args, **kwargs):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                result = await cursor.fetchall()
        return result

    async def select_simple_user(self, tgId):
        query = "SELECT tgId, fullname, language FROM simple_users WHERE tgId = %s;"
        return await self.execute_query(query, tgId)

    async def add_simple_user(self, tgId, fullname, language):
        query = "INSERT INTO simple_users (tgId, fullname, language) VALUES (%s, %s, %s);"
        await self.execute_query(query, tgId, fullname, language)
