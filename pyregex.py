# -*- coding: utf8 -*-
professor_name_re = r'(?P<lname>.*)\*(?P<fname>.*)\*(?P<field>.*)\((?P<num>[0-9]*)\)\*'
class_hours_re = r'(?P<dayname>.*)\-(?P<starttime>[0-9]*:[0-9]*):(?P<endtime>[0-9]*:[0-9]*)\((?P<location>.*)\)'
final_exam_date_re = r'(?P<year>[0-9]*)/(?P<month>[0-9]*)/(?P<day>[0-9]*)'
final_exam_time_re = r'(?P<start>[0-9]*:[0-9]*) - (?P<end>[0-9]*:[0-9]*)'
course_range_re = r'\W*\((?P<starthour>[0-9]*):(?P<startmin>[0-9]*)-(?P<endhour>[0-9]*):(?P<endmin>[0-9]*)\)'
#final_exam_date_re = r'(?P<year>[۰-۹]*)/(?P<month>[۰-۹]*)/(?P<day>[۰-۹]*)'
#final_exam_time_re = r'(?P<start>[۰-۹]*:[۰-۹]*) - (?P<end>[۰-۹]*:[۰-۹]*)'
