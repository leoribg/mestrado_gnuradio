import os
import time
#from teste_leo import *



for i in range (9022, 9280, 2):
#    main(i * 100000, "{0}.txt".format(i))
    if (i < 9075 or i > 9150) :
        s = "python power_final.py --center-freq=" + str(i * 100000) + " --filename=" + str(i) + ".txt"
        print(s)
    

    #if(i < 9075 or i > 9150):
        #s = "timeout 14 python teste_leo.py --center-freq=" + str(i * 100000) + " --filename=" + str(i) + ".txt"
        #main(902800000, 9028)
        #print(s)
        #os.system(s)
        #time.sleep(16)
        #print(s)
    