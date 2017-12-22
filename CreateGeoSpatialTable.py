#-------------------------------------------------------------------------------
# Name:        mCreateGeoSpatialTablele1
# Purpose:
#
# Author:      An Nguyen
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
from FilterDuplicationsModule import *
from DefineDistanceModule import *


env.overwriteOutput = True

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
        try:

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

        except ValueError:
            print "cleanCSV error"

    ##=============================================
    def importCSVTTable (self):  # Import CSV information to geodata table
        try:
            print "Import CSV table"
            arcpy.TableToTable_conversion(self.csvFile, self.AisGdbPath, self.aisTable)

        except ValueError:
            print "importCSVTTable error"

    ##=============================================
    def deleteFiles(self):
        try:

            print "Delete all gdb features"
            arcpy.Delete_management("C:/AIS_Data/AIS_layer_temp.lyr")
            arcpy.Delete_management("C:/AIS_Data/ais.gdb/ais")
    ##        arcpy.Delete_management("C:/AIS_Data/ais.gdb/AIS_FC")
        except ValueError:
            print "deleteFiles"

    ##=============================================
    def removeInvalidRow (self): # remove row that has invalide Lat and Lon
        try:
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
        except ValueError:
            print "deleteFiles"

     ##=============================================
    def createAISFeatureClass(self, fc, layerName):
        try:
            print "Creating Feature Class"
            in_Table = "ais"
            x_coords = "Longitude"
            y_coords = "Latitude"
            z_coords = ""
            out_Layer = "ais_layer"
            saved_Layer = layerName #r"C:\AIS_Data\ais.lyr"
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
    ##        arcpy.CopyFeatures_management("ais_layer", "C:/AIS_Data/ais.gdb/AIS_FC_Tmp")
            arcpy.CopyFeatures_management("ais_layer", "C:/AIS_Data/ais.gdb/" + fc)

        except ValueError:
            print "deleteFiles"


##===================================================
    def creatingAISFeatureClassFromCSVFile(self):
        try:

            print "START creating geospatial features"
            arcpy.RefreshCatalog(self.path)
            self.cleanCSV()
            filterDuplication = RemoveDup('C:/AIS_Data/ais.gdb/ais')
            converTimeZone    = ConvertingTimeZone("C:/AIS_Data/ais.gdb/ais")
    ##        distantFilter     = FindDistance(r"C:/AIS_Data/ais.gdb/AIS_FC_TEMP")

            self.deleteFiles()
            if not arcpy.Exists(self.AisGdbPath):
                arcpy.CreateFileGDB_management(self.path, self.AisGDB)
                print ('gdb is NOT  exist. Create AIS GDB')
                self.importCSVTTable()
                self.removeInvalidRow()
                #filter duplication
                filterDuplication.filterDuplicationRecords()
                #creating TimeZone
                converTimeZone.setNewTimeZone()
                #creating temp_AIS_FC()
                self.createAISFeatureClass("AIS_FC_TEMP", r"C:\AIS_Data\AIS_layer_temp")
                #set projection for joining
                distantFilter     = FindDistance(r"C:/AIS_Data/ais.gdb/AIS_FC_TEMP")
                distantFilter.project()
                print('sucessfully projeted fc.')
                #join to SYS_SEGMENT_CABLE_SYS
                distantFilter.join()
                print('sucessfully joined with SYS_SEGMENT_SYS.')
                # filter the distance from AIS to Cable System
    ##            distantFilter.distanceFilter()   # find distance
                distantFilter.renameFC_To_AIS_FC()
                print "Successful created and filtered the distance AIS_FC"

            else:
                print ('GDB is already existed')
                if arcpy.Exists("C:/AIS_Data/ais.gdb/AIS_FC"):
                    print ("AIS_FC is already created", "Remove ais table", "Create new ais table")
                    arcpy.Delete_management("C:/AIS_Data/ais.gdb/ais") #remove ais table
                    self.importCSVTTable()  # re-creating geospatial table with latest data
                    self.removeInvalidRow()
                    filterDuplication.filterDuplicationRecords()
                    converTimeZone.setNewTimeZone()
                    print "Creating AIS_FC_Temp"
                    self.createAISFeatureClass("AIS_FC_TEMP", r"C:\AIS_Data\AIS_layer_temp")
                    print "Successfull created AIS_FC_TEMP"

                    distantFilter     = FindDistance(r"C:/AIS_Data/ais.gdb/AIS_FC_TEMP")
                    distantFilter.project()
                    print('sucessfully projeted fc.')
                    #join to SYS_SEGMENT_CABLE_SYS
                    distantFilter.join()
                    print('sucessfully joined with SYS_SEGMENT_SYS.')
                    # filter the distance from AIS to Cable System
    ##                distantFilter.distanceFilter()   # find distance


                    self.appendFeatureClasses(r"C:\AIS_Data\ais.gdb\AIS_FC", r"C:\AIS_Data\ais.gdb\JOINED_AIS_FC")
                    print "Remove AIS_FC_TEMP and AIS_layer_temp.lyr after successfully appeding"
                    arcpy.Delete_management("C:/AIS_Data/ais.gdb/AIS_FC_TEMP") #remove AIS_FC_TEMP after merge table
                    arcpy.Delete_management("C:\AIS_Data\AIS_layer_temp.lyr")

        except ValueError:
            print "creatingAISFeatureClassFromCSVFile"

    ##=============================================
    ## Appending AIS_FC_TEMP with AIS_FC
    def appendFeatureClasses(self, fc1, fc2):

        print "Merge AIS_FC_TEMP to AIS_FC"
        try:
         arcpy.env.workspace = "C:/AIS_DATA"
         arcpy.Append_management([fc2], fc1, "NO_TEST","","")
         print "Appending completed"
        except:
         print("error: ", arcpy.GetMessages())
