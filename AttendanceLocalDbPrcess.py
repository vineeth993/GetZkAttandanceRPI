#!/usr/bin/python

import MySQLdb as mySql
from time import sleep
import datetime 


class dbManagement():
    
    def __init__(self, host, mysqlUser, mysqlPassword, database):
        
        self.host = host
        self.mysqlUser = mysqlUser
        self.mysqlPassword = mysqlPassword
        self.database = database
        self.dbConn = None
        self.dbCursor = None
       
    def dbConnect(self):
        mysqlStat = None
        mysqlError = None

        try:
            self.dbConn = mySql.connect(self.host, self.mysqlUser, self.mysqlPassword, self.database)
            mysqlStat = "SqlConnected"
        except Exception, error:
            mysqlStat = "SqlNotConnected"
            mysqlError = error
        if self.dbConn:
            self.dbCursor = self.dbConn.cursor()

        return mysqlStat, mysqlError

    def tableInsertion(self, tableName, values, tableFields=None):
        if tableFields:
            query = "insert into "+ tableName +str(tableFields)+" values " + str(values)    
        else:
            query = "insert into "+ tableName +" values" + str(values)
        # print query
        self.dbCursor.execute(query)
        self.dbConn.commit()

    def tableSelect(self, tableName, condition=None, wantedData=None):
        if condition and not wantedData:
            query = "select * from "+ tableName + " where "+ condition
        elif condition == "last":
            if wantedData:
                query = "select max("+wantedData+") from "+ tableName 
        else:

            query = "select * from "+ tableName
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchall()
        return data

    def tableUpdation(self, tableName, values, condition=1):
        query = "update "+ tableName + " set "+ str(values) +" where "+str(condition)
        self.dbCursor.execute(query)
        self.dbConn.commit()

    
    def tableDeletion(self, tableName, condition):
        query = "delete from "+ tableName +" where "+ condition
        self.dbCursor.execute(query)
        self.dbConn.commit()

    def tableConnectionClose(self):
        self.dbConn.close()

                
    
'''       
test = dbManagement()
print type(test.tableSelect("Patients", "Token=1")[0][1])
'''



