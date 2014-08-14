# -*- coding: utf8 -*-
import course
import re


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


def and_filter(filter1, filter2):
    def res_filter(cour):
        return filter1(cour) and filter2(cour)
    return res_filter


def or_filter(filter1, filter2):
    def res_filter(cour):
        return filter1(cour) or filter2(cour)
    return res_filter


def not_filter(filter1):
    def res_filter(cour):
        return not filter1(cour)
    return res_filter
