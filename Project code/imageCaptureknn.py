import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle

class imageCapture(object):


    def __init__(self):
        self.matches = [] # used in orb method as a variable to pass matches. len(self.matches) will return how many matches there are.
        self.matchedImage = None #only used when using the show() method and drawing the matches for visual matches
        self.storedImages2 = None


    def captureImage(self):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            print("The image has been captured: " + str(ret))
        else:
            ret = False
        img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #this converts the colours to RGB from BGR
        return img1


    def unpickle_database(self):
        infile = open("dict.pickle","rb")
        self.storedImages2 = pickle.load(infile)
        infile.close()


    def get_matches_Kaze(self, capturedImage):

        for image,des2 in self.storedImages2.items():
            print(image)

            storedImg = cv2.imread(image,0)

            #orb = cv2.ORB_create()
            orb = cv2.KAZE_create()

            kp1, des1 = orb.detectAndCompute(capturedImage, None) #this finds keypoints and descriptors with SIFT

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
                if(len(self.matches) > 15): # set as a temporary threshold so it doesnt return matches with the ceiling.
                    self.image = image
                else:
                    self.image = None

            print("curr="+str(len(good)))
            print("best="+str(len(self.matches)))

        return(self.image)


    def bookLookup(self):
        counter = 0
        round = 0
        match_found = None
        current_matching = None
        while True:
            round += 1
            print("Round " + str(round))
            captured_img = self.captureImage()
            match_found = self.get_matches_Kaze(captured_img)
            if(match_found != None):
                if(current_matching == match_found):
                    counter += 1
                else:
                    current_matching = match_found
                    counter = 0
            if(counter >= 2):
                self.read_Book(current_matching)
                counter = 0
                round = 0
                break


    def read_Book(self, match):
        print("IMAGE FOUND. IT IS = " + match)



testobj = imageCapture()
testobj.unpickle_database()
testobj.bookLookup()
#testobj.captureImage()
#testobj.get_matches_Kaze()
# testobj.get_Matches_Orb()
