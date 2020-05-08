import cv2
import pickle
import glob
import time

class precomputeDatabase(object):
    
    def computeDescriptors(self):
        
        pathname = '/home/pi/FYP/Files' #path for images and audio.
        storedImages = glob.glob(pathname + '/*.jpg') #grab file path string with jpg extention.
        descriptors = {} #store the image tied with corresponding descriptor values.
        
        start_time = time.time()
    
        for image in storedImages:
            storedImg = cv2.imread(image,0)
            kaze = cv2.KAZE_create()
            kp2, des2 = kaze.detectAndCompute(storedImg, None)
            descriptors[image] = des2 
            print(image + " Computed")
        
        end_time = time.time()
        print("This took " + str(end_time - start_time) + " seconds.") #prints the time it takes to compute all of the descriptors.

        pickle_out = open("dict.pickle","wb") #create a source file to pickle the data to.
        pickle.dump(descriptors,pickle_out) #dump the dictionary into specified location.
        pickle_out.close() 
        
        
        print("Descriptors computed")

         

def main():
    testobj = precomputeDatabase()
    testobj.computeDescriptors()
        
    
if __name__ == "__main__":
    main()
    
