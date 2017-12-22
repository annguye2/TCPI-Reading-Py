#-------------------------------------------------------------------------------
# Name:        Define Distance
# Purpose:
#
# Author:      524855
#
# Created:     20/11/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import datetime
from os.path import split
from arcpy import env
env.overwriteOutput = True



class FindDistance:
##    def __init__(self, _inputFC, _projectedFC, _joinFC, _outFC, _spatialRef):
    def __init__(self, _inputFC):

        self.inputFC        = _inputFC
        self.projectedFC    = r"C:/AIS_Data/ais.gdb/PROJECTED_AIS_FC"
        self.joinFC         = r"C:/AIS_Map/ais.gdb/IMT_SYS_SEGMENTS_FC"
##        self.outFC          = _outFC
        self.spatialRef     = arcpy.SpatialReference(3395)
        self.path           = ""
        self.joinedAISFC    = ""

 # create destination feature class using the source as a template to establish schema
    # and set destination spatial reference
    #=============================================================
    def project(self):
        try:
          """ projects self.inputFC to self.projectedFC  using cursors (supports in_memory workspace) """
          path, name = split(self.projectedFC)
          self.path = path
          arcpy.management.CreateFeatureclass(path, name,
                                              arcpy.Describe(self.inputFC).shapeType,
                                              template=self.inputFC,
                                              spatial_reference= self.spatialRef)

          # specify copy of all fields from source to destination
          fields = ["Shape@"] + [f.name for f in arcpy.ListFields(self.inputFC) if not f.required]

          # project source geometries on the fly while inserting to destination featureclass
          with arcpy.da.SearchCursor(self.inputFC, fields, spatial_reference= self.spatialRef) as source_curs, \
               arcpy.da.InsertCursor(self.projectedFC , fields) as ins_curs:
              for row in source_curs:
                ins_curs.insertRow(row)

        except ValueError:
            print "projecting error"

    #============================================================
    def renameFC_To_AIS_FC(self):
        try:
         env.workspace = "C:/AIS_Data/ais.gdb"
         #rename ais_feature to "AIS_FC"
         arcpy.Rename_management("JOINED_AIS_FC", "AIS_FC","FeatureClass")
         print("Rename JOINED_AIS_FC to AIS_FC")

        except ValueError:
            print "projecting error"
    #=============================================================
    # creating output joined-feature class
    def createEmptyFC(self, ref_fc):
     try:
        print ("creating fc")
        fc_workspace = r"C:\AIS_Data\ais.gdb"
        fields = arcpy.ListFields(ref_fc,"FID_*")
        self.joinedAISFC  = "JOINED_AIS_FC"
        created_fc = arcpy.CreateFeatureclass_management(fc_workspace,self.joinedAISFC, "POINT", spatial_reference = arcpy.Describe(self.projectedFC).spatialReference)

        for fc_field in fields:
            arcpy.AddField_management(created_fc, fc_field)

        return created_fc

     except ValueError:
      print "projecting error"
    #=============================================================
    # join feature to SEG_CALE_SYS_FC
    def join(self):
     try:
        fieldmappings = arcpy.FieldMappings()
        # Add all fields from inputs.
        fieldmappings.addTable(self.projectedFC)
        fieldmappings.addTable(self.joinFC)

        # define needed fields
        keeper1 =  arcpy.ListFields(self.projectedFC)
        keeper2 =  arcpy.ListFields(self.joinFC)
        for field in keeper2:
            if field.name == "CABLE_SYS_NAME":
                keeper1.append(field)
                break

        keepers = []
        for field in keeper1:
            keepers.append(field.name)

        # remove unneeded fields
        for field in fieldmappings.fields:
            if field.name not in keepers:
                fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))

        # must creating a fc with all fields above to get the out put
        joinedFC = self.createEmptyFC(self.projectedFC)

        # join features
        arcpy.SpatialJoin_analysis(target_features = self.projectedFC,
        join_features = self.joinFC,
        out_feature_class = joinedFC,
        join_operation = "JOIN_ONE_TO_ONE",
        join_type = "KEEP_ALL",
        field_mapping = fieldmappings,
        match_option="CLOSEST",
        distance_field_name="DIST_METERS")
        #remove empty and unused fields
        arcpy.DeleteField_management(r"C:\AIS_Data\ais.gdb\\" + self.joinedAISFC,["Join_Count", "Field22", "TARGET_FID"])
     except ValueError:
      print "projecting error"
    #=============================================================

##    def distanceFilter(self):
##        filteredAISVesselID  = []
##        #Inputs
##        ais_feature = r"C:\AIS_Data\ais.gdb\JOINED_AIS_FC"
##        cable_segment_feature = r"C:\AIS_Map\ais.gdb\IMT_SYS_SEGMENTS_FC"
##
##        ais_cursor = arcpy.da.SearchCursor(ais_feature, ['SHAPE@', 'OBJECTID', 'Vessel_ID'])
##
##        #loops through each point in the input
##        for row in ais_cursor:
##            ais_geometry = ais_cursor[0]
##            ais_id = ais_cursor[1]
##            cable_segment_cursor = arcpy.da.SearchCursor(cable_segment_feature, ['SHAPE@', 'CABLE_SYS_NAME'])
##            mindist = 10000.00
##            #loops through each line finding the closest line to current point
##            for row in cable_segment_cursor:
##                newgeometry = cable_segment_cursor[0]
##            #distanceTo finds the distance in meters
##                tmpdist = newgeometry.distanceTo(ais_geometry)
##                if tmpdist < mindist:
##                    mindist = tmpdist
##                    cable_sys= cable_segment_cursor[1]
##                    filteredAISVesselID.append(ais_cursor[2])
##                    print ('Vessel ID: ' + str(ais_cursor[2]) +' OBJECT ID: ' + str(ais_cursor[2]) +  ' the closest cable system is ' + cable_sys + ' at a distance of ' + str(mindist))
##
##        print(filteredAISVesselID)
##        #remove ais_id that is not in the range
##        with arcpy.da.UpdateCursor(ais_feature, "Vessel_ID") as cursor:
##            for row in cursor:
####                if row[0] not in filteredAISVesselID:
####                    cursor.deleteRow()
##
##                if (self.findInList(filteredAISVesselID, row[0]) == False):
##                    cursor.deleteRow()
##
##
##        env.workspace = "C:/AIS_Data/ais.gdb"
##        #rename ais_feature to "AIS_FC"
##        arcpy.Rename_management("JOINED_AIS_FC", "AIS_FC")
##        return ais_feature
##    #=============================================================
##
##    def findInList(self, listItems, key):
##        for item in listItems:
##            if key == item:
##                return True
##        return False

     #=============================================================

# This main is for testing purpose
if __name__ == '__main__':

##
##    findDist = FindDistance(  r"C:/AIS_Data/ais.gdb/AIS_FC_TEMP",           #   _inputFC
##                              r"C:/AIS_Data/ais.gdb/PROJECTED_AIS_FC",      #   _projectedFC  as out out name and location
##                              r"C:/AIS_Map/ais.gdb/IMT_SYS_SEGMENTS_FC",    #   _joinFC
##                              arcpy.SpatialReference(3395))             #   _spatialRef


    findDist = FindDistance(  r"C:/AIS_Data/ais.gdb/AIS_FC_TEMP")           #   _inputFC


    findDist.project()
    print('sucessfully projeted fc.')
    findDist.join()
    print('sucessfully joined fc.')
    now = datetime.datetime.now()
    print now.strftime("%Y-%m-%d %H:%M:%S")
##    findDist.distanceFilter()   # find distance
    print ("DONE")
    now = datetime.datetime.now()
    print now.strftime("%Y-%m-%d %H:%M:%S")



