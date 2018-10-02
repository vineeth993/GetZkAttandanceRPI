#!/usr/bin/python

import sys
import zklib
import time
from zklib import zklib, zkconst
import logging

_logger = logging.getLogger(__name__)

class AttandanceDeviceManagement():

	def __init__(self, zkIp, zkPort):

		self.zkIp = zkIp
		self.zkPort = zkPort
		self.zkConn = None

	def zkDeviceConnect(self):
		
		self.zkConn = zklib.ZKLib(self.zkIp, self.zkPort)
		zkConnStatus = None
		zkConnError = None
		try:
			connStat = self.zkConn.connect()
			if connStat:
				zkConnStatus = "zkConnected"
			else:
				zkConnStatus = "zkNotConnected"
				zkConnError = "Please check device ip and port"
		except Exception, e:
			zkConnStatus = "zkNotConnected"
			zkConnError = e	

		return zkConnStatus, zkConnError
			
	def zkAttendance(self):
		
		self.zkConn.disableDevice()
		_logger.info("In get attendance")
		attendance = self.zkConn.getAttendance()

		self.zkConn.enableDevice()
		self.zkConn.disconnect()
		return attendance

	def zkAttendanceClear(self):
		
		self.zkDeviceConnect()
		self.zkConn.disableDevice()

		clearStatus = self.zkConn.clearAttendance()

		self.zkConn.enableDevice()
		self.zkConn.disconnect()
		return clearStatus

	def zkGetTime(self):

		self.zkDeviceConnect()
		self.zkConn.disableDevice()

		time = self.zkConn.getTime()

		self.zkConn.enableDevice()
		self.zkConn.disconnect()
		return time
