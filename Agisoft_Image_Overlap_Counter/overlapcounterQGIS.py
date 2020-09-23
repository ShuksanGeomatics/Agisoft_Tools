##!/usr/bin/env python3
""":"

# Find a suitable python interpreter (adapt for your specific needs) 
for cmd in python3.5 python3 /opt/myspecialpython/bin/python3.5.99 ; do
   command -v > /dev/null $cmd && exec $cmd $0 "$@"
done

echo "OMG Python not found, exiting!!!!!11!!eleven" >2

exit 2

":"""


import traceback
import sys
try:
	import processing
	pth = 'home/gerry/PythonScripts/Agisoft_Tools/Agisoft_Image_Overlap_Counter/Test/'
	processing.runalg("script:splitvectorlayerbyattribute", pth + "testdata.shp", "Id", pth + "split")
	




except:
	tb = sys.exc_info()[2]
	tbinfo = traceback.format_tb(tb)[0]
	print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1]))


#def main():
	
			
#if __name__ == "__main__":
	#main()  

