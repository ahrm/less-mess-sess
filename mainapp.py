from flask import Flask, render_template, request, redirect, session, url_for
from course import Course
from course_filters import *
#from logtest import log23

courses = Course.get_from_db()

app = Flask(__name__)

selected_user_courses = {}
departments = ['computer', 'physics', 'tarbiat']


# @app.route('/')
# def main_page():
#     user = ''
#     if 'username' in session:
#         user = session['username']
#     return render_template('main_template.html',
#                            selected_courses=[],
#                            unselected_courses=courses,
#                            user=user)

def schedule():
    reqargs = request.args.getlist('clsl')
    selected_courses = Course.select_courses(courses, reqargs)
    return render_template('schedule.html', selected_courses=selected_courses)


@app.route('/')
def handler():
    button_string = request.args.get('btn')
    if button_string == 'Schedule':
        return schedule()
    else:
        return test()


@app.route('/test')
def test():

    reqargs = request.args.getlist('clsl')

    department_string = request.args.get('dep')
    course_name_filter_string = request.args.get('cnf')
    prof_name_filter_string = request.args.get('pnf')
    course_day_filter_string = request.args.get('cdf')
    course_time_filter_string = request.args.get('ctf')
    sex_filter_int = (request.args.get('jens') and int(request.args.get('jens'))) or 0

    dep_filter = department_filter(department_string)
    course_name_filter = parse_courfilter_string(course_name_filter_string)
    prof_name_filter = parse_proffilter_string(prof_name_filter_string)
    course_day_filter = parse_dayfilter_string(course_day_filter_string)
    course_time_filter = parse_timefilter_string(course_time_filter_string)
    sex_filt = sex_filter(sex_filter_int)

    final_filter = and_filter(course_name_filter,
                              prof_name_filter,
                              course_day_filter,
                              course_time_filter,
                              dep_filter,
                              sex_filt)

    selected_courses = Course.select_courses(courses, reqargs)
    user = ''
    if 'username' in session:
        user = session['username']
    if selected_courses:
        selected_user_courses[user] = selected_courses
    unselected_courses = [
        cour for cour in courses if not cour in selected_courses]
    return render_template('main_template.html',
                           selected_courses=selected_courses,
                           unselected_courses=filter(
                               final_filter, unselected_courses),
                           user=user,
                           filter_strings=[course_name_filter_string,
                                           prof_name_filter_string,
                                           course_day_filter_string,
                                           course_time_filter_string,
                                           department_string,
                                           sex_filter_int],
                           departments=departments)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('main_page'))
    else:
        return render_template('login_page.html')

app.secret_key = 'thisisthemostsecretkeyintheworld'
if __name__ == '__main__':
    app.run(debug=True)
