# -*- coding: utf8 -*-

import myutils


class ClassTime:
    week_day_order = {
        u'شنبه': 0,
        u'يک شنبه': 1,
        u'دو شنبه': 2,
        u'سه شنبه': 3,
        u'چهار شنبه': 4,
        u'پنج شنبه': 5}

    def __init__(self,
                 week_day,
                 start_time,
                 end_time):
        self.day = week_day
        self.day_num = ClassTime.week_day_order[week_day]
        self.start = start_time
        self.end = end_time
        start_time_split = [int(x) for x in start_time.split(':')]
        end_time_split = [int(x) for x in end_time.split(':')]
        self.start_tup = (start_time_split[0], start_time_split[1])
        self.end_tup = (end_time_split[0], end_time_split[1])

    def __str__(self):
        return self.day + 's from ' + self.start + ' to ' + self.end

    def __cmp__(self, other):
        selfsplitted = self.start.split(':')
        othersplitted = other.start.split(':')
        return cmp((self.day_num, int(selfsplitted[0]), int(selfsplitted[1])),
                   (other.day_num, int(othersplitted[0]), int(othersplitted[1])))

    def is_in_range(self, start, end):
        return self.start_tup >= start and self.end_tup <= end

    # def __key__(self):
    # 	start_times = self.start_time.split(':')
    # return ClassTime.week_day_order[self.day] * 100000 + int(start_times[0])
    # * 1000 + int(start_times[1])


class Course:

    class CourseSession:

        def __init__(self, parent_course, session_time):
            self.parent_course = parent_course
            self.session_time = session_time

        def __cmp__(self, other):
            return self.session_time.__cmp__(other.session_time)

    def __init__(self,
                 course_name,
                 prof_name=None,
                 course_hours=None,
                 final_exam_date=None,
                 final_exam_time=None,
                 course_id=None,
                 class_type=None,
                 allowed_sex=None,
                 allowed_fields=None,
                 vahed=None,
                 group=None,
                 capacity=None,
                 enrolled_num=None):
        self.name = course_name
        if (prof_name):
            self.professor = prof_name[0] + ' ' + prof_name[1]
        else:
            self.professor = None
        self.course_hours = course_hours
        self.final_exam_date = final_exam_date
        self.final_exam_time = final_exam_time
        self.course_id = course_id
        self.class_type = class_type
        self.allowed_sex = allowed_sex
        self.allowed_fields = allowed_fields
        self.vahed = vahed
        self.group = group
        self.capacity = capacity
        self.enrolled_num = enrolled_num
    # todo: rename the confusing name

    def get_sessions(self):
        return [Course.CourseSession(self, session_time) for session_time in self.course_hours]

    def get_class_sessions(self):
        return self.course_hours

    def __hash__(self):
        return hash(self.name) + hash(self.professor) +\
            hash(self.final_exam_date)

    def __str__(self):
        r = 'Course Name: ' + self.name.decode('utf8') + '\n' + \
            'Professor: ' + self.professor.__str__().decode('utf8') + '\n'
        for class_time in self.course_hours:
            r += (class_time.__str__() + ' ')
        return r + '\n_________________________________________________________'
