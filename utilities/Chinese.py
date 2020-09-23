#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# author: JianGe, created on: 2018/10/25
from .xpinyin import Pinyin

p = Pinyin()


def allPinyin(inputStr):
    res = ''
    for item in p.get_pinyin(inputStr, u""):
        res += item
    return res


def allInitials(inputStr):
    return p.get_initials(inputStr, u"")


if __name__ == "__main__":
    str_input = u'WOmeneabac世界欢迎你2-9'

    print(allPinyin('我去你大爷88的额'))
    print(allPinyin(u'山东钢铁'))
    print(allInitials(u'山东钢铁'))
