#!/usr/bin/python

import logging
import logging.config
from datetime import datetime, date
import time

logging.config.fileConfig('/home/pi/ZkAttendanceSystem/logger.ini')
_logger = logging.getLogger(__name__)

_logger.info('Starting App') 

import AttendanceLocalDbPrcess
import AttandanceDeviceManagement
import ErpMainConn

class MainThread():

	def __init__(self, localDbHost, localUser, localPassword, mainDatabase, mainTable):

		self.dbConn = AttendanceLocalDbPrcess.dbManagement(localDbHost, localUser, localPassword, mainDatabase)
		self.mainTable = mainTable
		self.connectLocalDb()

	def __del__(self):
		self.dbConn.tableConnectionClose()
		self.erp.close()
	
	def connectLocalDb(self):
		localConnStat = None
		while localConnStat != "SqlConnected":
			localConnStat, localError = self.dbConn.dbConnect()
			self.loggerPrinting(localConnStat, localError)
			if localError:
				time.sleep(1)
	
	def connectERP(self):
		devParam = self.distributeParam("erp")
		self.erp = ErpMainConn.ErpServerConn(devParam['erpServerUser'],
											devParam['erpPasscode'],
											devParam['erpDb'],
											devParam['erpServer'])

		serverConnStat = None
		while serverConnStat != "ServerConnectd":
			serverConnStat, serverError = self.erp.serverConnect()
			self.loggerPrinting(serverConnect, serverError)
			time.sleep(1)			
	
	def loggerPrinting(self, stat, error=None):

		_logger.info("The status = "+str(stat))
		if error:
			_logger.error("The error = "+str(error))

	def getSystemParameters(self, table):
		
		systemParameter = self.dbConn.tableSelect(table)
		return systemParameter

	def massDeletion(self, conditon):


	def distributeParam(self, system=None):

		systemParam = self.getSystemParameters(self.mainTable)
		returnParam = {}
		if systemParam:
			if system == "erp":
				returnParam = {
					"erpServer":systemParam[0][0],
					"erpServerUser":systemParam[0][1],
					"erpPasscode":systemParam[0][2],
					"erpDb":systemParam[0][3]
				}
			elif system == "device":
				returnParam = {
					"devIp":systemParam[0][4],
					"devPort":systemParam[0][5]
				}

		return returnParam

	def zkConnect(self):
		devParam = None
		while not devParam:
			devParam = self.distributeParam("device")
			if not devParam:
				_logger.error("Please check the table name or table value = "+str(self.mainTable))
				time.sleep(1)				

		prevAttandanceParam = self.getSystemParameters("AttandanceParam")

		self.device = AttandanceDeviceManagement.AttandanceDeviceManagement(devParam["devIp"], devParam["devPort"])
		devConnStat = None

		while devConnStat != "zkConnected":
			devConnStat, devConnError = self.device.zkDeviceConnect()
			self.loggerPrinting(devConnStat, devConnError)
			time.sleep(1)

	def pushDataToLocal(self, attandanceTable):
		
		attendances = self.device.zkAttendance()
		isAttendance = False
		count = 0

		if attendances:
			for attendance in attendances:
				try:
					attendanceDate = str(attendance[2])
					if not prevAttandanceParam or prevAttandanceParam[0][1] < attendance[2]:
						isAttendance = True
						count += 1
						self.dbConn.tableInsertion(attandanceTable, (attendance[0], attendanceDate), '(EmpId,DateTime)')
					else:
						isAttendance = False
						continue
				except Exception, error:
					_logger.error("Table insertion error for EmpId %s on date %s error = %s"%(attendance[0], attendanceDate, error))
					return "DbError"

			if not isAttendance:
				_logger.info("No new data are found")
				return "Noattendance"

			else:
				_logger.info(str(count)+" Attendance is updated")
				if prevAttandanceParam:
					whereCondition = "id = %i"%prevAttandanceParam[0][0]
					value = 'lastDateTime = "'+str(attendanceDate)+'"'

					try:
						self.dbConn.tableUpdation("AttandanceParam", value, whereCondition)
					except Exception, error:
						_logger.error("Table updation error = "+str(error))
						self.massDeletion(prevAttandanceParam[0][1])
						return "DbError"
				else:
					self.dbConn.tableInsertion('AttandanceParam', '("'+str(attendanceDate)+'")', '(lastDateTime)')

		else:
			_logger.info("There is no attendance data in the device ")
			return "Noattendance"

		_logger.info("Local DbProcess Completed")
		return "Completed"

	def pushDataToErp(self, attandanceTable, model, createModel):

		getLocalAttendance = self.dbConn.tableSelect(attandanceTable)
		if getLocalAttendance:
			for attendance in getLocalAttendance:
				try:
					data = self.erp.searchData(model, searchFields=[("emp_id", "=", attendance[1])])
					if not data:
						_logger.warning("Employee not found in erp with employee id = "+str(attendance[1]))
					else:
						stat = self.erp.creatData(createModel, {'employee_id':data[0], 
															'date_time':str(attendance[2]), 
															'emp_id':attendance[1]})
						if stat:
							try:
								condition = "id = %i"%attendance[0]
								self.dbConn.tableDeletion(attandanceTable, condition)
							except Exception, e:
								self.loggerPrinting("db Deletion error", e)
								condition = "id = %i"%stat[0]
								self.erp.deleteData(createModel, condition)
								return "DbError"					
				except Exception, e:
					self.loggerPrinting("Please check the erp table name", e)
					return "ErpError"
		else:
			return "NoData"

		return "UpdationCompleted"

	def main(self):
		
		prevAttandanceParam = self.getSystemParameters("AttandanceParam")
		initial = False
		final = False
		isAttendance = False

		while True:
			presentDateTime = datetime.now()
			time = presentDateTime.time	
			if prevAttandanceParam[0][2] >= time and prevAttandanceParam[0][3] < time and not initial:
				initial = True
				isAttendance = True
				final = False

			elif not final and prevAttandanceParam[0][3] >= time:
				initial = False
				final = True
				isAttendance = True 

			else:
				final = False

			if not isAttendance:
				self.connectERP()
				status = self.pushDataToErp('Attandance', 'hr.employee', 'attendance.attendance')
			elif isAttendance:
				self.zkConnect()
				status = self.pushDataToLocal('Attandance')




if __name__ == "__main__":

	main = MainThread('localhost', 'vineeth', 'vineeth', 'zkAttendance','SystemParam')
	main.get()