import random
from datetime import datetime

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
        query = "SELECT id, nameUz, nameRu, active FROM educational_areas;"
        return await self.execute_query(query, fetchall=True)

    async def select_active_directions(self):
        query = "SELECT id, nameUz, nameRu FROM educational_areas WHERE active = TRUE;"
        return await self.execute_query(query, fetchall=True)

    async def select_direction(self, id):
        query = "SELECT id, nameUz, nameRu, active FROM educational_areas WHERE id = %s;"
        return await self.execute_query(query, id, fetchone=True)

    async def get_sciences_for_direction(self, direction_id):
        query = """
            SELECT s.id, s.nameUz, s.nameRu
            FROM sciences s
            INNER JOIN educational_areas_sciences eas ON s.id = eas.science_id
            WHERE eas.directionofeducation_id = %s;
        """
        return await self.execute_query(query, direction_id, fetchall=True)

    async def get_sciences_not_for_direction(self, direction_id):
        query = """
            SELECT s.id, s.nameUz, s.nameRu
            FROM sciences s
            WHERE s.id NOT IN (
                SELECT science_id
                FROM educational_areas_sciences
                WHERE directionofeducation_id = %s
            );
        """
        return await self.execute_query(query, direction_id, fetchall=True)

    async def remove_science_for_direction(self, direction_id, science_id):
        query = """
            DELETE FROM educational_areas_sciences
            WHERE directionofeducation_id = %s AND science_id = %s;
        """
        await self.execute_query(query, direction_id, science_id)

    async def add_science_for_direction(self, direction_id, science_id):
        query = """
            INSERT INTO educational_areas_sciences (directionofeducation_id, science_id)
            VALUES (%s, %s);
        """
        await self.execute_query(query, direction_id, science_id)

    async def add_direction(self, newId, nameUz, nameRu, *args, **kwargs):
        if await self.select_direction(newId):
            return 'already_exist'
        query = "INSERT INTO educational_areas (id, nameUz, nameRu, active) VALUES (%s, %s, %s, FALSE);"
        await self.execute_query(query, newId, nameUz, nameRu)

    async def set_direction(self, id, nameUz, nameRu, *args, **kwargs):
        if await self.select_direction(id):
            query = "UPDATE educational_areas SET nameUz = %s, nameRu = %s WHERE id = %s;"
            await self.execute_query(query, nameUz, nameRu, id)

    async def update_active_direction(self, id, action: bool):
        query = "UPDATE educational_areas SET active = %s WHERE id = %s;"
        await self.execute_query(query, action, id)

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
        SELECT cp.id, cp.typeOfEducation_id, cp.amount, te.nameUz, te.nameRu 
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

    async def get_applicant(self, tgId, pinfl=None, phone=None):
        query = (
            "SELECT tgId, phoneNumber, additionalPhoneNumber, pinfl, firstName, lastName, middleName, passport, "
            "directionOfEducation_id, typeOfEducation_id, languageOfEducation, contractFile, olympian, createdTime, "
            "applicationStatus "
            "FROM applicants WHERE tgId = %s OR pinfl = %s OR phoneNumber = %s;"
        )
        return await self.execute_query(query, tgId, pinfl, phone, fetchone=True)

    async def get_applicant_for_excel(self, tgId):
        query = """
        SELECT 
            a.tgId, a.phoneNumber, a.additionalPhoneNumber, a.pinfl, a.firstName, a.lastName, a.middleName, a.passport, 
            e.nameUz AS directionOfEducation, t.nameUz AS typeOfEducation, a.languageOfEducation, a.contractFile, 
            a.olympian, a.createdTime, a.applicationStatus
        FROM 
            applicants a
        LEFT JOIN 
            educational_areas e ON a.directionOfEducation_id = e.id
        LEFT JOIN 
            types_of_education t ON a.typeOfEducation_id = t.id
        WHERE 
            a.tgId = %s;
        """
        return await self.execute_query(query, tgId, fetchone=True)

    async def update_application_status(self, tgId, new_status):
        query = "UPDATE applicants SET applicationStatus = %s WHERE tgId = %s;"
        await self.execute_query(query, new_status, tgId)

    async def add_applicant(self, tgId, phoneNumber, additionalPhoneNumber, pinfl, firstName, lastName, middleName,
                            passport, directionOfEducation_id, typeOfEducation_id, languageOfEducation, olympian):
        query = (
            "INSERT INTO applicants (tgId, phoneNumber, additionalPhoneNumber, pinfl, firstName, lastName, "
            "middleName, passport, directionOfEducation_id, typeOfEducation_id, languageOfEducation, "
            "applicationStatus, olympian, createdTime, updatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s);"
        )
        await self.execute_query(query, tgId, phoneNumber, additionalPhoneNumber, pinfl, firstName, lastName,
                                 middleName, passport, directionOfEducation_id, typeOfEducation_id,
                                 languageOfEducation, 'SUBMITTED', olympian, datetime.now(), datetime.now())

    async def get_applicant_exam_results(self, tgId):
        query = "SELECT id, applicant_id, result, trueResponseCount FROM exam_results WHERE applicant_id = %s"
        return await self.execute_query(query, tgId, fetchall=True)

    async def add_exam_result(self, applicant_id, result, trueResponseCount):
        query = "INSERT INTO exam_results (applicant_id, result, trueResponseCount) VALUES (%s, %s, %s);"
        await self.execute_query(query, applicant_id, result, trueResponseCount)

    async def select_questions_for_test(self, test_id, count=None):
        if count:
            # Randomly select `count` number of questions
            query = "SELECT id, test_id, image, question, trueResponse FROM questions WHERE test_id = %s;"
            all_questions = await self.execute_query(query, test_id, fetchall=True)
            random_questions = random.sample(all_questions, min(count, len(all_questions)))
            return random_questions
        else:
            # Select all questions
            query = "SELECT id, test_id, image, question, trueResponse FROM questions WHERE test_id = %s;"
            return await self.execute_query(query, test_id, fetchall=True)

    async def select_question(self, ques_id):
        query = """
            SELECT q.id, q.test_id, q.image, q.question, q.trueResponse, t.science_id, t.language, s.nameUz
            FROM questions q
            JOIN tests t ON q.test_id = t.id
            JOIN sciences s ON t.science_id = s.id
            WHERE q.id = %s;
            """
        return await self.execute_query(query, ques_id, fetchone=True)

    async def add_or_update_question(self, test_id, image, question, trueResponse, question_id=None, *args, **kwargs):
        if question_id:
            query = "UPDATE questions SET test_id = %s, image = %s, question = %s, trueResponse = %s WHERE id = %s;"
            await self.execute_query(query, test_id, image, question, trueResponse, question_id)
            return 'update'
        else:
            query = "INSERT INTO questions (test_id, image, question, trueResponse) VALUES (%s, %s, %s, %s);"
            await self.execute_query(query, test_id, image, question, trueResponse)
            test_app = await self.select_test(test_id)
            if test_app[2] == test_app[6]:
                query_test = "UPDATE tests SET isActive = %s WHERE id = %s"
                await self.execute_query(query_test, True, test_app[0])
            return 'add'

    async def delete_question(self, ques_id, test_id):
        query = "DELETE FROM questions WHERE id = %s;"
        await self.execute_query(query, ques_id)
        test_app = await self.select_test(test_id)
        if test_app[2] > test_app[6]:
            query_test = "UPDATE tests SET isActive = %s WHERE id = %s"
            await self.execute_query(query_test, False, test_id)

    async def select_sciences(self):
        query = "SELECT id, nameUz, nameRu FROM sciences;"
        return await self.execute_query(query, fetchall=True)

    async def select_science(self, sc_id):
        query = "SELECT id, nameUz, nameRu FROM sciences WHERE id = %s;"
        return await self.execute_query(query, sc_id, fetchone=True)

    async def add_or_update_science(self, nameUz, nameRu, science_id=None, *args):
        if science_id is None:
            query = "INSERT INTO sciences (nameUz, nameRu) VALUES (%s, %s);"
            await self.execute_query(query, nameUz, nameRu)
        else:
            query = "UPDATE sciences SET nameUz = %s, nameRu = %s WHERE id = %s;"
            await self.execute_query(query, nameUz, nameRu, science_id)

    async def delete_science(self, sc_id):
        query = "DELETE FROM sciences WHERE id = %s;"
        await self.execute_query(query, sc_id)

    async def add_test(self, science_id, questionsCount, language, id=None, *args):
        query = ("INSERT INTO tests (science_id, questionsCount, language, isActive, "
                 "createdTime) VALUES (%s, %s, %s, %s, %s);")
        await self.execute_query(query, science_id, questionsCount, language, False,
                                 datetime.now())

    async def update_test(self, science_id, questionsCount, language, id):
        query = "UPDATE tests SET science_id = %s, questionsCount = %s, language = %s WHERE id = %s;"
        await self.execute_query(query, science_id, questionsCount, language, id)

    async def select_tests_for_science(self, sc_id):
        query = ("""
            SELECT t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime, 
                   COUNT(q.id) AS questions_count
            FROM tests t
            LEFT JOIN questions q ON t.id = q.test_id
            WHERE t.science_id = %s
            GROUP BY t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime;
        """)
        return await self.execute_query(query, sc_id, fetchall=True)

    async def select_active_tests_for_science(self, sc_id, language):
        query = ("""
            SELECT t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime, 
                   COUNT(q.id) AS questions_count
            FROM tests t
            LEFT JOIN questions q ON t.id = q.test_id
            WHERE t.science_id = %s AND t.language = %s AND t.isActive = TRUE
            GROUP BY t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime
            ORDER BY t.createdTime;
        """)
        return await self.execute_query(query, sc_id, language, fetchall=True)

    async def select_test(self, test_id):
        query = ("""
            SELECT t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime, 
                   COUNT(q.id) AS questions_count, s.nameUz, s.nameRu
            FROM tests t
            LEFT JOIN questions q ON t.id = q.test_id
            LEFT JOIN sciences s ON t.science_id = s.id
            WHERE t.id = %s
            GROUP BY t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime, s.nameUz, s.nameRu;
        """)
        return await self.execute_query(query, test_id, fetchone=True)

    async def delete_test(self, test_id):
        # Update questions to set test_id to NULL
        update_query = "DELETE FROM questions WHERE test_id = %s"
        await self.execute_query(update_query, test_id)

        # Delete the test
        delete_query = "DELETE FROM tests WHERE id = %s"
        await self.execute_query(delete_query, test_id)

    async def get_active_token(self):
        query = "SELECT id, token, isActive, createdTime, updatedTime FROM tokens WHERE isActive = TRUE;"
        return await self.execute_query(query, fetchone=True)

    async def add_active_token(self, token):
        # Deactivate all active tokens
        await self.execute_query("UPDATE tokens SET isActive = FALSE updatedTime = %s WHERE isActive = TRUE",
                                 datetime.now())
        # Insert the new active token
        query = "INSERT INTO tokens (token, isActive, createdTime, updatedTime) VALUES (%s, TRUE, %s, NULL)"
        return await self.execute_query(query, token, datetime.now())


