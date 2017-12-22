#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      524855
#
# Created:     20/11/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy


##
###Set local variables
##fc = point_feature # "C:/Data/Garbo.gdb/trails" #Note:empty feature class
##field = "SHAPE@" #short int, non nullable field
##new_name = "SHAPE@"
##new_alias = "Shape"
##new_type = "geometry"
##new_length = ""
##new_is_nullable = "NULLABLE"
##clear_alias = "FALSE"
##
###Alter the properties of a non nullable, short data type field to become a text field
##arcpy.AlterField_management(fc, field, new_name, new_alias, new_type, new_length, new_is_nullable, clear_alias)


#Inputs

##point_feature = r"Y:\SHARED_DATA\test.gdb\points"
##line_feature = r"Y:\SHARED_DATA\test.gdb\lines"

point_feature = r"C:\AIS_Data\ais.gdb\JOINED_AIS_FC"
line_feature = r"C:\AIS_Data\ais.gdb\IMT_SYS_SEGMENTS_FC"


pointcursor = arcpy.da.SearchCursor(point_feature, ['Shape@', 'OBJECTID'])

#loops through each point in the input
for row in pointcursor:

    geometry = pointcursor[0]
    print ("geometry point " ,geometry)
    point_id = pointcursor[1]
    linecursor = arcpy.da.SearchCursor(line_feature, ['SHAPE@', 'CABLE_SYS_NAME'])
    mindist = 9999999
    #loops through each line finding the closest line to current point
    for row in linecursor:
        newgeometry = linecursor[0]
    #distanceTo finds the distance in meters
        tmpdist = newgeometry.distanceTo(geometry)
        if tmpdist < mindist:
            mindist = tmpdist
            cable_sys= linecursor[1]
    print ('For ' + str(point_id) + ' the closest cable system is ' + cable_sys + ' at a distance of ' + str(mindist))
