#-------------------------------------------------------------------------------
# Name:        Filter Duplication Records in AIS Table
# Purpose:
#
# Author:      An Nguyen
#
# Created:     13/11/2017
# Copyright:   (c) 524855 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
env.overwriteOutput = True
##=======================================
class Vessel:
    vesselID = ""
    objectID = ""
    def __init__(self, _VesselID, _ObjectID):
        self.objectID = _ObjectID
        self.vesselID = _VesselID

    def compareVessel (self, v1, v2):
        return v1.objectID > v2.objectID

    def getOjectID(self, v):
        return v.objectID

    def getVesselID(self, v):
        return v.vesselID
##========================================

class RemoveDup:
     def __init__(self, _ais):
        self.fc = _ais

     def getListVesselInfo(self, fc,vesselObjs):
        tmpVesselIDs = []
        cursor = arcpy.SearchCursor(self.fc)
        for row in cursor:
            vObject = Vessel(row.getValue("Vessel_ID"),row.getValue("OBJECTID"))
            vesselObjs.append(vObject)
            tmpVesselIDs.append(row.getValue("Vessel_ID"))

        return list(set(tmpVesselIDs))
    ##    return  [item for item, count in collections.Counter(tmpVesselIDs).items() if count > 1]

##===================================================='
     def collectValidVesselObjectIDs(self, vesselIDs, vesselObjs):
        validVesselIDs = []
        for vID in vesselIDs:
            greatest = 0
            for v in vesselObjs:
                if  int(vID) == int(v.vesselID):
                    if int(v.objectID) > greatest:
                        greatest = int(v.objectID)
                       # print("great test   :", greatest)
            validVesselIDs.append(greatest)
        return validVesselIDs
##===================================================
     def removeDuplication(self,validVesselObjectIDs):
       with arcpy.da.UpdateCursor(self.fc, ["Vessel_ID","OBJECTID"]) as cursor:
           for row in cursor:
             if row[1] not in validVesselObjectIDs:
              print row [1]
              cursor.deleteRow()

##===================================================
     def filterDuplicationRecords(self):
       try:
           vesselObjs = []
           distinctVesselIDs = self.getListVesselInfo(self.fc, vesselObjs)
           validVesseIDs = self.collectValidVesselObjectIDs(distinctVesselIDs, vesselObjs)
           self.removeDuplication(validVesseIDs)
       except ValueError:
           print ("Filter Duplication Err!")


##======================End of reove Dup Class=============================



##==================== TESTING PURPOSE ================================
def displayObjects(vesselObjs):
    for v in vesselObjs:
        print v.vesselID, "            ", v.objectID

def displayVesselID (vList):
    for v in  vList:
        print v

##===========================END TEST==========================

if __name__ == '__main__':

   fc = r'C:\AIS_Map\ais.gdb\ais'
   filterDuplication = RemoveDup(fc)
   filterDuplication.filterDuplicationRecords(fc)
   print ("END MAIN")



