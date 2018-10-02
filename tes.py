from struct import pack, unpack
import sys
import zklib
import time
from zklib import zklib, zkconst
from zklib import *
from datetime import datetime, date
from zklib.zkconst import *

zk = zklib.ZKLib("192.168.1.201", 4370)

ret = zk.connect()
print ret
zk.disableDevice()
print "connection:", ret

def getSizeAttendance(self):
    """Checks a returned packet to see if it returned CMD_PREPARE_DATA,
    indicating that data packets are to be sent

    Returns the amount of bytes that are going to be sent"""
    command = unpack('HHHH', self.data_recv[:8])[0] 
    if command == CMD_PREPARE_DATA:
        size = unpack('I', self.data_recv[8:12])[0]
        return size
    else:
        return False


def reverseHex(hexstr):
    tmp = ''
    for i in reversed( xrange( len(hexstr)/2 ) ):
        tmp += hexstr[i*2:(i*2)+2]
    
    return tmp
    
def zkgetattendance(self):
    """Start a connection with the time clock"""
    command = CMD_ATTLOG_RRQ
    command_string = ''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    #print buf.encode("hex")
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        if getSizeAttendance(self):
            bytes = getSizeAttendance(self)
            # print "bytes = "+str(bytes)
            while bytes > 0:
                data_recv, addr = self.zkclient.recvfrom(1032)
                # print data_recv
                self.attendancedata.append(data_recv)
                # print "self.attendancedata = "+str(self.attendancedata)
                bytes -= 1024
                
            self.session_id = unpack('HHHH', self.data_recv[:8])[2]
            data_recv = self.zkclient.recvfrom(8)
            # print "data_recv = "+str(data_recv)
        attendance = []  
        if len(self.attendancedata) > 0:
            # The first 4 bytes don't seem to be related to the user
            for x in xrange(len(self.attendancedata)):
                if x > 0:
                    self.attendancedata[x] = self.attendancedata[x][8:]
            
            attendancedata = ''.join( self.attendancedata )
            
            attendancedata = attendancedata[14:]
            
            while len(attendancedata) > 0:
                
                uid, state, timestamp, space = unpack( '24s1s4s11s', attendancedata.ljust(40)[:40] )
                pls = unpack('c', attendancedata[29:30])
                uid = uid.split('\x00', 1)[0]
                tmp = ''
                for i in reversed(xrange(len(timestamp.encode('hex')) / 2)):
                    tmp += timestamp.encode('hex')[i * 2:(i * 2) + 2]
                attendance.append((uid, int(state.encode('hex'), 16),decode_time( int( reverseHex( timestamp.encode('hex') ), 16 ) ), unpack('HHHH', space[:8])[0]))

                attendancedata = attendancedata[40:]
            
        return attendance
    except:
        return False


if ret == True:
    # print "Disable Device", zk.disableDevice()

    # print "ZK Version:", zk.version()
    # print "OS Version:", zk.osversion()
    # """
    # print "Extend Format:", zk.extendFormat()
    # print "Extend OP Log:", zk.extendOPLog()
    # """
    
    # print "Platform:", zk.platform()
    # print "Platform Version:", zk.fmVersion()
    # print "Work Code:", zk.workCode()
    # print "Work Code:", zk.workCode()
    # print "SSR:", zk.ssr()
    # print "Pin Width:", zk.pinWidth()
    # print "Face Function On:", zk.faceFunctionOn()
    # print "Serial Number:", zk.serialNumber()
    # print "Device Name:", zk.deviceName()
    
    # data_user = zk.getUser()
    # print "Get User:"
    # if data_user:
    #     for uid in data_user:
            
    #         if data_user[uid][2] == 14:
    #             level = 'Admin'
    #         else:
    #             level = 'User'
    #         print "[UID %d]: ID: %s, Name: %s, Level: %s, Password: %s" % ( uid, data_user[uid][0], data_user[uid][1], level, data_user[uid][3]  )

        #zk.setUser(uid=61, userid='41', name='Dony Wahyu Isp', password='123456', role=zkconst.LEVEL_ADMIN)
    
    attendance = zkgetattendance(zk)
    # print "Get Attendance:", attendance
    
    if ( attendance ):
        for lattendance in attendance:
            # print lattendance
            
       # # if lattendance[1] == 15:
    #         #    state = 'Check In'
    #         #elif lattendance[1] == 0:
    #          #   state = 'Check Out'
    #         #else:
    #          #   state = 'Undefined'
                
            print "date %s, Jam %s: %s, Status: %s" % ( lattendance[2].date(), lattendance[2].time(), lattendance[0], lattendance[1] )
               
    # # print "Clear Attendance:", zk.clearAttendance()
    
    # zk.setUser(67, '67', 'Shubhamoy Chakrabarty', '', 0)
    print "Get Time:", zk.getTime()
    print "Enable Device", zk.enableDevice()
    print "Disconnect:", zk.disconnect()


