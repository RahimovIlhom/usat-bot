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

    async def select_types_of_education(self):
        query = "SELECT id, nameUz, nameRu FROM types_of_education;"
        return await self.execute_query(query, fetchall=True)

    async def select_type_of_education(self, id):
        query = "SELECT id, nameUz, nameRu FROM types_of_education WHERE id = %s;"
        return await self.execute_query(query, id, fetchone=True)

    async def add_or_set_type_of_education(self, nameUz, nameRu, id=None):
        if id:
            if await self.select_type_of_education(id):
                query = "UPDATE types_of_education SET nameUz = %s, nameRu = %s WHERE id = %s;"
                await self.execute_query(query, nameUz, nameRu, id)
        else:
            query = "INSERT INTO types_of_education (nameUz, nameRu) VALUES (%s, %s);"
            await self.execute_query(query, nameUz, nameRu)

    async def delete_type_of_education(self, id):
        query = "DELETE FROM types_of_education WHERE id = %s"
        await self.execute_query(query, id)

    async def select_contact_price(self, direction_id, type_id):
        query = "SELECT id, amount FROM contract_prices WHERE directionOfEducation_id = %s AND typeOfEducation_id = %s"
        return await self.execute_query(query, direction_id, type_id, fetchone=True)

    async def select_contract_prices_for_direction(self, direction_id):
        query = """
        SELECT cp.id, cp.typeOfEducation_id, cp.amount, te.nameUz 
        FROM contract_prices cp
        JOIN types_of_education te ON cp.typeOfEducation_id = te.id
        WHERE cp.directionOfEducation_id = %s;
        """
        return await self.execute_query(query, direction_id, fetchall=True)

    async def add_or_set_contract_price(self, summa, direction_id, type_id):
        contract_price = await self.select_contact_price(direction_id, type_id)
        if contract_price:
            query = "UPDATE contract_prices SET amount = %s WHERE id = %s"
            await self.execute_query(query, summa, contract_price[0])
            return 'set'
        else:
            query = ("INSERT INTO contract_prices (amount, directionOfEducation_id, typeOfEducation_id) VALUES "
                     "(%s, %s, %s);")
            await self.execute_query(query, summa, direction_id, type_id)
            return 'add'

    async def delete_contract_price(self, direction_id, type_id):
        query = "DELETE FROM contract_prices WHERE directionOfEducation_id = %s AND typeOfEducation_id = %s;"
        await self.execute_query(query, direction_id, type_id)
