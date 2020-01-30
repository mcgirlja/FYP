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
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            print("The image has been captured: " + str(ret))
        else:
            ret = False
        img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #this converts the colours to RGB from BGR
        self.queryImage = img1 #assigned the captured image to be used be the following method.
        #self.queryImage = 'C:\pythonImg\OF-MICE-AND-MEN.jpg'
        return img1

    def get_Matches_Orb(self,capturedImage):

        for image in self.storedImages:
            print(image)
            storedImg = cv2.imread(image,0)

            orb = cv2.ORB_create()
            #orb = cv2.KAZE_create()

            kp1, des1 = orb.detectAndCompute(capturedImage, None) #this finds keypoints and descriptors with SIFT
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
                self.bestKP1 = kp1 # keypoints for the queryImage
                self.bestKP2 = kp2 # keypoints for the best matched image/ one with highest number
                if(len(self.matches) > 15): # set as a temporary threshold so it doesnt return matches with the ceiling.
                    self.image = image
                else:
                    self.image = None

            print("curr="+str(len(good)))
            print("best="+str(len(self.matches)))

        return(self.image)

        # img3 = cv2.drawMatchesKnn(self.queryImage,self.bestKP1,self.matchedImage,self.bestKP2,self.matches, None, flags=2)
        # plt.imshow(img3)
        # plt.show()
        # self.bookFound = True #sets the variable true if a match has been found.


    def bookLookup(self):
        counter = 0
        match_found = None
        current_matching = None
        while True:
            captured_img = self.captureImage()
            match_found = self.get_Matches_Orb(captured_img)
            if(match_found != None):
                if(current_matching == match_found):
                    counter += 1
                else:
                    current_matching = match_found
                    counter = 0
            if(counter >= 2):
                self.read_Book(current_matching)
                counter = 0
                break


    def read_Book(self, match):
        print("IMAGE FOUND. IT IS = " + match)








testobj = imageCapture()
# testobj.captureImage()
# testobj.get_Matches_Orb()
testobj.bookLookup()
