#!/usr/bin/env python

from PyQt4.QtCore import QDateTime, QTime, QString

def systime():
    now = QDateTime.currentDateTime()
    systime = now.toString("yyyyMMddhhmmss.zz")
    return systime

def systimef():
    now = QDateTime.currentDateTime()
    systime = now.toString("yyyy/MM/dd hh:mm:ss.zz")
    return systime

def sysdate():
    now = QDateTime.currentDateTime()
    sysdate = now.toString("yyyyMMdd")
    return sysdate

def systimeonly():
    now = QDateTime.currentDateTime()
    systo = now.toString("hhmmss.zz")
    return systo

def removeZZfromJDStime(instr):
    if isTimeFormatZZ(instr):
        form=QString("hh:mm:ss.zz")
        inqstr=QString(instr)
        dts = QTime.fromString(inqstr, form)
        newtime = dts.toString("hh:mm:ss")
        return newtime
    else:
        return instr

def removeZZZfromJDStime(instr):
    if isTimeFormatZZZ(instr):
        form=QString("hh:mm:ss.zzz")
        inqstr=QString(instr)
        dts = QTime.fromString(inqstr, form)
        newtime = dts.toString("hh:mm:ss")
        return newtime

def isTimeFormatZZ(instr):
    form=QString("hh:mm:ss.zz")
    inqstr=QString(instr)
    dts = QTime.fromString(inqstr, form)

    if dts.isValid():
        return True
    else:
        return False

def isTimeFormatZZZ(instr):
    form=QString("hh:mm:ss.zzz")
    inqstr=QString(instr)
    dts = QTime.fromString(inqstr, form)

    if dts.isValid():
        return True
    else:
        return False

def isDateTimeFormatZZ(instr):
    form=QString("yyyy/MM/dd hh:mm:ss.zz")
    inqstr=QString(instr)
    dts = QDateTime.fromString(inqstr, form)

    if dts.isValid():
        return True
    else:
        return False

def isDateTimeFormatZZZ(instr):
    form=QString("yyyy/MM/dd hh:mm:ss.zzz")
    inqstr=QString(instr)
    dts = QDateTime.fromString(inqstr, form)

    if dts.isValid():
        return True
    else:
        return False

def syssecs():
    now = QDateTime.currentDateTime()
    syssecs = now.toString("ss.zz")
    return syssecs
