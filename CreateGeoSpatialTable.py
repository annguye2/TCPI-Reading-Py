#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      524855
#
# Created:     18/10/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
import os
import csv
import arcpy
import shutil
from ConvertTimeZoneModule import *

class CreateGeoSpatialTable:
    def __init__(self, _msg):
        self.msg = _msg
        self.path = r"C:/AIS_Data/"
        self.AisGDB  = "ais.gdb"
        self.aisTable = "ais"
        arcpy.env.workspace = self.path
        self.csvFile = self.path + r"ais_live.csv"
        self.AisGdbPath = self.path + self.AisGDB


    def printHello(self):
        print self.msg
    ##=============================================
    def cleanCSV(self):
        print "Clean CSV"
        csv1 =  'C:/AIS_Data/ais_live.csv'
        csv2 =  'C:/AIS_Data/ais_live_edit.csv'
        with open(csv1,'r') as f, open(csv2,'w') as f1:
            next(f) # skip header line
            next(f)
            for line in f:
                f1.write(line)

        arcpy.Delete_management(csv1)
        shutil.move(csv2,  csv1)
        arcpy.RefreshCatalog("C:\AIS_Data")
        #os.system("TASKKILL /F /IM ArcCatalog.exe")
        #os.system("TASKKILL /F /IM ArcMap.exe")
    ##=============================================
    def importCSVTTable (self):  # Import CSV information to geodata table
        print "Import CSV table"
        arcpy.TableToTable_conversion(self.csvFile, self.AisGdbPath, self.aisTable)

    ##=============================================
    def deleteFiles(self):
        print "Delete all gdb features"
        arcpy.Delete_management("C:/AIS_Data/ais.lyr")
        arcpy.Delete_management("C:/AIS_Data/ais.gdb/ais")
        arcpy.Delete_management("C:/AIS_Data/ais.gdb/AIS_FC")
    ##=============================================
    def removeInvalidRow (self): # remove row that has invalide Lat and Lon
        print "Remove invalid rows"
        fc = "C:/AIS_Data/ais.gdb/ais"
        field = "Longitude"
        cursor = arcpy.SearchCursor(fc)
        with arcpy.da.UpdateCursor(fc, ["Longitude", "Latitude"]) as cursor:
            for row in cursor:
                if row[0] == None:
                    #print "this is null"
                    #print(row.getValue("Vessel_ID"))
                    cursor.deleteRow()

     ##=============================================
    def createAISFeatureClass(self):
        print "Creating Feature Class"
        arcpy.env.workspace = "C:/AIS_Data/ais.gdb"
        # Set the local variables
        in_Table = "ais"
        x_coords = "Longitude"
        y_coords = "Latitude"
        z_coords = ""
        out_Layer = "ais_layer"
        saved_Layer = r"C:\AIS_Data\ais.lyr"
        # Set the spatial reference
        spRef = r"Coordinate Systems\Graphic Coordinate Systems\World\WGS 1984.prj"
        #spRef = r"Coordinate Systems\Projected Coordinate Systems\Utm\Nad 1983\NAD 1983 UTM Zone 11N.prj"
        #spRef = r"GCS_WGS_1984"
        # Make the XY event layer...
        arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
        # Print the total rowsz
        print arcpy.GetCount_management(out_Layer)
        # Save to a layer file
        arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
        arcpy.CopyFeatures_management("ais_layer", "C:/AIS_Data/ais.gdb/AIS_FC")
    ##=============================================
    def creatingAISFeatureClassFromCSVFile(self):
        arcpy.RefreshCatalog(self.path)
        self.cleanCSV()
        self.deleteFiles()
        if not arcpy.Exists(self.AisGdbPath):
            arcpy.CreateFileGDB_management(self.path, self.AisGDB)
            self.importCSVTTable()
##            print ('gdb is NOT  exist')
        else:
##            print ('gdb is  exist')
            if arcpy.Exists("C:/AIS_Data/ais.gdb/ais"):
##                print ("table is exist then remove the ais table")
                arcpy.Delete_management("C:/AIS_Data/ais.gdb/ais")
                self.importCSVTTable()
            else:
                # add new ais table
                self.importCSVTTable()

        self.removeInvalidRow()
        converTimeZone  = ConvertingTimeZone("C:/AIS_Data/ais.gdb/ais")
        converTimeZone.setNewTimeZone()
        self.createAISFeatureClass()
        #pythonaddins.MessageBox('Select a data frame', 'INFO', 0)

