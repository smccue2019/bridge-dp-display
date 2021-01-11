#!/usr/bin/env python
#import sys
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import cos, sin, sqrt

class CompassWidget(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.ship_heading = 0.0
        self.prior_ship_heading = 0.0
        self.cmd_crs = 0.0
        self.prior_cmd_crs = 0.0
        self.cmd_spd = 0.0
        self.prior_cmd_spd = 0.0
        self.actual_crs = 0.0
        self.actual_spd = 0.0
        self.prior_actual_crs = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
                           225: "SW", 270: "W", 315: "NW"}      
        self.ship_shape=[QPoint(-10, 0), QPoint(-9, 15), QPoint(-9, 30),
                      QPoint(-8, 45), QPoint(8, 45), QPoint(9, 30),
                      QPoint(9, 15), QPoint(10, 0), QPoint(10, -10), 
                      QPoint(8, -20), QPoint(7, -30), QPoint(5, -35),
                      QPoint(3, -40), QPoint(0, -45), QPoint(-3, -40),
                      QPoint(-5, -35), QPoint(-7, -30), QPoint(-8, -20), 
                      QPoint(-10, -10), QPoint(-10, 0)]
        self.arrow_shape=[QPoint(0,0), QPoint(2,0), QPoint(2,20), QPoint(4,18),
                          QPoint(2,21), QPoint(0,24), QPoint(-2,21),
                          QPoint(-4,18),QPoint(-2,20), QPoint(-2, 0),
                          QPoint(0,0)]

        self.arrow_shape2=[QPoint(0,24), QPoint(-2,21), QPoint(-4,18),
                          QPoint(-2,20),QPoint(-2,0),
                          QPoint(2,0), QPoint(2, 20),QPoint(4,18),
                          QPoint(2,21),QPoint(0,24)]

        self.actual_arrow_color = QColor(Qt.darkGreen)
        aac_alpha = self.actual_arrow_color.alpha()
        self.actual_arrow_color.setAlpha(128)

        self.cmd_arrow_color = QColor(Qt.darkBlue)
        cac_alpha = self.cmd_arrow_color.alpha()
        self.cmd_arrow_color.setAlpha(128)

        self.scale_constant = 120
        self.arrow_scale = 18
        self.tr_fudge_factor = 12

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
        self.drawMarkings(painter)
        self.drawShip(painter)
        self.drawCmdArrow(painter)
        self.drawActArrow(painter)

        painter.end()

    def drawMarkings(self, painter):

        painter.save()
        painter.translate(self.framewidth/2 - self.tr_fudge_factor, self.frameheight/2 - self.tr_fudge_factor)
        scale = min((self.framewidth - self._margins)/self.scale_constant,
                    (self.frameheight - self._margins)/self.scale_constant)
        painter.scale(scale, scale)

        font = QFont(self.font())
        font.setPixelSize(10)
        metrics = QFontMetricsF(font)

        painter.setFont(font)
#        painter.setPen(self.palette().color(QPalette.Shadow))
        painter.setPen(QColor(Qt.darkBlue))

        i = 0
        while i < 360:
            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-metrics.width(self._pointText[i])/2.0, -52,self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)
            painter.rotate(1)
            i += 1

        painter.restore()

    def drawShip(self, painter):

        painter.save()
        painter.translate(self.framewidth/2-self.tr_fudge_factor, self.frameheight/2 - self.tr_fudge_factor)
        painter.rotate(self.ship_heading)

        scale = min((self.framewidth - self._margins)/self.scale_constant,
                    (self.frameheight - self._margins)/self.scale_constant)
        painter.scale(scale, scale)
        painter.setPen(QPen(QColor(Qt.gray)))
        #painter.setBrush(self.palette().brush(QPalette.Shadow))
	painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawPolygon( QPolygon(self.ship_shape) )

        painter.restore()

    def drawCmdArrow(self, painter):
        # Draw commanded course arrow
        painter.save()
        painter.translate(self.framewidth/2, self.frameheight/2)
        arrow_angle = 180 + self.cmd_crs
        if arrow_angle > 360.0:
            arrow_angle = arrow_angle - 360.0
        painter.rotate(arrow_angle)

        scale = min((self.framewidth - self._margins)/self.scale_constant,
                    (self.frameheight - self._margins)/self.scale_constant)
        painter.scale(scale, scale)
#        painter.setPen(QPen(QColor(Qt.black), 2))
        arrow_scale = self.arrow_scale * self.cmd_spd
        painter.scale(arrow_scale, arrow_scale)
        painter.setBrush(self.cmd_arrow_color)
        painter.drawPolygon( QPolygon(self.arrow_shape) )

        painter.restore()

    def drawActArrow(self, painter):
        # Draw actual course arrow
        painter.save()
        painter.translate(self.framewidth/2, self.frameheight/2)
        arrow_angle = 180 + self.actual_crs
        if arrow_angle > 360.0:
            arrow_angle = arrow_angle - 360.0
        painter.rotate(arrow_angle)

        scale = min((self.framewidth - self._margins)/self.scale_constant,
                    (self.frameheight - self._margins)/self.scale_constant)
        painter.scale(scale, scale)
 #       painter.setPen(QPen(QColor(Qt.black)))
        painter.setBrush(self.actual_arrow_color)
        arrow_scale = self.arrow_scale * self.actual_spd
        painter.scale(arrow_scale, arrow_scale)
        painter.drawPolygon(QPolygon(self.arrow_shape))

        painter.restore()

#    def sizeHint(self):
#        return QSize(600, 600)

# Ships Heading
    def getHeading(self):
        return self.ship_heading

    def setShipHeading(self, heading):
        if heading != self.ship_heading:
            self.prior_ship_heading = self.ship_heading
            self.ship_heading = heading
            #print self.ship_heading
            self.update()

#CmdCourse
    def getCmdCourse(self):
        return self.cmd_crs

    def setCmdCourse(self, cmd_crs):
        if cmd_crs != self.cmd_crs:
            self.prior_cmd_crs = self.cmd_crs
            self.cmd_crs=cmd_crs
            self.cc_diff = self.cmd_crs - self.prior_cmd_crs
            self.update()

# Commanded Speed
    def getCmdSpd(self):
        return self.cmd_spd

    def setCmdSpd(self, cmd_spd):
        if cmd_spd != self.cmd_spd:
            self.prior_cmd_spd = self.cmd_spd
            self.cmd_spd = cmd_spd
            self.update()

#RealCourse
    def getActualCourse(self):
        return self.actual_crs

    def setActualCourse(self, actual_crs):
        if actual_crs != self.actual_crs:
            self.prior_actual_crs = self.actual_crs
            self.actual_crs = actual_crs
            self.ac_diff = self.actual_crs - self.prior_actual_crs
            self.update()

# Actual Speed
    def getActualSpd(self):
        return self.actual_spd

    def setActualSpd(self, actual_spd):
        if actual_spd != self.actual_spd:
            self.prior_act_spd = self.actual_spd
            self.actual_spd = actual_spd
            self.update()
            
    def set_framewidth(self, passed_width):
        self.framewidth = passed_width

    def set_frameheight(self, passed_height):
        self.frameheight = passed_height

#        self.unused_arrow_shape=[QPoint(0,0), QPoint(15,40),
#                                   QPoint(5,30), QPoint(5,120),
#                                   QPoint(15,160), QPoint(0,130),
#                                   QPoint(-15,160), QPoint(-5,120),
#                                   QPoint(-5,30), QPoint(-15,40)]
