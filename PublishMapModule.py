#-------------------------------------------------------------------------------
# Name:        Create and Public Map
# Purpose:
# Author:      524855
# Created:     12/08/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import arcpy
import datetime


class PublishMap:

   def __init__(self):
    self.mapLocation = r"C:\AIS_Map\ais.mxd"
    self.sourceLayerLocation = r"C:\AIS_Map\Vessels.lyr"
    self.layerName ="Vessel"

    # creating Vessel and add layer into existen map
    # Note: ais map has to be created before hand
    # Arcpy can handle to create the map, but the process require lot more DOM objects which could slow our process
    # for the most convenience, we should create the map and named it as ais.mxd
   def removeMapDefinitionFile(self, fileName):
     if arcpy.Exists(fileName): #filename = full path
        arcpy.Delete_management(fileName)

   def createVesselMapDocument(self):
    try:

        AIS_fc = r"C:/AIS_Data/ais.gdb/AIS_FC"  #data source
        arcpy.MakeFeatureLayer_management(AIS_fc, self.layerName)  #making layer from data source
        print "mapping mxd map"
        vesselMxd = arcpy.mapping.MapDocument(self.mapLocation)
##        print "adding map to data frame"
        dataFrame = arcpy.mapping.ListDataFrames(vesselMxd)[0]

##        print "remove Vessel layer if exist"
        for layer in arcpy.mapping.ListLayers(vesselMxd , "", dataFrame):
             if layer.name.lower() == 'vessel':
               arcpy.mapping.RemoveLayer(dataFrame , layer)


##        print "adding Vessel layer to Map"
        layer = arcpy.mapping.Layer(self.layerName)
        arcpy.mapping.AddLayer(dataFrame, layer, "AUTO_ARRANGE")
##        print "get Vessel layer from map"
        updateLayer = arcpy.mapping.ListLayers(vesselMxd, self.layerName, dataFrame)[0]
##        print "get Vessel layer to copy all symbologies"
        sourceLayer = arcpy.mapping.Layer(self.sourceLayerLocation)
##        print "add customed symbologies into Vessle layer"
        arcpy.mapping.UpdateLayer(dataFrame,updateLayer,sourceLayer, symbology_only = True)
##        print "update map(save)"
        vesselMxd.save()
    except ValueError:
        print "createVesselMapDocument error! "
    ##    del vesselMap

##==================================================
   def publishMapToArcGISServer(self):
    try:

        # Define local variables
        wrkspc = 'C:/AIS_Map'
        mapDoc = arcpy.mapping.MapDocument(wrkspc + '/ais.mxd')

        con ='GIS Servers/arcgis on 10.200.76'  # double click on arcgis server connection and copy ONLY arcgis on 10.200.76 ( see screen short "how to copy ArcGIS ServerStrig")
        serverFolder = "AIS"

        # Provide other service details
        service = 'AIS'
        sddraft = wrkspc + service + '.sddraft'
        sd = wrkspc + service + '.sd'
        summary = 'General reference map of the Created AIS Live data'
        tags = 'Vessel'

        # Create service definition draft
        arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER', con, True, serverFolder, summary, tags)

        # Analyze the service definition draft
        analysis = arcpy.mapping.AnalyzeForSD(sddraft)

        # Print errors, warnings, and messages returned from the analysis
        print "The following information was returned during analysis of the MXD:"
        for key in ('messages', 'warnings', 'errors'):
          print '----' + key.upper() + '---'
          vars = analysis[key]
          for ((message, code), layerlist) in vars.iteritems():
            print '    ', message, ' (CODE %i)' % code
            print '       applies to:',
            for layer in layerlist:
                print layer.name,
            print

        # Stage and upload the service if the sddraft analysis did not contain errors
        if analysis['errors'] == {}:
            # Execute StageService. This creates the service definition.
            arcpy.StageService_server(sddraft, sd)

            # Execute UploadServiceDefinition. This uploads the service definition and publishes the service.
        ##    arcpy.UploadServiceDefinition_server(sd, con)
            arcpy.UploadServiceDefinition_server(sd, con, "", "", "EXISTING", serverFolder)
            print "Service successfully published AIS feature to ArcGIS Services"
        else:
            print "Service could not be published because errors were found during analysis."

    except ValueError:
        print "publishMapToArcGISServer error! "
##==================================================
   # call this function in another module/class or main
   def executePublishProcess (self):

    try:
        print "check existen Map definition file"
        self.removeMapDefinitionFile("C:\AIS_MapAIS.sd")
        print "Creating Vessle Map documen"
        self.createVesselMapDocument()
        print "Publishing Map"
        now = datetime.datetime.now()
        print now.strftime("%Y-%m-%d %H:%M:%S")
        self.publishMapToArcGISServer()
        print "Publishing process is done"
        now = datetime.datetime.now()
        print "End: "
        print now.strftime("%Y-%m-%d %H:%M:%S")

    except ValueError:
        print "executePublishProcess error! "

##==================================================
#this main is for testing purpose
if __name__ == '__main__':

   publishMap = PublishMap ()
   publishMap.executePublishProcess()

