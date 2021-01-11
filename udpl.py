#!/usr/bin/env python
import sys, re, time, threading
from math import isnan
from PyQt4.QtCore import Qt, QTime, QTimer, QString, pyqtSignal, QFile
from PyQt4 import QtNetwork

class dp_udp(QDialog):

#    new_jds = pyqtSignal(QString, name = 'new_jds')
    new_jdp = pyqtSignal(QString, name = 'new_jdp')
#    new_pns = pyqtSignal(QString, name = 'new_vfr')

    def __init__(self, listen_port, parent=None):
        super(dp_udp, self).__init__(parent)

        self.ListenPort = listen_port
	print "Listening on UDP port %d" % listen_port

        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(QtNetwork.QHostAddress.Any, self.ListenPort)
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)

    def processPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            udpstr, host, port = \
               self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())

            u = datagram2packetID(udpstr)
            id_string = u.identify_datagram(udpstr)

            if id_string == 'JDP':
                self.new_jdp.emit(udpstr)
	        print(udpstr)
            else:
                # Other packets don't matter
                pass

class datagram2packetID():

    def __init__(self, datagram):

#        self.datagram = datagram
#        self.j = re.compile('^JDS')
        self.d = re.compile('^JDP')
#        self.p = re.compile('^VFR.*SOLN_GPS0.*')

    def identify_datagram(self, datagram):

#        if self.j.match(datagram):
#            return('ODR')
        if self.d.match(datagram):
            return('JDP')
#        elif self.p.match(datagram):
#            return('VFR')
        else:
            return None
