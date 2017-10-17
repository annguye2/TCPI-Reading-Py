# Name: ConvertTimeZone_Ex02.py
# Description: Convert a time field to another time zone
# Requirements: None

# Import system modules
import arcpy

def convertingTimeZone(): #  this work with date foramt properly
    inTable = "C:/AIS_Data/ais.gdb/test"


    inputTimeField = "t_time"
    inputTimeZone = "Greenwich_Standard_Time"

    outputTimeField = "Output_Time1"
    onputTimeZone = "Eastern_Standard_Time"
    inputUseDaylightSaving = "INPUT_ADJUSTED_FOR_DST"
    outputUseDaylightSaving = "OUTPUT_ADJUSTED_FOR_DST"
    print "Converting Time Zone"

        # Execute CalculateEndDate
    try:
        arcpy.ConvertTimeZone_management(inTable, inputTimeField, inputTimeZone, outputTimeField, onputTimeZone, inputUseDaylightSaving, outputUseDaylightSaving)
    except:
        print " invalid value "



#works: remove row that has no valid Lat nor long
def removeInvalidRow (): # remove row that has invalide Lat and Lon
    fc = "C:/AIS_Data/ais.gdb/ais"
    field = "Longitude"
    cursor = arcpy.SearchCursor(fc)
    with arcpy.da.UpdateCursor(fc, ["Longitude", "Latitude"]) as cursor:
        for row in cursor:
            if row[0] == None:
                print "this is null"
                #print(row.getValue("Vessel_ID"))
                cursor.deleteRow()


if __name__ == '__main__':
    print "Main"
    removeInvalidRow() # works
   # convertingTimeZone ()
    print "End Main"