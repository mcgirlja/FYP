import cv2
import numpy as np
import pickle

class precomputeDatabase(object):


    storedImages = [r'C:\pythonImg\HP-ORDER-OF-THE-PHOENIX.jpg',r'C:\pythonImg\OF-MICE-AND-MEN.jpg',r'C:\pythonImg\OLIVER-TWIST.jpg',r'C:\pythonImg\TWILIGHT-BREAKING-DAWN.jpg']
    descriptors = {}


    for image in storedImages:
        storedImg = cv2.imread(image,0)
        orb = cv2.KAZE_create()
        kp2, des2 = orb.detectAndCompute(storedImg, None)
        descriptors[image] = des2 

    #
    # for x,y in descriptors.items():
    #     print(x,y)


    pickle_out = open("dict.pickle","wb")
    pickle.dump(descriptors,pickle_out)
    pickle_out.close()
