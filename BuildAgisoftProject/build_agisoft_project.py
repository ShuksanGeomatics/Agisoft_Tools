#!/usr/bin/env python3
'''This script build a directory tree for holding my Agisoft Photoscan/Metashape projects...
The user need to set the parent_dir prior to running this script...
Gerry Gabrisch, 2020'''
import sys
import os
import traceback
try:
    project_name = input('Enter the name of the project...> ')
    
    # Parent Directory path to be set by the user to their default agisoft project directory...
    parent_dir = "/home/gerry/Drone"
      
    # Project name....
    project_path = os.path.join(parent_dir, project_name) 
    os.mkdir(project_path)
    print("making directory :" + project_path)
    
    proj_dir = os.path.join(project_path, 'ProjectFiles') 
    os.mkdir(proj_dir) 
    print("   making directory :" + proj_dir)
    
    ortho_dir = os.path.join(project_path, 'Orthomosaic') 
    os.mkdir(ortho_dir) 
    print("   making directory :" + ortho_dir)
    
    image_dir = os.path.join(project_path, 'Images') 
    os.mkdir(image_dir) 
    print("   making directory :" + image_dir)
    
    gpc_dir = os.path.join(project_path, 'GCP') 
    os.mkdir(gpc_dir)
    print("   making directory :" + gpc_dir)
    
    surface_dir = os.path.join(project_path, 'SurfaceModel') 
    os.mkdir(surface_dir) 
    print("   making directory :" + surface_dir)    
    
    dem_dir = os.path.join(surface_dir, 'DEM') 
    os.mkdir(dem_dir)
    print("      making directory :" + dem_dir)
    
    hs_dir = os.path.join(surface_dir, 'Hillshade') 
    os.mkdir(hs_dir)
    print("      making directory :" + hs_dir)
    print('done without error')
    
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1]))