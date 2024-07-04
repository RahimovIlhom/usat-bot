from datetime import datetime

import aiomysql
from environs import Env

env = Env()
env.read_env()


class DatabaseOlympian:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=env.str("FAN_DB_HOST"),
                user=env.str("FAN_DB_USER"),
                password=env.str("FAN_DB_PASSWORD"),
                db=env.str("FAN_DB_NAME"),
                autocommit=True
            )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def execute_query(self, query, *args, fetchall=False, fetchone=False):
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

    async def get_olympian(self, tgId, pinfl):
        query = (
            "SELECT tr.tg_id, tr.fullname, tr.phone_number, tr.science, tr.responses, tr.result_time, tr.test_id, "
            "tr.certificate_image, LENGTH(REPLACE(tr.responses, '0', '')) AS num_ones "
            "FROM test_result tr "
            "JOIN tests t ON tr.test_id = t.id "
            "WHERE (tr.tg_id = %s OR tr.pinfl = %s) AND t.olympiad_test = TRUE AND "
            "tr.result_time BETWEEN %s AND %s "
            "ORDER BY num_ones DESC "
            "LIMIT 1;"
        )
        start_date = datetime(2024, 4, 15)
        end_date = datetime(2024, 5, 5)
        return await self.execute_query(query, (tgId, pinfl, start_date, end_date), fetchone=True)
