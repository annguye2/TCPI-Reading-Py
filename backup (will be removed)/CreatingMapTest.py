#-------------------------------------------------------------------------------
# Name:        Create and Public Map
# Purpose:
# Author:      524855
# Created:     12/08/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import arcpy



def mappingMXD():
    FC = r"C:/AIS_Data/ais.gdb/AIS_FC"
    arcpy.MakeFeatureLayer_management(FC, "Vessel")
    print "1"
    MXD = arcpy.mapping.MapDocument(r"C:\AIS_Map\ais.mxd")
    print "2"
    DF = arcpy.mapping.ListDataFrames(MXD)[0]
    print "3"
    layer = arcpy.mapping.Layer("Vessel")
    arcpy.mapping.AddLayer(DF, layer, "AUTO_ARRANGE")
    updateLayer = arcpy.mapping.ListLayers(MXD, "Vessel", DF)[0]
    sourceLayer = arcpy.mapping.Layer(r"C:\AIS_Map\Vessels.lyr")
    arcpy.mapping.UpdateLayer(DF,updateLayer,sourceLayer, symbology_only = True)



    print "4"


    MXD.save()
    print "Done"
##    del MXD


if __name__ == '__main__':

    mappingMXD()
