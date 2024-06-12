import os
import asyncio
import xlsxwriter


async def write_applicant_to_excel(tgId):
    from loader import db
    applicant = await db.get_applicant_for_excel(tgId)
    directory = 'data/applicants/'
    filename = f'{directory}applicant_{tgId}.xlsx'

    if not os.path.exists(directory):
        os.makedirs(directory)

    columns = ["tgId", "phoneNumber", "additionalPhoneNumber", "pinfl", "firstName", "lastName",
               "middleName", "passport", "directionOfEducation", "typeOfEducation",
               "languageOfEducation", "contractFile", "olympian", "createdTime", "applicationStatus"]

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    for col_num, header in enumerate(columns):
        worksheet.write(0, col_num, header)

    for col_num, data in enumerate(applicant):
        worksheet.write(1, col_num, data)

    workbook.close()
    return filename
