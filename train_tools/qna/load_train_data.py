import pymysql
import openpyxl

# from config.DatabaseConfig import *
DB_HOST = "localhost"
DB_USER = "myuser118"
DB_PASSWORD = "1234"
DB_NAME = "mango"


def all_clear_train_data(db):
    sql = """
        delete from mango_train_data
    """
    with db.cursor() as cursor:
        cursor.execute(sql)

    sql = """
        ALTER TABLE mango_train_data AUTO_INCREMENT=1
    """
    with db.cursor() as cursor:
        cursor.execute(sql)

def insert_data(db, xls_row):
    intent, emotion, ner, answer, answer_img_url = xls_row

    sql = """
        INSERT mango_train_data(intent, emotion, ner, answer, answer_img_url)
        values(
            "{}", "{}", "{}", "{}", "{}"
        )
    """.format(intent.value, emotion.value, ner.value, answer.value, answer_img_url.value)

    sql = sql.replace("'None'", "null")

    with db.cursor() as cursor:
        cursor.execute(sql)
        db.commit()

train_file = './train_data.xlsx'
db = None
a = 0
try:
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
    )
    a += 1
    all_clear_train_data(db)

    wb = openpyxl.load_workbook(train_file)
    a += 1
    sheet = wb['Sheet1']
    a += 1
    for row in sheet.iter_rows(min_row=2):
        insert_data(db, row)
    a += 1

    wb.close()

except Exception as e:
    print(e, a)

finally:
    if db is not None:
        db.close()