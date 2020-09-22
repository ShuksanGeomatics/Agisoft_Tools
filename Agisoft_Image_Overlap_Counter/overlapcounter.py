import sys
import traceback
#import pyshape
#import georaster
from osgeo import gdal, ogr


try:
    print ("worked")
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1]))
