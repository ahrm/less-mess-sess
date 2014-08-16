# -*- coding: utf8
import sqlite3
import khayyam
import course
dbfilename = 'C:\\Users\\mrsar_000\\Desktop\\stuff\\devel\\python\\sess-autoselect-project\\lessmesssess.db'
create_course_table_query = '''CREATE TABLE IF NOT EXISTS course(id INTEGR PRIMARY KEY ,
                            course_name TEXT,
                            department TEXT,
                            prof_name TEXT,
                            course_hours TEXT,
                            final_exam_date TEXT,
                            final_exam_time TEXT,
                            course_id TEXT,
                            class_type TEXT,
                            allowed_sex TEXT,
                            allowed_fields TEXT,
                            vahed INTEGER,
                            grhoup TEXT,
                            cpacity INTEGER,
                            enrolled_num INTEGER)'''

insert_course_query = '''INSERT OR REPLACE INTO course(id ,
                            course_name,
                            department,
                            prof_name,
                            course_hours,
                            final_exam_date,
                            final_exam_time,
                            course_id,
                            class_type,
                            allowed_sex,
                            allowed_fields,
                            vahed,
                            grhoup,
                            cpacity,
                            enrolled_num) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

select_course_query = '''SELECT id,course_name,department,prof_name,course_hours,
                        final_exam_date,final_exam_time,
                        course_id,class_type,allowed_sex,allowed_fields,
                        vahed,grhoup,cpacity,enrolled_num FROM course'''
drop_table_query = '''DROP TABLE course'''

final_exam_format_type = '%Y/%m/%d'


def create_tables():
    db = sqlite3.connect(dbfilename)
    cursor = db.cursor()
    cursor.execute(create_course_table_query)
    db.commit()
    db.close()


def save_course_to_db(cour):
    #print cour.name
    #print type(cour.name.decode('utf8'))
    id_i = hash(cour)
    coursename_s = cour.name
    coursedepartment_s = cour.department
    profname_s = cour.professor
    if not cour.course_hours:
        coursehours_s = None
    else:
        coursehours_s = ('?'.join([x.str2() for x in cour.course_hours]))
    if cour.final_exam_date is None:
        final_exam_date_s = None
    else:
        final_exam_date_s = cour.final_exam_date.strftime(final_exam_format_type)
    if cour.final_exam_time is None:
        final_exam_time_s = None
    else:
        final_exam_time_s = ('?'.join(cour.final_exam_time))

    course_id_s = cour.course_id
    class_type_s = cour.class_type
    allowed_sex_s = cour.allowed_sex
    allowed_fields_s = cour.allowed_fields
    vahed_i = cour.vahed
    group_s = cour.group
    capacity_i = cour.capacity
    enrolled_num_i = cour.enrolled_num

    try:
        db = sqlite3.connect(dbfilename)
        cursor = db.cursor()
        cursor.execute(insert_course_query, (id_i,
                                             coursename_s,
                                             coursedepartment_s,
                                             profname_s,
                                             coursehours_s,
                                             final_exam_date_s,
                                             final_exam_time_s,
                                             course_id_s,
                                             class_type_s,
                                             allowed_sex_s,
                                             allowed_fields_s,
                                             vahed_i,
                                             group_s,
                                             capacity_i,
                                             enrolled_num_i))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def drop_table():
    try:
        db = sqlite3.connect(dbfilename)
        cursor = db.cursor()
        cursor.execute(drop_table_query)
        db.commit()
    except Exception as e:
        db.rollback()
        print e
        raise e
    finally:
        db.close()
def load_course_from_db():
    courses = []
    try:

        db = sqlite3.connect(dbfilename)

        cursor = db.cursor()

        cursor.execute(select_course_query)
        #print 'preloop'
        #db.commit()

        for row in cursor:
            #print 'row'
            id_i = row[0]
            coursename_s = row[1]
            coursedepartment_s = row[2]
            profname_s = row[3]
            coursehours_s = row[4]
            final_exam_date_s = row[5]
            final_exam_time_s = row[6]
            course_id_s = row[7]
            class_type_s = row[8]
            allowed_sex_s = row[9]
            allowed_fields_s = row[10]
            vahed_i = row[11]
            group_s = row[12]
            capacity_i = row[13]
            enrolled_num_i = row[14]
            
            if final_exam_date_s is None:
                final_exam_date_p = None
            else:
                final_exam_date_p = khayyam.JalaliDatetime.strptime(
                    final_exam_date_s,final_exam_format_type)
            if final_exam_time_s is None:
                final_exam_time_p = None
            else:
                final_exam_time_p = final_exam_time_s.split('?')

            if not coursehours_s:
                course_hours_temp = []
            else:
                course_hours_temp = coursehours_s.split('?')

            course_hours_l = []
            for hour_temp in course_hours_temp:
                course_hours_l.append(course.ClassTime.from_string(hour_temp))
            courses.append(course.Course(coursename_s,
                                         coursedepartment_s,
                                         profname_s,
                                         course_hours_l,
                                         final_exam_date_p,
                                         final_exam_time_p,
                                         course_id_s,
                                         class_type_s,
                                         allowed_sex_s,
                                         allowed_fields_s,
                                         vahed_i,
                                         group_s,
                                         capacity_i,
                                         enrolled_num_i))
            
            

    except Exception as e:
        db.rollback()
        print e
        raise e
    finally:
        db.close()
        return courses

#WARNING: drops the tables
if __name__ == '__main__':
    drop_table()
    create_tables()