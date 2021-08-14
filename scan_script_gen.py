import os
import time

for i in range (9022, 9280, 2):
    if (i < 9075 or i > 9150) :
        s = "python power_final.py --center-freq=" + str(i * 100000) + " --samp-rate=1000000" + " --bw=100000" + " --filename=" + str(i) + ".txt\n" + "LimeQuickTest"
        print(s)
        s = ""

for i in range (2402, 2482, 2):
    s = "python power_final.py --center-freq=" + str(i * 1000000) + " --samp-rate=2000000" + " --bw=1000000" + " --filename=" + str(i) + ".txt\n" + "LimeQuickTest"
    print(s)
    s = ""