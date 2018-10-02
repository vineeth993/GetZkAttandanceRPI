#!/usr/bin/python

import xmlrpclib
import time

class ErpServerConn():

	def __init__(self, userName, password, dbName, url):

		self.dbName = dbName
		self.password = password
		self.userName = userName
		self.url = url
		self.serverAcess = None
		self.loginId = None

	def serverConnect(self):
		serverConn = self.serverProxy(self.urlFormat(self.url, "/xmlrpc/common"))
		serverConnStat = None
		serverError = None
		try:
			self.loginId = serverConn.login(dbName, userName, password)
			if self.loginId:
				serverConnStat = "ServerConnectd"
				self.serverAcess = self.serverProxy(self.urlFormat(self.url, "/xmlrpc/object"))
			else:
				serverConnStat = "ServerNotConnectd"
				serverError = "Please Check the server Parameter"
		except Exception, error:
			serverConnStat = "ServerNotConnectd"
			serverError = error
		
		return serverConnStat, serverError

	def serverProxy(self, url):
		
		serverConn = xmlrpclib.ServerProxy(url)
		return serverConn

	def urlFormat(self, url, urlExtension):
		
		formatExtension = '{}'+str(urlExtension)
		formattedUrl = formatExtension.format(url)
		return formattedUrl

	def searchData(self, model, fields):

		# print "model = "+str(model)
		# print "fields = "+str(fields)
		# print "id = "+str(self.loginId)
		searchId = self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "search", fields)
		# print fields
		return searchId 

	def readData(self, model, searchFields=[], readFields=[]):

		searchId = self.searchData(model, searchFields)
		# print searchId
		getData = self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "read", searchId, readFields)
		return searchId, getData

	def deleteData(self, model, fields=None):

		self.serverAcess.execute(self.dbName, self.loginId, self.password, model, 'unlink', fields)


	def updateData(self, model, id, fields):

		self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "write", id, fields)

	def createData(self, model, data):

		val = self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "create", data)
		return val