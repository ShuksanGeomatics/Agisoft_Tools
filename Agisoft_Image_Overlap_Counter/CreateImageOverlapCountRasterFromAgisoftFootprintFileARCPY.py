'''This script will take the Agisoft Metashape\Photoscan footprint output shapefile and create a new raster dataset that counts the overlap
for a particular drone flight.  The input shapefile should reference a projected coordinate reference system
to ensure the cell size of the output raster is meaningful.
'''
import sys, traceback
try:
    #import standard libraries...
    import os
    import arcpy
    from arcpy.sa import *
    arcpy.CheckOutExtension("Spatial")
    arcpy.AddMessage("Create Agisoft Image Overlay Count Raster...") 
    arcpy.AddMessage("Copyright 2019, Gerry Gabrisch ,  Creative Commons Attribution 4.0 International (CCBY 4.0)...")
    arcpy.AddMessage("Working...")
      
    ###########################################################################
    #        USER DEFINED PARAMETERS     #
    
    #this is the full path to the agisoft footprint output file...
    input_FC = r"C:\gTemp\Drone\SkookumEdfroPhase2_20191211\ProjectFiles\imagefootprints\footprints.shp"
    
    #this is the path to an empty directory.  This directory will store the interum data.... 
    outFolder = r"C:\gTemp\Drone\SkookumEdfroPhase2_20191211\ProjectFiles\imagefootprints"
    
    #This is the full path and name of the output raster that will store the image overlap count....
    outRas = r"C:\gTemp\Drone\SkookumEdfroPhase2_20191211\ProjectFiles\imagefootprints\imagecount"
    
    #This is the output raster cell size in the input_FC coordinate reference system.
    cellSize = 0.1
    
    
    ##########################################################################  
    arcpy.env.overwriteOutput = True
    arcpy.env.scratchWorkspace = outFolder  
    arcpy.env.workspace = outFolder     
    #add thefield to hold the value of the raster....
    fieldList = arcpy.ListFields(input_FC)
    if 'imgcnt' not in fieldList:
        arcpy.AddMessage("Adding field...")
        arcpy.AddField_management(input_FC, 'imgcnt', "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")    
    #populate that field by one....
    arcpy.AddMessage("Populating field...")
    arcpy.CalculateField_management(input_FC, 'imgcnt', 1)
    arcpy.AddMessage("Converting rows to rasters...")
    layer = arcpy.MakeFeatureLayer_management(input_FC)
    OID_field = arcpy.Describe(layer).OIDFieldName # get OID/FID field name
    fields = [OID_field, "imgcnt"]
    #Sift through the shapefile and export each record as a raster with a value of 1
    with arcpy.da.SearchCursor(layer,OID_field) as cursor: # create cursor  
        for row in cursor: 
            where = '{0} = {1}'.format(arcpy.AddFieldDelimiters(layer,OID_field),row[0]) # set up where clause
            arcpy.SelectLayerByAttribute_management(layer,"NEW_SELECTION",where) # select the current feature  
            arcpy.FeatureToRaster_conversion (layer, fields[1], outFolder+"\\"+str(row[0]), cellSize)
    arcpy.AddMessage("Adding output rasters together...")
    
    #create a list of rasters 
    arcpy.env.workspace = outFolder
    rasters = arcpy.ListRasters('','')  
    i = 0  
    #loop through rasters in list and add them together
    for raster in rasters:  
        print "processing raster: %s" %os.path.join(outFolder, raster)  
        #convert nodata to zero  
        out1 = Con(IsNull(raster), 0, raster)
        #sum rasters together  
        if i == 0:  
            out2 = out1  
            i += 1  
        else:  
            out2 = out2 + out1  
            i += 1  
    #save final output  
    out2.save(outRas)
    arcpy.AddMessage("\n  Finished running script..." + "\n")
    del arcpy
except arcpy.ExecuteError: 
    msgs = arcpy.GetMessages(2) 
    arcpy.AddError(msgs)  
    print msgs
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)
    print pymsg + "\n"
    print msgs
