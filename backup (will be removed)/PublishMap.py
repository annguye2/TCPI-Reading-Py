#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      524855
#
# Created:     03/11/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Publishes a service to machine myserver using USA.mxd
# A connection to ArcGIS Server must be established in the
#  Catalog window of ArcMap before running this script
import arcpy

# Define local variables
wrkspc = 'C:/AIS_Map'
mapDoc = arcpy.mapping.MapDocument(wrkspc + '/aisx.mxd')

# Provide path to connection file
# To create this file, right-click a folder in the Catalog window and
#  click New > ArcGIS Server Connection
con ='GIS Servers/arcgis on 10.200.76'
serverFolder = "AIS"

# Provide other service details
service = 'AIS'
sddraft = wrkspc + service + '.sddraft'
sd = wrkspc + service + '.sd'
summary = 'General reference map of the Created AIS Live data'
tags = 'AIS'

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
    print "Service successfully published"
else:
    print "Service could not be published because errors were found during analysis."

print arcpy.GetMessages()