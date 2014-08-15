# -*- coding: utf8 -*-
import splinter
import my_data
import course
import re
import pyregex
import codecs
from myutils import fa2en_numbers
import khayyam
from course_filters import *

term_schedule_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/\
td[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/\
tbody/tr[2]/td/ul/li[17]/a'
sess_login_path = 'http://sess.shirazu.ac.ir'
sess_login_username_id = 'edId'
sess_login_password_id = 'edPass'
sess_login_enter_id = 'edEnter'
sess_department_select_id = 'edDepartment'
sess_computer_department_xpath = '/html/body/form/table/tbody/tr[3]/td/table/\
tbody/tr[3]/td[6]/select/option[2]'
sess_term_select_xpath = '/html/body/form/table/tbody/tr[3]/td/table/tbody/\
tr[3]/td[3]/select/option[3]'
sess_department_select_button_id = 'edDisplay'
course_element_xpath = '/html/body/form/table/tbody/tr[4]/td/table/tbody/\
tr[4]/td[2]'
course_element_xpath2 = '/html/body/form/table/tbody/tr[4]/td/table/tbody/\
tr[*]/td[2]'
course_teacher_name_xpath = '/html/body/form/table/tbody/tr[2]/td/table/\
tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[6]/div'
course_name_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/\
td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/div'
course_hours_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/\
td/table/tbody/tr[4]/td/table/tbody/tr[3]/td[3]/div'
course_exam_date_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/\
tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr[4]/td[3]/div'
course_exam_time_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/\
tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr[4]/td[6]/div'
course_id_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/\
td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[3]/div'
course_type_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/\
td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[3]/div'
vahed_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/\
table/tbody/tr[2]/td/table/tbody/tr[2]/td[6]/div'
group_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td/\
table/tbody/tr[2]/td/table/tbody/tr[3]/td[6]/div'
course_sex_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/\
td/table/tbody/tr[3]/td/table/tbody/tr[2]/td[3]/div'
course_allowed_fields_xpath = '/html/body/form/table/tbody/tr[2]/td/table/\
tbody/tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[3]/div'
course_capacity_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/\
tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr[5]/td[3]/div'
course_enrolled_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/\
tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr[5]/td[6]/div'


browser = splinter.Browser()

browser.visit(sess_login_path)
browser.find_by_id(sess_login_username_id).fill(
    my_data.my_username)  # fill the username
browser.find_by_id(sess_login_password_id).fill(
    my_data.my_pass)  # fill the password

browser.find_by_id(sess_login_enter_id).click()  # click the login button
browser.find_by_xpath(term_schedule_xpath).click()  # go to schedule page


# select the department
browser.find_by_xpath(sess_computer_department_xpath).first.click()
browser.find_by_xpath(sess_term_select_xpath).first.click()  # select the term
browser.find_by_id(sess_department_select_button_id).click()

# print len(browser.find_by_xpath(course_element_xpath2))
elems = browser.find_by_xpath(course_element_xpath2)

log = codecs.open('log.log', mode='w', encoding='utf8')
log2 = codecs.open('log2.log', mode='w', encoding='utf8')

courses = []
sessions = []
# todo: do not encode any of the strings
for i in range(1, len(elems)):  # 10 -> len(elems)
    elems = browser.find_by_xpath(course_element_xpath2)
    elems[i].click()
    # todo: handle the case there are more than one teachers
    try:
        teacher_string = browser.find_by_xpath(
            course_teacher_name_xpath).text  # .encode('utf8')
        prof_name_match = re.match(pyregex.professor_name_re, teacher_string)
        prof_name = ' '.join((prof_name_match.group('fname'),
                              prof_name_match.group('lname')))
    except Exception as e:
        teacher_string = None
        prof_name_match = None
        prof_name = None

    try:
        course_name = browser.find_by_xpath(
            course_name_xpath).text  # .encode('utf8')
    except Exception as e:
        course_name = None

    try:

        course_hours_string = fa2en_numbers(browser.find_by_xpath(
            course_hours_xpath).text)  # .encode('utf8')
        cours_hours_splitted = course_hours_string.split('\n')
        class_times = []
        for class_t in cours_hours_splitted:
            course_hours_match = re.match(
                pyregex.class_hours_re, class_t)

            class_hours = (course_hours_match.group('dayname'),
                           course_hours_match.group('starttime'),
                           course_hours_match.group('endtime'))
            class_time = course.ClassTime(course_hours_match.group('dayname'),
                                          course_hours_match.group(
                                              'starttime'),
                                          course_hours_match.group('endtime'))
            class_location = course_hours_match.group('location')
            class_times.append(class_time)
    except Exception as e:
        course_hours_string = None
        course_hours_match = None
        class_hours = None
        class_location = None
        class_time = None

    try:
        final_exam_date_string = fa2en_numbers(browser.find_by_xpath(
            course_exam_date_xpath).text)

        final_exam_datetime = khayyam.JalaliDatetime.strptime(
            final_exam_date_string, '%Y/%m/%d')

        course_final_exam_date_match = re.match(
            pyregex.final_exam_date_re, final_exam_date_string)
        final_exam_date = (course_final_exam_date_match.group('year'),
                           course_final_exam_date_match.group('month'),
                           course_final_exam_date_match.group('day'))
    except Exception as e:
        final_exam_date_string = None
        course_final_exam_date_match = None
        final_exam_date = None
        final_exam_datetime = None

    try:
        final_exam_time_string = fa2en_numbers(browser.find_by_xpath(
            course_exam_time_xpath).text)
        course_final_exam_time_match = re.match(
            pyregex.final_exam_time_re, final_exam_time_string)
        final_exam_time = (course_final_exam_time_match.group('start'),
                           course_final_exam_time_match.group('end'))
    except Exception as e:
        final_exam_time_string = None
        course_final_exam_time_match = None
        final_exam_time = None

    try:
        course_id_string = browser.find_by_xpath(
            course_id_xpath).text  # .encode('utf8')
    except Exception as e:
        course_id_string = None

    try:
        course_type_string = browser.find_by_xpath(
            course_type_xpath).text  # .encode('utf8')
    except Exception as e:
        course_type_string = None
    try:
        vahed_string = browser.find_by_xpath(vahed_xpath).text
    except Exception as e:
        vahed_string = None
    try:
        group_string = browser.find_by_xpath(
            group_xpath).text  # .encode('utf8')
    except Exception as e:
        group_string = None
    try:
        course_sex_string = browser.find_by_xpath(
            course_sex_xpath).text  # .encode('utf8')
    except Exception as e:
        course_sex_string = None
    try:
        course_allowed_fields_string = browser.find_by_xpath(
            course_allowed_fields_xpath).text  # .encode('utf8')
    except Exception as e:
        course_allowed_fields_string = None
    try:
        course_capacity_string = browser.find_by_xpath(
            course_capacity_xpath).text
    except Exception as e:
        course_capacity_string = None
    try:
        course_enrolled_string = browser.find_by_xpath(
            course_enrolled_xpath).text
    except Exception as e:
        course_enrolled_string = None

    new_course = course.Course(course_name,
                               prof_name,
                               class_times,
                               final_exam_datetime,
                               final_exam_time,
                               course_id_string,
                               course_type_string,
                               course_sex_string,
                               course_allowed_fields_string,
                               int(fa2en_numbers(vahed_string)),
                               group_string,
                               int(fa2en_numbers(course_capacity_string)),
                               int(fa2en_numbers(course_enrolled_string))
                               )
    courses.append(new_course)
    sessions += new_course.get_sessions()
    # log.write(courses[-1].__str__())

    browser.back()

# sessions.sort()
#filtered_courses = filter(profname_filter('زهره'), courses)
# for session in sessions:
#     log.write(session.parent_course.__str__() + '\n')
# for fcourse in filtered_courses:
#     log2.write(fcourse.__str__() + '\n')

for cour in courses:
    print 'writing'
    cour.save_to_db()
print 'done!'
