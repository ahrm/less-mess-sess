# -*- coding: utf8 -*-
import course
import codecs
from course_filters import *
courses = course.Course.get_from_db()

log3 = codecs.open('log3.log', mode='w', encoding='utf8')
for cour in filter(profname_filter(u'اقبال'),courses):
    # print 'reading'
    log3.write(cour.__str__() + '\n')
