# Name: ConvertTimeZone_Ex02.py
# Description: Convert a time field to another time zone
# Requirements: None

# Import system modules
import arcpy
import os
from ConvertTimeZoneModule import *

def killArcGISProcesses():
    print "Kill Arc Catalog or Arc Map Process"

    print "Kill Arc Catalog Process"
    os.system("TASKKILL /F /IM ArcCatalog.exe")
##    if (pidName == "ArcMap.exe"):
    print "Kill Arc Map Process"
    os.system("TASKKILL /F /IM ArcMap.exe")



#works: remove row that has no valid Lat nor long
##def removeInvalidRow (): # remove row that has invalide Lat and Lon
##    fc = "C:/AIS_Data/ais.gdb/ais"
##    field = "Longitude"
##    cursor = arcpy.SearchCursor(fc)
##    with arcpy.da.UpdateCursor(fc, ["Longitude", "Latitude"]) as cursor:
##        for row in cursor:
##            if row[0] == None:
##                print "this is null"
##                #print(row.getValue("Vessel_ID"))
##                cursor.deleteRow()
##


# add date field into table

# set value to  Date Field into Table
##def setValueToField():
##
##    print "format date time zone values"
##    fc = "C:/AIS_Data/ais.gdb/ais"
##    dateField = "Date_tag_last_rpt__GMT_"
##    field2 = "Time_tag_last_rpt__GMT_"
##
##    cursor = arcpy.UpdateCursor(fc)
##    for row in cursor:
##        # field2 will be equal to field1 multiplied by 3.0
##        print row.getValue(dateField)
##        row.setValue(dateField, "new value") #set value to dateField colum
##        cursor.updateRow(row)


###=============For adding new date and Time field and reformat ===============
##def convertingTimeZone(): #  this work with date foramt properly look at the table "test " in Y drive
##    inTable = "C:/AIS_Data/ais.gdb/ais"
##    inputTimeField = "tmp_Date_Time"
##    inputTimeZone = "Greenwich_Standard_Time"
##    outputTimeField = "Date_Time"
##    onputTimeZone = "Eastern_Standard_Time"
##    inputUseDaylightSaving = "INPUT_ADJUSTED_FOR_DST"
##    outputUseDaylightSaving = "OUTPUT_ADJUSTED_FOR_DST"
##    print "Converting Time Zone"
##    try:
##        arcpy.ConvertTimeZone_management(inTable, inputTimeField, inputTimeZone, outputTimeField, onputTimeZone, inputUseDaylightSaving, outputUseDaylightSaving)
##    except:
##        print " invalid value "
##    print"Remove TempDateTime"
##    arcpy.DeleteField_management("C:/AIS_Data/ais.gdb/ais",
##                             ["tmp_Date_time"])
####=======================================
##def addDateFieldIntoTable():
##    print "add Date_Time field"
##    arcpy.env.workspace = "C:/AIS_Data/ais.gdb"
##    # Set local variables
##    inFeatures = "ais"  #table name
##    dateTime = "tmp_Date_Time"
##    fieldPrecision = 30
##    fieldAlias = "tmp_Date_Time"
##    arcpy.AddField_management(inFeatures, dateTime, "DATE", fieldPrecision,
##                          field_alias=fieldAlias, field_is_nullable="NULLABLE")
##
##
####=======================================
##def getMonth(monthStr):
##    # creating months dictionary
##    monthDictionary = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
##                        "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
##                        "Nov": "11", "Dec": "12"}
##    return monthDictionary.get(monthStr) #return selected month
####=======================================
##def formatDate(inDateStr):
##    #split whole string and get Date part
##    dateStr =  inDateStr.split(" ")[1]
##    #get day part
##    dayStr = dateStr[:2]
##    monthStr = (dateStr[2:])[:3]
##    yearStr =  dateStr[5:]
##    newDateFormat = getMonth(monthStr) + "/" + dayStr + "/" + yearStr + " "
##    return newDateFormat
####=======================================
##def buildDateTimeInfo():
##    print"build data-time information"
##    dateStr =  ""
##    fc = "C:/AIS_Data/ais.gdb/ais"
##    dateField = "Date_tag_last_rpt__GMT_"
##    timeField = "Time_tag_last_rpt__GMT_"
##    dateTimeField = "tmp_Date_Time"
##    cursor = arcpy.UpdateCursor(fc)
##    for row in cursor:
####        print row.getValue(timeField)
##        tmp_time = datetime.strptime(row.getValue(timeField), "%H:%M:%S")
##        _time = tmp_time.strftime("%I:%M:%S %p")
####        print _time
##        dateStr = formatDate(row.getValue(dateField)) + " " + _time
##        row.setValue(dateTimeField, dateStr) #set value to dateField colum
##        cursor.updateRow(row)
##
####=======================================
###  This  function conver GMT time zone to Eastern Standard Time Zone
###  Call this function on the main to get table has new Time Zone
##def setNewTimeZone():
##    print "Set New Time Zone "
##    killArcGISProcesses()
##    addDateFieldIntoTable()  #works
##    buildDateTimeInfo()      #works
##    convertingTimeZone()
##=============== Main ====================
if __name__ == '__main__':
    print "Main"
    killArcGISProcesses()
    converTimeZone  = ConvertingTimeZone("C:/AIS_Data/ais.gdb/ais")
    converTimeZone.setNewTimeZone()

##    setNewTimeZone()
    print "End Main"