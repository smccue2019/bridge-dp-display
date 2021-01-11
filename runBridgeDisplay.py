#!/usr/bin/env python

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import fabs

class Worker(QThread):

    updateAngle = pyqtSignal(float)
    new_jdp = pyqtSignal(QString, name = 'new_jdp')

    def __init__(self):
        QThread.__init__(self)

        self.heartbeat = QTimer()
        self.heartbeat.timeout.connect(self.on_heartbeat)

        # True then generate internal JDP messages.
        # False then listen for them on JasonNet
        self.run_heartbeat =False 

	self.run_lightcheck=True
	if self.run_lightcheck:
            self.lightcheck_timer=QTimer()
            self.lightcheck_timer.timeout.connect(self.on_lightcheck_timer)
            self.lightcheck_timer.start(1000)
        
    def run(self):

        if self.run_heartbeat:
            self.heartbeat.start(1000)

    def on_heartbeat(self):

        jdp= self.makeJDP()

        self.new_jdp.emit(jdp)
#        self.updateAngle.emit(num(syssecs()) * 6.0)

    def on_lightcheck_timer(self):
        lightlevel=readLight()
        adjust_brightness(lightlevel)

    def makeJDP(self):
        date=sysdate()
        tm=systimeonly()
        md=1
        noise = random.randint(-9,9)
        cs=fabs(num(syssecs())/30.0 - noise/10.0)
        cc=num(syssecs()) * 6.0 + 90.0
        act_s= fabs(num(syssecs())/30.0 + noise/10.0)
        act_c= cc + noise/5.0
        dx= num(syssecs()) * 2.0
        dy= num(syssecs()) * 3.0
        jh= num(syssecs()) * 6.0 - noise/3.0
        ttg= num(syssecs())

        jdppkt = "JDP %s %s %f %f %f %f %f %f %f %f %f" % (date, tm, md, cs, cc, act_s, act_c, dx, dy, jh, ttg)
        return jdppkt

    def oldrun(self):
        for i in range(360):
            self.updateAngle.emit(i)
            time.sleep(0.2)

def num(s):
    try:
        return int(s)
    except ValueError as e:
        return float(s)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        execfile("/home/pi/src/BridgeDisplay/BridgeWidget.py")
    except Exception as e:
        print "Error opening or running BridgeWidget.py", e

    try:
        execfile("/home/pi/src/BridgeDisplay/CompassWidget.py")
    except Exception as e:
        print "Error opening or running CompassWidget.py", e

    try:
        execfile("/home/pi/src/BridgeDisplay/udpl.py")
    except Exception as e:
        print "Error opening or running udpl.py", e

    try:
        execfile("/home/pi/src/BridgeDisplay/time_routines.py")
    except Exception as e:
        print "Error opening or running time_routines.py", e

    try:
        execfile("/home/pi/src/BridgeDisplay/parse.py")
    except Exception as e:
        print "Error opening or running BridgeWidget.py", e

    try:
        execfile("/home/pi/src/BridgeDisplay/auto_brightness.py")
    except Exception as e:
	print "Error opening or running auto_brightness.py", e

    window = BridgeDisplay()

    window.show()

    sys.exit(app.exec_())
