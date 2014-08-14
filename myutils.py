# -*- coding: utf8 -*-


def fa2en_numbers(instr):

    translate_table = {ord(u'۰') + x: ord('0') + x for x in range(10)}
    return instr.translate(translate_table)
