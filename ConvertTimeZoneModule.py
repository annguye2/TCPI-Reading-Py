#-------------------------------------------------------------------------------
# Name:        Converting Time Zone
# Purpose:     Converting Time Zone for AIS Live Data
#
# Author:      An Nguyen (524855)
#
# Created:     17/10/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
from datetime import datetime


##-------------------------------------------------------------------------------

class Test:
    def __init__(self, _msg):
      self.msg = _msg
      print "construction"
    def writeHello(self):
        print self.msg

##-------------------------------------------------------------------------------
class ConvertingTimeZone:
    def __init__(self, _inTable):
      print "construction"
      self.inTable = _inTable
      self.temp = "temp"                    #tmp field hold values from Time_tag_last_rpt__GMT_
      self.tmp_date_time  = "Tmp_Date_Time" # Temp Field holds GMT date time format

    #=============For adding new date and Time field and reformat ===============
    def convertingTimeZone(self, inputTimeField, outputTimeField): #  this work with date foramt properly look at the table "test " in Y drive
##        inputTimeField = "tmp_Date_Time"
        inputTimeZone = "Greenwich_Standard_Time"
##        outputTimeField = "Date_Time"
        onputTimeZone = "Eastern_Standard_Time"
        inputUseDaylightSaving = "INPUT_ADJUSTED_FOR_DST"
        outputUseDaylightSaving = "OUTPUT_ADJUSTED_FOR_DST"
        print "Converting Time Zone"
        try:
            arcpy.ConvertTimeZone_management(self.inTable, inputTimeField, inputTimeZone, outputTimeField, onputTimeZone, inputUseDaylightSaving, outputUseDaylightSaving)
        except:
            print " invalid value "

    ##===================================================
    def deleteFields (self, fields):
        print "Delete field(s)"
        arcpy.DeleteField_management(self.inTable,fields)
    ##=======================================
    def addDateFieldIntoTable(self, fieldType, fieldName):
        print "Add new field"
        arcpy.env.workspace = "C:/AIS_Data/ais.gdb"
        # Set local variables
        inFeatures = "ais"  #table name
        fieldPrecision = 30
        fieldAlias = fieldName
        arcpy.AddField_management(inFeatures, fieldName, fieldType, fieldPrecision,
                              field_alias=fieldAlias, field_is_nullable="NULLABLE")

    ##=======================================
    def getMonth(self, monthStr):
        # creating months dictionary
        monthDictionary = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
                            "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
                            "Nov": "11", "Dec": "12"}
        return monthDictionary.get(monthStr) #return selected month
    ##=======================================
    def formatDate(self, inDate):
        #split whole string and get Date part
        dateStr =  inDate.split(" ")[1]
        #get day part
        dayStr = dateStr[:2]
        monthStr = (dateStr[2:])[:3]
        yearStr =  dateStr[5:]
        newDateFormat = self.getMonth(monthStr) + "/" + dayStr + "/" + yearStr + " "
        return newDateFormat
    ##=======================================
    def buildDateTimeInfo(self, timeField, dateTimeField):
        print"Build data-time information"
        dateStr =  ""
        dateField = "Date_tag_last_rpt__GMT_"
##        dateTimeField = "tmp_Date_Time"
        cursor = arcpy.UpdateCursor(self.inTable)
        for row in cursor:
            tmp_time = datetime.strptime(row.getValue(timeField), "%H:%M:%S")
            _time = tmp_time.strftime("%I:%M:%S %p")
            dateStr = self.formatDate(row.getValue(dateField)) + " " + _time
            row.setValue(dateTimeField, dateStr) #set value to dateField colum
            cursor.updateRow(row)

    ##===================================================
    def setValueToField(self, fieldToFill, inTable ):
        print "Set values into new field:   ", fieldToFill
        timeField = "Time_tag_last_rpt__GMT_"
        cursor = arcpy.UpdateCursor(inTable)
        for row in cursor:
            # field2 will be equal to field1 multiplied by 3.0
##            print row.getValue(timeField)
            row.setValue(fieldToFill, row.getValue(timeField)) #set value to dateField colum
            cursor.updateRow(row)

    ##==================================
    #  Call this function on the main to get table has new Time Zone
    def setNewTimeZone(self):
        print "Set new time zone"
        self.addDateFieldIntoTable("DATE", self.tmp_date_time)# Creating temporary field (type Date)for Date Time
##        Creating temp field (type text) to hold Time_tag_last_rpt__GMT_ values since
##        values in that field sometimes type Date, sometime type TEXT, so creating this field to make sure the app
##        always processes the field type as TEXT
        self.addDateFieldIntoTable("TEXT", self.temp)
        #set time field to temp
        self.setValueToField("temp", self.inTable)
        self.buildDateTimeInfo("temp","tmp_Date_Time")      #works
        self.convertingTimeZone("tmp_Date_Time", "Eastern_Standard_Time")
        self.deleteFields(["temp", "tmp_Date_Time"]) # clean up created temp fields

##==================================##==================================