import json
import random
from datetime import datetime
from typing import Optional, List, Dict, Any

import aiomysql
from environs import Env

from utils.db_api.encrypt_data import encrypt_data, decrypt_data

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
        query = "SELECT id, nameUz, nameRu, active FROM educational_areas WHERE deleted = FALSE;"
        return await self.execute_query(query, fetchall=True)

    async def select_active_directions(self):
        query = "SELECT id, nameUz, nameRu FROM educational_areas WHERE active = TRUE AND deleted = FALSE;"
        return await self.execute_query(query, fetchall=True)

    async def select_direction(self, id):
        query = "SELECT id, nameUz, nameRu, active FROM educational_areas WHERE id = %s;"
        return await self.execute_query(query, id, fetchone=True)

    async def get_sciences_for_direction(self, direction_id):
        query = """
            SELECT s.id, s.nameUz, s.nameRu
            FROM sciences s
            INNER JOIN educational_areas_sciences eas ON s.id = eas.science_id
            WHERE eas.directionofeducation_id = %s AND s.deleted = FALSE
            ORDER BY eas.id;
        """
        return await self.execute_query(query, direction_id, fetchall=True)

    async def get_sciences_for_exam(self, direction_id):
        query = """
            SELECT s.id, s.nameUz, s.nameRu
            FROM sciences s
            INNER JOIN educational_areas_sciences eas ON s.id = eas.science_id
            WHERE eas.directionofeducation_id = %s AND s.deleted = FALSE
            ORDER BY eas.id
            LIMIT 3;
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
            ) AND s.deleted = FALSE;
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
        query = "INSERT INTO educational_areas (id, nameUz, nameRu, active, deleted) VALUES (%s, %s, %s, FALSE, FALSE);"
        await self.execute_query(query, newId, nameUz, nameRu)

    async def set_direction(self, id, nameUz, nameRu, *args, **kwargs):
        if await self.select_direction(id):
            query = "UPDATE educational_areas SET nameUz = %s, nameRu = %s WHERE id = %s;"
            await self.execute_query(query, nameUz, nameRu, id)

    async def update_active_direction(self, id, action: bool):
        query = "UPDATE educational_areas SET active = %s WHERE id = %s;"
        await self.execute_query(query, action, id)

    async def delete_direction(self, id):
        query = "UPDATE educational_areas SET active = FALSE, deleted = TRUE WHERE id = %s;"
        await self.execute_query(query, id)

    async def select_types_of_education(self):
        query = "SELECT id, nameUz, nameRu, active FROM types_of_education WHERE deleted = FALSE;"
        return await self.execute_query(query, fetchall=True)

    async def select_types_no_contract(self, direction_id):
        query = """
            SELECT t.id, t.nameUz, t.nameRu, t.active 
            FROM types_of_education t
            WHERE t.id NOT IN (
                SELECT c.typeOfEducation_id 
                FROM contract_prices c
                WHERE c.directionOfEducation_id = %s
            ) AND t.deleted = FALSE;
        """
        return await self.execute_query(query, direction_id, fetchall=True)

    async def select_type_of_education(self, id):
        query = "SELECT id, nameUz, nameRu, active FROM types_of_education WHERE id = %s;"
        return await self.execute_query(query, id, fetchone=True)

    async def add_type_of_education(self, newId, nameUz, nameRu, *args, **kwargs):
        if await self.select_type_of_education(newId):
            return 'already_exist'
        query = ("INSERT INTO types_of_education (id, nameUz, nameRu, active, deleted) "
                 "VALUES (%s, %s, %s, FALSE, FALSE);")
        await self.execute_query(query, newId, nameUz, nameRu)

    async def set_type_of_education(self, id, nameUz, nameRu, *args, **kwargs):
        if await self.select_type_of_education(id):
            query = "UPDATE types_of_education SET nameUz = %s, nameRu = %s WHERE id = %s;"
            await self.execute_query(query, nameUz, nameRu, id)

    async def update_active_type(self, id, action: bool):
        query = "UPDATE types_of_education SET active = %s WHERE id = %s;"
        await self.execute_query(query, action, id)

    async def delete_type_of_education(self, id):
        query = "UPDATE types_of_education SET active = FALSE, deleted = TRUE WHERE id = %s;"
        await self.execute_query(query, id)

    async def select_contact_price(self, direction_id, type_id):
        query = "SELECT id, amount FROM contract_prices WHERE directionOfEducation_id = %s AND typeOfEducation_id = %s"
        return await self.execute_query(query, direction_id, type_id, fetchone=True)

    async def select_contract_prices_for_direction(self, direction_id):
        query = """
        SELECT cp.id, cp.typeOfEducation_id, cp.amount, te.nameUz, te.nameRu 
        FROM contract_prices cp
        JOIN types_of_education te ON cp.typeOfEducation_id = te.id
        WHERE cp.directionOfEducation_id = %s AND te.deleted = FALSE;
        """
        return await self.execute_query(query, direction_id, fetchall=True)

    async def select_active_contract_prices_for_direction(self, direction_id):
        query = """
        SELECT cp.id, cp.typeOfEducation_id, cp.amount, te.nameUz, te.nameRu 
        FROM contract_prices cp
        JOIN types_of_education te ON cp.typeOfEducation_id = te.id
        WHERE cp.directionOfEducation_id = %s AND te.active = TRUE;
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

    async def get_applicant(self, tgId, passport=None, birthDate=None):
        query = (
            "SELECT tgId, phoneNumber, additionalPhoneNumber, pinfl, firstName, lastName, middleName, passport, "
            "directionOfEducation_id, typeOfEducation_id, languageOfEducation, contractFile, olympian, createdTime, "
            "applicationStatus, applicantNumber, birthDate, gender, photo, applicantId, regionId, regionName, cityId, "
            "cityName "
            "FROM applicants WHERE tgId = %s OR (passport = %s AND birthDate = %s);"
        )
        result = await self.execute_query(query, tgId, passport, birthDate, fetchone=True)

        if result:
            result = (
                result[0],
                result[1],
                result[2],
                decrypt_data(result[3]) if result[3] else None,
                result[4],
                result[5],
                result[6],
                decrypt_data(result[7]),
                result[8],  result[9], result[10], result[11], result[12], result[13], result[14],
                result[15],
                decrypt_data(result[16]),
                result[17], result[18], result[19],
                result[20], result[21], result[22], result[23],
            )
        return result

    async def get_applicant_for_post_exam_result(self, tgId, passport=None, birthDate=None):
        query = (
            "SELECT a.tgId, a.phoneNumber, a.additionalPhoneNumber, a.pinfl, a.firstName, a.lastName, a.middleName, "
            "a.passport, a.directionOfEducation_id, a.typeOfEducation_id, a.languageOfEducation, a.contractFile, "
            "a.olympian, a.createdTime, a.applicationStatus, a.applicantNumber, a.birthDate, a.gender, a.photo, "
            "a.applicantId, a.regionId, a.regionName, a.cityId, a.cityName, "
            "e.nameUz AS directionOfEducationName, t.nameUz AS typeOfEducationName, "
            "o.vaucher, a.passportImageFront, a.passportImageBack "
            "FROM applicants a "
            "LEFT JOIN educational_areas e ON a.directionOfEducation_id = e.id "
            "LEFT JOIN types_of_education t ON a.typeOfEducation_id = t.id "
            "LEFT JOIN olympians o ON a.tgId = o.applicant_id "
            "WHERE a.tgId = %s OR (a.passport = %s AND a.birthDate = %s);"
        )
        result = await self.execute_query(query, tgId, passport, birthDate, fetchone=True)

        if result:
            result = {
                'tgId': result[0],
                'phoneNumber': result[1],
                'additionalPhoneNumber': result[2],
                'pinfl': decrypt_data(result[3]) if result[3] else None,
                'firstName': result[4],
                'lastName': result[5],
                'middleName': result[6],
                'passport': decrypt_data(result[7]) if result[7] else None,
                'directionOfEducation_id': result[8],
                'typeOfEducation_id': result[9],
                'languageOfEducation': result[10],
                'contractFile': result[11],
                'olympian': result[12],
                'createdTime': result[13],
                'applicationStatus': result[14],
                'applicantNumber': result[15],
                'birthDate': decrypt_data(result[16]) if result[16] else None,
                'gender': result[17],
                'photo': result[18],
                'applicantId': result[19],
                'regionId': result[20],
                'regionName': result[21],
                'cityId': result[22],
                'cityName': result[23],
                'directionOfEducationName': result[24],
                'typeOfEducationName': result[25],
                'vaucher': result[26],
                'passportImageFront': result[27],
                'passportImageBack': result[28]
            }
        return result

    async def update_application_status(self, tgId, new_status):
        query = "UPDATE applicants SET applicationStatus = %s WHERE tgId = %s;"
        await self.execute_query(query, new_status, tgId)

    async def add_draft_applicant(self, tgId, applicantId, applicantNumber, phoneNumber, additionalPhoneNumber,
                                  passport, birthDate, gender=None, photo=None,
                                  olympian=False, *args, **kwargs):

        passport_encrypted = encrypt_data(passport)
        birthDate_encrypted = encrypt_data(birthDate)
        gender = gender if gender in ['MALE', 'FEMALE'] else None

        query = (
            "INSERT INTO applicants "
            "(tgId, applicantId, applicantNumber, phoneNumber, additionalPhoneNumber, passport, birthDate, gender, "
            "photo, applicationStatus, olympian, createdTime, updatedTime) "
            "VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        )
        await self.execute_query(query, tgId, applicantId, applicantNumber, phoneNumber, additionalPhoneNumber,
                                 passport_encrypted, birthDate_encrypted, gender, photo, 'DRAFT', olympian,
                                 datetime.now(), datetime.now())

    async def submit_applicant(self, firstName, lastName, middleName, pinfl, passportPhotoFront,
                               passportBackPhoto, tgId, directionOfEducationId, typeOfEducationId,
                               languageOfEducationName, olympian, regionId, regionName, cityId, cityName,
                               dtmScore=None, dtmAbiturientNumber=None, *args, **kwargs):
        pinfl_encrypted = encrypt_data(pinfl)
        query = (
            "UPDATE applicants SET "
            "pinfl = %s, firstName = %s, lastName = %s, middleName = %s, passportImageFront = %s, "
            "passportImageBack = %s, directionOfEducation_id = %s, typeOfEducation_id = %s, languageOfEducation = %s, "
            "applicationStatus = %s, updatedTime = %s, olympian = %s, regionId = %s, regionName = %s, cityId = %s, "
            "cityName = %s, dtmScore = %s, dtmAbiturientNumber = %s "
            "WHERE tgId = %s;"
        )
        await self.execute_query(query, pinfl_encrypted, firstName, lastName, middleName,
                                 passportPhotoFront, passportBackPhoto, directionOfEducationId,
                                 typeOfEducationId, languageOfEducationName, 'SUBMITTED', datetime.now(), olympian,
                                 regionId, regionName, cityId, cityName, dtmScore, dtmAbiturientNumber, tgId)

    async def add_olympian_result(self, olympianId, vaucher, certificateImage=None, result=None, **kwargs):
        query = "INSERT INTO olympians (applicant_id, result, vaucher, certificateImage) VALUES (%s, %s, %s, %s);"
        await self.execute_query(query, olympianId, result, vaucher, certificateImage)

    async def get_applicant_exam_results(self, applicant_id):
        query = """
        SELECT id, applicant_id
        FROM exam_results 
        WHERE applicant_id = %s
        """
        return await self.execute_query(query, applicant_id, fetchall=True)

    async def get_exam_result_last(self, applicant_id):
        query = """
            SELECT id, applicant_id, userResponses, trueResponseCount, result, totalScore, intervalTime, createdTime 
            FROM exam_results 
            WHERE applicant_id = %s
            ORDER BY createdTime DESC
            LIMIT 1
            """
        return await self.execute_query(query, applicant_id, fetchone=True)

    async def add_exam_result(
            self,
            applicant_id: int,
            true_response_count: int,
            result: float,
            total_score: int,
            user_responses: Optional[List[Dict[str, Any]]] = None,
            interval_time: Optional[float] = None
    ) -> None:
        query = """
        INSERT INTO exam_results 
        (applicant_id, userResponses, trueResponseCount, result, totalScore, intervalTime, createdTime)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        user_responses_json = json.dumps(user_responses) if user_responses else None
        created_time = datetime.now()

        await self.execute_query(
            query,
            applicant_id,
            user_responses_json,
            true_response_count,
            result,
            total_score,
            interval_time,
            created_time
        )

    async def select_questions_for_test(self, test_id, count=None):
        if count:
            # Randomly select `count` number of questions
            query = ("SELECT id, test_id, image, question, trueResponse FROM questions WHERE test_id = %s AND active = "
                     "TRUE;")
            all_questions = await self.execute_query(query, test_id, fetchall=True)
            random_questions = random.sample(all_questions, min(count, len(all_questions)))
            return random_questions
        else:
            # Select all questions
            query = ("SELECT id, test_id, image, question, trueResponse FROM questions WHERE test_id = %s AND active = "
                     "TRUE;")
            return await self.execute_query(query, test_id, fetchall=True)

    async def select_question(self, ques_id):
        query = """
            SELECT q.id, q.test_id, q.image, q.question, q.trueResponse, t.science_id, t.language, s.nameUz, 
            q.response1, q.response2, q.response3, q.response4
            FROM questions q
            JOIN tests t ON q.test_id = t.id
            JOIN sciences s ON t.science_id = s.id
            WHERE q.id = %s;
            """
        return await self.execute_query(query, ques_id, fetchone=True)

    async def add_or_update_question(self, test_id, image, question, trueResponse, response1=None, response2=None,
                                     response3=None, response4=None, question_id=None, *args, **kwargs):
        if question_id:
            query = ("UPDATE questions SET test_id = %s, image = %s, question = %s, trueResponse = %s, "
                     "response1 = %s, response2 = %s, response3 = %s, response4 = %s WHERE id = %s;")
            await self.execute_query(query, test_id, image, question, trueResponse, response1, response2,
                                     response3, response4, question_id)
            return 'update'
        else:
            query = ("INSERT INTO questions (test_id, image, question, trueResponse, active, response1, response2, response3, response4) "
                     "VALUES (%s, %s, %s, %s, TRUE, %s, %s, %s, %s);")
            await self.execute_query(query, test_id, image, question, trueResponse, response1, response2, response3, response4)
            test_app = await self.select_test(test_id)
            if test_app[2] == test_app[6]:
                query_test = "UPDATE tests SET isActive = %s WHERE id = %s"
                await self.execute_query(query_test, True, test_app[0])
            return 'add'

    async def delete_question(self, ques_id, test_id):
        # Update the question to set active to FALSE
        query = "UPDATE questions SET active = FALSE WHERE id = %s;"
        await self.execute_query(query, ques_id)

        # Check the status of the test and update if necessary
        test_app = await self.select_test(test_id)
        if test_app[2] > test_app[6]:
            query_test = "UPDATE tests SET isActive = %s WHERE id = %s"
            await self.execute_query(query_test, False, test_id)

    async def select_sciences(self):
        query = "SELECT id, nameUz, nameRu FROM sciences WHERE deleted = FALSE;"
        return await self.execute_query(query, fetchall=True)

    async def select_science(self, sc_id):
        query = "SELECT id, nameUz, nameRu FROM sciences WHERE id = %s;"
        return await self.execute_query(query, sc_id, fetchone=True)

    async def add_or_update_science(self, nameUz, nameRu, science_id=None, *args):
        if science_id is None:
            query = "INSERT INTO sciences (nameUz, nameRu, deleted) VALUES (%s, %s, FALSE);"
            await self.execute_query(query, nameUz, nameRu)
        else:
            query = "UPDATE sciences SET nameUz = %s, nameRu = %s WHERE id = %s;"
            await self.execute_query(query, nameUz, nameRu, science_id)

    async def delete_science(self, sc_id):
        # Update the science to set deleted to TRUE
        query = "UPDATE sciences SET deleted = TRUE WHERE id = %s;"
        await self.execute_query(query, sc_id)

        # Update all tests related to this science to set deleted to TRUE
        update_tests_query = "UPDATE tests SET deleted = TRUE isActive = FALSE WHERE science_id = %s;"
        await self.execute_query(update_tests_query, sc_id)

    async def add_test(self, science_id, questionsCount, language, id=None, *args):
        query = ("INSERT INTO tests (science_id, questionsCount, language, isActive, "
                 "createdTime, deleted) VALUES (%s, %s, %s, %s, %s, FALSE);")
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
            LEFT JOIN questions q ON t.id = q.test_id AND q.active = TRUE
            WHERE t.science_id = %s AND t.deleted = FALSE
            GROUP BY t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime;
        """)
        return await self.execute_query(query, sc_id, fetchall=True)

    async def select_active_tests_for_science(self, sc_id, language):
        query = ("""
            SELECT t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime, 
                   COUNT(q.id) AS questions_count
            FROM tests t
            LEFT JOIN questions q ON t.id = q.test_id AND q.active = TRUE
            WHERE t.science_id = %s AND t.language = %s AND t.isActive = TRUE AND t.deleted = FALSE
            GROUP BY t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime
            ORDER BY t.createdTime;
        """)
        return await self.execute_query(query, sc_id, language, fetchall=True)

    async def select_test(self, test_id):
        query = ("""
            SELECT t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime, 
                   COUNT(q.id) AS questions_count, s.nameUz, s.nameRu
            FROM tests t
            LEFT JOIN questions q ON t.id = q.test_id AND q.active = TRUE
            LEFT JOIN sciences s ON t.science_id = s.id
            WHERE t.id = %s AND t.deleted = FALSE
            GROUP BY t.id, t.science_id, t.questionsCount, t.language, t.isActive, t.createdTime, s.nameUz, s.nameRu;
        """)
        return await self.execute_query(query, test_id, fetchone=True)

    async def delete_test(self, test_id):
        # Update the test to set deleted to TRUE and isActive to FALSE
        delete_query = "UPDATE tests SET deleted = TRUE, isActive = FALSE WHERE id = %s"
        await self.execute_query(delete_query, test_id)

        # Update all questions related to this test to set active to FALSE
        update_questions_query = "UPDATE questions SET active = FALSE WHERE test_id = %s"
        await self.execute_query(update_questions_query, test_id)

    async def get_active_token(self):
        query = "SELECT id, token, isActive, createdTime, updatedTime FROM tokens WHERE isActive = TRUE;"
        return await self.execute_query(query, fetchone=True)

    async def add_active_token(self, token):
        # Deactivate all active tokens
        await self.execute_query("UPDATE tokens SET isActive = FALSE, updatedTime = %s WHERE isActive = TRUE",
                                 datetime.now())
        # Insert the new active token
        query = "INSERT INTO tokens (token, isActive, createdTime, updatedTime) VALUES (%s, TRUE, %s, NULL)"
        return await self.execute_query(query, token, datetime.now())

    async def get_me(self, tgId):
        query = """
        SELECT 
            tgId, phoneNumber, additionalPhoneNumber, passport, birthDate, pinfl, firstName, lastName, 
            middleName, olympian, createdTime, photo
        FROM 
            applicants
        WHERE 
            tgId = %s;
        """
        result = await self.execute_query(query, tgId, fetchone=True)

        if result:
            # Decrypt sensitive data
            result = (
                result[0],
                result[1],
                result[2],
                decrypt_data(result[3]),
                decrypt_data(result[4]),
                decrypt_data(result[5]) if result[5] else None,
                result[6],
                result[7],
                result[8],
                result[9],
                result[10],
                result[11],
            )
        return result

    async def get_my_application(self, tgId):
        query = """
        SELECT 
            a.tgId, 
            e.nameUz AS directionOfEducationUz, e.nameRu AS directionOfEducationRu, 
            t.nameUz AS typeOfEducationUz, t.nameRu AS typeOfEducationRu,
            a.languageOfEducation, 
            a.olympian, a.updatedTime, a.applicationStatus
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
