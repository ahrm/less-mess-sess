import sqlite3


create_course_table_query = '''CREATE TABLE IF NOT EXISTS course(id INTEGR PRIMARY KEY ,
							course_name TEXT,
							prof_name TEXT,
							course_hours TEXT,
							final_exam_date TEXT,
							final_exam_time TEXT,
							course_id TEXT,
							class_type TEXT,
							allowed_sex TEXT,
							vahed INTEGER,
							group TEXT,
							cpacity INTEGER,
							enroller_num INTEGER'''


def create_tables():
	db = sqlite3.connect('lessmesssess.db')
	cursor = db.cursor()
	cursor.execute(create_course_table_query)
	db.commit()
	db.close()

def save_course_to_db(cour):
	pass