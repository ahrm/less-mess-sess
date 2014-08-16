# -*- coding: utf8 -*-
import course
import re
from pyregex import course_range_re


def tiemrange_filter(start, end, include_nons=False):  # start,end = (hh,mm)
    def res_filter(cour):
        sessions = cour.get_class_sessions()
        if include_nons is False and not sessions:
            return False
        for session in sessions:
            if not session.is_in_range(start, end):
                return False
        return True
    return res_filter


def day_filter(days):  # days = ['شنبه' , 'یک شنبه'] or [0,1]
    if type(days[0]) != int:
        days = [course.ClassTime.week_day_order[x] for x in days]

    def res_filter(cour, include_nons=False):
        sessions = cour.get_class_sessions()
        if include_nons is False and not sessions:
            return False
        for session in sessions:
            if not session.day_num in days:
                return False
        return True
    return res_filter


def coursename_filter(name):
    course_re = re.compile('.*' + name + '.*')

    def res_filter(cour):
        if re.match(course_re, cour.name):
            return True
        else:
            return False
    return res_filter


def cnf(name):
    return coursename_filter(name)


def profname_filter(name):
    course_re = re.compile('.*' + name + '.*')

    def res_filter(cour, include_nons=False):
        if not include_nons and not cour.professor:
            return False
        if re.match(course_re, cour.professor):
            return True
        else:
            return False
    return res_filter


def and_filter(*filters):
    def res_filter(cour):
        for filt in filters:
            if not filt(cour):
                return False
        return True
    return res_filter


def or_filter(*filters):
    def res_filter(cour):
        for filt in filters:
            if filt(cour):
                return True
        return False
    return res_filter


def orf(*filters):
    return or_filter(*filters)


def andf(*filters):
    return and_filter(*filters)


def not_filter(filter1):
    def res_filter(cour):
        return not filter1(cour)
    return res_filter


def allways_true(course):
    return True


def allways_false(course):
    return False


def parse_dayfilter_string(string):
    try:
        days = string.split(',')
        return day_filter([int(i) for i in days])
    except Exception as e:
        return allways_true


def parse_timefilter_string(string):
    try:
        substrings = string.split(',')
        timerange_filters = []
        for substring in substrings:
            m = re.match(course_range_re, substring)
            starthour = int(m.group('starthour'))
            startmin = int(m.group('startmin'))
            endhour = int(m.group('endhour'))
            endmin = int(m.group('endmin'))
            temp_filter = tiemrange_filter(
                (starthour, startmin), (endhour, endmin))
            timerange_filters.append(temp_filter)
        return or_filter(*timerange_filters)
    except Exception as e:
        return allways_true


def parse_proffilter_string(string):
    try:
        substrings = string.split(',')
        courprof_filters = []
        for substring in substrings:
            stripped = substring.strip()
            temp_filter = profname_filter(stripped)
            courprof_filters.append(temp_filter)
        return or_filter(*courprof_filters)
    except Exception as e:
        return allways_true

def parse_courfilter_string(string):
    try:
        substrings = string.split(',')
        courprof_filters = []
        for substring in substrings:
            stripped = substring.strip()
            temp_filter = coursename_filter(stripped)
            courprof_filters.append(temp_filter)
        return or_filter(*courprof_filters)
    except Exception as e:
        return allways_true


