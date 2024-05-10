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

    async def execute_query(self, query, *args, fetchall=False, fetchone=False, **kwargs):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                if fetchall:
                    result = await cursor.fetchall()
                elif fetchone:
                    result = await cursor.fetchone()
                else:
                    result = None
        return result

    async def select_simple_user(self, tgId):
        query = "SELECT tgId, fullname, language FROM simple_users WHERE tgId = %s;"
        return await self.execute_query(query, tgId, fetchone=True)

    async def add_or_set_simple_user(self, tgId, fullname, language):
        if await self.select_simple_user(tgId):
            query = "UPDATE simple_users SET fullname = %s, language = %s WHERE tgId = %s;"
            await self.execute_query(query, fullname, language, tgId)
        else:
            query = "INSERT INTO simple_users (tgId, fullname, language) VALUES (%s, %s, %s);"
            await self.execute_query(query, tgId, fullname, language)

    async def select_directions(self):
        query = "SELECT id, nameUz, nameRu FROM educational_areas;"
        return await self.execute_query(query, fetchall=True)

    async def select_direction(self, id):
        query = "SELECT id, nameUz, nameRu FROM educational_areas WHERE id = %s;"
        return await self.execute_query(query, id, fetchone=True)

    async def add_or_set_direction(self, nameUz, nameRu, id=None):
        if id:
            if await self.select_direction(id):
                query = "UPDATE educational_areas SET nameUz = %s, nameRu = %s WHERE id = %s;"
                await self.execute_query(query, nameUz, nameRu, id)
        else:
            query = "INSERT INTO educational_areas (nameUz, nameRu) VALUES (%s, %s);"
            await self.execute_query(query, nameUz, nameRu)

    async def delete_direction(self, id):
        query = "DELETE FROM educational_areas WHERE id = %s"
        await self.execute_query(query, id)



