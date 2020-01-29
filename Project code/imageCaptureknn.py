import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

class imageCapture(object):


    def __init__(self):
        self.queryImage = None #image taken from the camera
        self.storedImages = [r'C:\pythonImg\HP-ORDER-OF-THE-PHOENIX.jpg',r'C:\pythonImg\OF-MICE-AND-MEN.jpg',r'C:\pythonImg\OLIVER-TWIST.jpg',r'C:\pythonImg\TWILIGHT-BREAKING-DAWN.jpg']
        self.bookFound = False # this variable is set to True when a suitable book match has been found.
        self.matches = [] # used in orb method as a variable to pass matches. len(self.matches) will return how many matches there are.
        self.matchedImage = None # used in orb method to use in show()

    def captureImage(self):
        time.sleep(2.5)
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            print("The image has been captured: " + str(ret))
        else:
            ret = False
        img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #this converts the colours to RGB from BGR
        self.queryImage = img1 #assigned the captured image to be used be the following method.


    def get_Matches_Orb(self):


        for image in self.storedImages:
            print(image)
            storedImg = cv2.imread(image,0)

            orb = cv2.ORB_create()

            kp1, des1 = orb.detectAndCompute(self.queryImage,None) #this finds keypoints and descriptors with SIFT
            kp2, des2 = orb.detectAndCompute(storedImg,None)

            # BFMatcher with default params
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1,des2, k=2)

            # Apply the ratio test
            good = []
            for m,n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])

            if(len(self.matches) < len(good)):
                self.matches = good
                self.matchedImage = storedImg

            print("curr="+str(len(good)))
            print("best="+str(len(self.matches)))


        img3 = cv2.drawMatchesKnn(self.queryImage,kp1,self.matchedImage,kp2,self.matches, None, flags=2)
        plt.imshow(img3)
        plt.show()
        self.bookFound = True #sets the variable true if a match has been found.

    def get_MatchedImage(self):
        return self.matchedImage

    def bookLookup(self):
        counter = 0
        image = None
        if(counter < 5):
            while True:
                self.captureImage()
                self.get_Matches_Orb()
                if(image == None):
                    image = self.matchedImage
                    if()
                if(image === self.matchedImage):
                    counter += 1



                break






testobj = imageCapture()
testobj.bookLookup()
#testobj.captureImage()
#testobj.get_Matches_Orb()
