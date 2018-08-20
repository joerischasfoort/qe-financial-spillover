import os

for filename in os.listdir("."):
    print filename
    if 'Marketsize' in filename:
    	os.rename(filename,  (filename[:34] + "_" +filename[34:]))
	#if filename.startswith("M"):
		#print filename
		#  filename[:7] +'_'+filename[7:])
  
 