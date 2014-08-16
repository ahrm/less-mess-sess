from flask import Flask, render_template, request, redirect, session, url_for
from course import Course

courses = Course.get_from_db()

app = Flask(__name__)

selected_user_courses = {}


@app.route('/')
def main_page():
    user = ''
    if 'username' in session:
        user = session['username']
    return render_template('main_template.html',
                           selected_courses=[],
                           unselected_courses=courses,
                           user=user)


@app.route('/test')
def test():
    reqargs = request.args.getlist('clsl')
    selected_courses = Course.select_courses(courses, reqargs)
    user = ''
    if 'username' in session:
        user = session['username']

    selected_user_courses[user] = selected_courses
    unselected_courses = [
        cour for cour in courses if not cour in selected_courses]
    return render_template('main_template.html',
                           selected_courses=selected_courses,
                           unselected_courses=unselected_courses,
                           user=user)


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
