#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      524855
#
# Created:     06/11/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy




def appendFeatureClasses(fc1, fc2):
    try:
     print "Merge Feature Classes"
     arcpy.env.workspace = "C:/AIS_DATA"
     arcpy.Append_management([fc2], fc1, "NO_TEST","","")
     print "Appending completed"
    except:
     print("error: ", arcpy.GetMessages())



if __name__ == '__main__':

    fc1 = r"C:\AIS_Data\ais.gdb\AIS_FC"
    fc2 = r"C:\AIS_Data\ais.gdb\AIS_FC_TEMP"
##    appendFeatureClasses(fc1, fc2)
    arcpy.Delete_management("C:/AIS_Data/ais.gdb/AIS_FC_TEMP") #remove AIS_FC_TEMP after merge table
##    mergeFeatureClass(FDSName, fc1, fc2)

