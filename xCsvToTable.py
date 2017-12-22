#-------------------------------------------------------------------------------
# Name:        Import CSV table to GDB
# Purpose:    Taking AIS csv file, and import to AIS Gdb
#
# Author:      524855
#
# Created:     10/08/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
import os
import csv
import arcpy
import shutil
##from ConvertTimeZoneModule import *
from CreateGeoSpatialTable import *

##path = r"C:/AIS_Data/"
##AisGDB  = "ais.gdb"
##aisTable = "ais"
##arcpy.env.workspace = path
##csvFile = path + r"ais_live.csv"
##AisGdbPath = path + AisGDB

##================================================================
##def cleanCSV():
##    # Refresh the Catalog window for the new directory
##    csv1 =  'C:/AIS_Data/ais_live.csv'
##    csv2 =  'C:/AIS_Data/ais_live_edit.csv'
##    with open(csv1,'r') as f, open(csv2,'w') as f1:
##        next(f) # skip header line
##        next(f)
##        for line in f:
##            f1.write(line)
##
##    arcpy.Delete_management(csv1)
##    shutil.move(csv2,  csv1)
##    arcpy.RefreshCatalog("C:\AIS_Data")
##    #os.system("TASKKILL /F /IM ArcCatalog.exe")
##    #os.system("TASKKILL /F /IM ArcMap.exe")

##================================================================

##def createAISFeatureClass():
##    print "Creating Feature Class"
##    arcpy.env.workspace = "C:/AIS_Data/ais.gdb"
##    ##
##    # Set the local variables
##    in_Table = "ais"
##    x_coords = "Longitude"
##    y_coords = "Latitude"
##    z_coords = ""
##    out_Layer = "ais_layer"
##    saved_Layer = r"C:\AIS_Data\ais.lyr"
##
##    # Set the spatial reference
##    spRef = r"Coordinate Systems\Graphic Coordinate Systems\World\WGS 1984.prj"
##    #spRef = r"Coordinate Systems\Projected Coordinate Systems\Utm\Nad 1983\NAD 1983 UTM Zone 11N.prj"
##    #spRef = r"GCS_WGS_1984"
##    print "can't add spRef here"
##    # Make the XY event layer...
##    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
##    # Print the total rowsz
##    print arcpy.GetCount_management(out_Layer)
##    # Save to a layer file
##    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
##    arcpy.CopyFeatures_management("ais_layer", "C:/AIS_Data/ais.gdb/AIS_FC")

##
####================================================================
##def importCSVTTable ():  # Import CSV information to geodata table
##     #arcpy.Delete_management(AisGdbPath)
##
##     arcpy.TableToTable_conversion(csvFile, AisGdbPath, aisTable)
##
##def deleteFiles():
##
##    #arcpy.Delete_management("C:/AIS_Data/schema.ini")
##    arcpy.Delete_management("C:/AIS_Data/ais.lyr")
##    arcpy.Delete_management("C:/AIS_Data/ais.gdb/ais")
##    arcpy.Delete_management("C:/AIS_Data/ais.gdb/AIS_FC")
##
####================================================================
##
##def removeInvalidRow (): # remove row that has invalide Lat and Lon
##    fc = "C:/AIS_Data/ais.gdb/ais"
##    field = "Longitude"
##    cursor = arcpy.SearchCursor(fc)
##    with arcpy.da.UpdateCursor(fc, ["Longitude", "Latitude"]) as cursor:
##        for row in cursor:
##            if row[0] == None:
##                #print "this is null"
##                #print(row.getValue("Vessel_ID"))
##                cursor.deleteRow()


##================================================================

if __name__ == '__main__':

   creatingSpatialFeature = CreateGeoSpatialTable("Start creating AIS Geospatial table")
   creatingSpatialFeature.printHello()
   creatingSpatialFeature.creatingAISFeatureClassFromCSVFile()


