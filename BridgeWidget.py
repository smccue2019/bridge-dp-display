#!/usr/bin/env python
#import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import sqrt, pow
from BridgeDisplay import Ui_BridgeDispMW

class BridgeDisplay(QMainWindow):

    def __init__(self, parent=None):
        super(BridgeDisplay, self).__init__(parent)

        udp_port = 52108

        self.ui = Ui_BridgeDispMW()
        self.ui.setupUi(self)
        self.compass = CompassWidget()
        compassframewidth = self.ui.frame.frameGeometry().width()
        compassframeheight = self.ui.frame.frameGeometry().height()
        self.compass.set_framewidth(compassframewidth)
        self.compass.set_frameheight(compassframeheight)

#        self.ui.cmd_course_label.setStyleSheet("QLabel {color:rgb(200,200,200);font:20pt}")
#        self.ui.cmd_spd_label.setStyleSheet("QLabel {color:rgb(200,200,200);font:20pt}")
#        self.ui.act_course_label.setStyleSheet("QLabel {color:rgb(200,200,200); font:20pt}")
#        self.ui.act_spd_label.setStyleSheet("QLabel {color:rgb(200,200,200);font: 20pt}")
#        self.ui.ActualGB.setStyleSheet("QGroupBox { border:4px;color: rgb(0,255,0) }")
#        self.ui.CmmdGB.setStyleSheet("QGroupBox { border:4px;color: rgb(0,0,255) }")
        
        self._worker = Worker()
        self._worker.new_jdp.connect(self.on_new_jdp)

        self._worker.start()

        spinBox = QSpinBox()
        spinBox.setRange(0, 359)
        
        layout = QVBoxLayout()
        layout.addWidget(self.compass)
        self.ui.frame.setLayout(layout)
#        self.setWidgetColors()

        self.ur=dp_udp(udp_port)
        self.ur.new_jdp.connect(self.on_new_jdp)

        self.flash_on_time = 200  # milliseconds
        self.jdpflashtimer=QTimer()
        self.jdpflashtimer.timeout.connect(self.on_jdpflashtimer_timeout)
        ("QGroupBox { border:4px;color: rgb(0,0,255) }")

    def on_new_jdp(self, udpstr):
            date,time,md,cspd,ccrs,aspd,acrs,dx,dy,h,t2g=parseJDP(udpstr)


            self.jdpdate = date
            self.jdptime = time
            self.jdpmode = md
            self.jdp_cmd_spd = num(cspd)
            cspdt = "%5.1f kn" % self.jdp_cmd_spd
            self.jdp_cmd_crs = num(ccrs) % 360.0
            ccrst = "%5.1f" % self.jdp_cmd_crs
            self.jdp_act_spd = num(aspd)
            aspdt = "%4.2f kn" % self.jdp_act_spd
            self.jdp_act_crs = num(acrs) % 360.0
            acrst = "%5.1f" % self.jdp_act_crs 
            self.jdp_delx = num(dx)
            self.jdp_dely = num(dy)
            self.jdp_shipheading = num(h) % 360.0
            self.time2goal = "%s s" % t2g

            dist2goal = sqrt(pow(self.jdp_delx, 2) + pow(self.jdp_dely,2))
            dist2goalt = "%5.1f m" % dist2goal
            self.ui.dist_label.setText(dist2goalt)
            self.ui.time_label.setText(self.time2goal)

            self.ui.cmd_course_label.setText(ccrst)
            self.ui.cmd_spd_label.setText(cspdt)
            self.ui.act_course_label.setText(acrst)
            self.ui.act_spd_label.setText(aspdt)

            self.compass.setCmdCourse(self.jdp_cmd_crs)
            self.compass.setCmdSpd(self.jdp_cmd_spd)
            self.compass.setActualCourse(self.jdp_act_crs)
	    self.compass.setActualSpd(self.jdp_act_spd)
            self.compass.setShipHeading(self.jdp_shipheading)

    def on_jdpflashtimer_timeout(self):
        self.ui.commLED.setStyleSheet("QLabel {background: rgb(255, 255, 255)}")


