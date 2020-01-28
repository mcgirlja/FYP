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
        self.avgMatches = 0 #used to set the threshold and return no book if it hasnt been met.

    def captureImage(self):
        time.sleep(2.5)
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            print("The image has been captured: " + str(ret))
        else:
            ret = False
        img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #this converts the colours to RGB from BGR
        self.queryImage = img1 #assigns this to be used for
        self.queryImage = cv2.imread(r'C:\pythonImg\HP-ORDER-OF-THE-PHOENIX.jpg',0)


    def get_Matches_Orb(self):


        for image in self.storedImages:
            print(image)
            storedImg = cv2.imread(image,0)

            orb = cv2.ORB_create()

            kp1, des1 = orb.detectAndCompute(self.queryImage,None) #this finds keypoints and descriptors with SIFT
            kp2, des2 = orb.detectAndCompute(storedImg,None)

            #bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) #create a bfMatcher object
            # matches = bf.match(des1,des2) #Match descriptors
            # matches = sorted(matches, key = lambda x:x.distance) #sorts them in order of their distance - lowest distance first.

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
            self.avgMatches = self.avgMatches + len(good)
            print("best="+str(len(self.matches)))


        avg = self.avgMatches / len(self.storedImages) #here i am trying to set a threshold to return the right book but when the wrong book is provided it will return nothing.
        if(len(self.matches) * 0.70 < avg):
            print("No suitable book found")
        else:

            # img3 = cv2.drawMatches(self.queryImage,kp1,self.matchedImage,kp2,self.matches,None, flags=2) #helps us to draw the matches
            img3 = cv2.drawMatchesKnn(self.queryImage,kp1,self.matchedImage,kp2,self.matches, None, flags=2)
            plt.imshow(img3)
            plt.show()
            self.bookFound = True #sets the variable true if a match has been found.

    def get_Matches_flann(self):

        img2 = cv2.imread(r'C:\pythonImg\HP-ORDER-OF-THE-PHOENIX.jpg',0) # trainImage

        # Initiate SIFT detector
        sift = cv2.SIFT()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(self.queryImage,None)
        kp2, des2 = sift.detectAndCompute(img2,None)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   # or pass empty dictionary

        flann = cv2.FlannBasedMatcher(index_params,search_params)

        matches = flann.knnMatch(des1,des2,k=2)

        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in xrange(len(matches))]

        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i]=[1,0]

        draw_params = dict(matchColor = (0,255,0),
                           singlePointColor = (255,0,0),
                           matchesMask = matchesMask,
                           flags = 0)

        img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

        plt.imshow(img3,),plt.show()



testobj = imageCapture()
testobj.captureImage()
testobj.get_Matches_Orb()






        #plt.imshow(img1)
        #plt.title('Test title')
        #plt.xticks([])
        #plt.yticks([])
        #plt.show()
        #cap.release()
        #cap.destoryAllWindows()
