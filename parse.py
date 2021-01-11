#!/usr/bin/env python

from PyQt4.QtCore import QString, QRegExp
import re

#def parseJDS(jdspkt):
#    jdspkt.chop(1)
#    jdsfields  = jdspkt.split(" ")
#    pktid = jdsfields[0].toAscii()
#    jdsdate = jdsfields[1].toAscii()
#    jdstime = jdsfields[2].toAscii()
#    veh = jdsfields[3].toAscii()
#    lat_deg = num(jdsfields[4])
#    lon_deg = num(jdsfields[5])
#    X_local = num(jdsfields[6])
#    Y_local = num(jdsfields[7])
#    oct_roll = num(jdsfields[8])
#    oct_pitch = num(jdsfields[9])
#    oct_heading = num(jdsfields[10])
#    jdsdepth = num(jdsfields[11])
#    u1 = jdsfields[12]
#    u2 = jdsfields[13]
#    jdsalt = jdsfields[14]
    
    # Altitude can be wrong for several reasons. one
    # of them is that the vehicle is too high in th
    # water column. If it's not reporting a number,
    # then set it to something that's definitely
    # not-a-number.
#    try:
#        jdsalt = num(jdsfields[12])
#    except ValueError:
#        jdsalt = "0"
#    return(jdsdate, jdstime, jdsdepth, jdsalt, oct_heading)

# QString jdpRecord = "JDP " + timeString + " " +
# QString::number(dpType) + " " +
# QString::number(reasonableReferenceSpeed,'f',2) + " " +
# QString::number(bearing,'f',1) +
# QString::number(shipSpeed,'f',2) + " " +
# QString::number(shipCog,'f',2) + " " +
# QString::number(dx,'f',1) + " " +
# QString::number(dy,'f',1) + " " +
# QString::number(shipHeading,'f',1) + " " +
# QString::number(currentTimeToGoal,'f',0) + "\n";

def parseJDP(jdppkt):
    jdppkt.chop(1)
    jdpfields  = jdppkt.split(" ")
    pktid = jdpfields[0].toAscii()
    jdpdate=jdpfields[1].toAscii()
    jdptime = jdpfields[2].toAscii()
    jdpmode = jdpfields[3]
    jdp_cmd_spd = jdpfields[4]
    jdp_cmd_crs = jdpfields[5]
    jdp_act_spd = jdpfields[6]
    jdp_act_crs = jdpfields[7]
    jdp_delx = jdpfields[8]
    jdp_dely = jdpfields[9]
    jdp_heading = jdpfields[10]
    jdp_time2goal = jdpfields[11]

    return jdpdate, jdptime, jdpmode, jdp_cmd_spd, jdp_cmd_crs, jdp_act_spd, jdp_act_crs, jdp_delx, jdp_dely, jdp_heading, jdp_time2goal

def num(s):
    try:
        return int(s)
    except ValueError as e:
        return float(s)
