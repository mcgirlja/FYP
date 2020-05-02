import cv2
import pickle
import glob

class precomputeDatabase(object):

    pathname = '/home/pi/FYP/Files' #path for images and audio.
    storedImages = glob.glob(pathname + '/*.jpg') #grab file path string with jpg extention.
    descriptors = {} #store the image tied with corresponding descriptor values.


    for image in storedImages:
        storedImg = cv2.imread(image,0)
        kaze = cv2.KAZE_create()
        kp2, des2 = kaze.detectAndCompute(storedImg, None)
        descriptors[image] = des2


    pickle_out = open("dict.pickle","wb") #create a source file to pickle the data to.
    pickle.dump(descriptors,pickle_out) #dump the dictionary into specified location.
    pickle_out.close()


    print("Descriptors computed")
