import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle
import simpleaudio as sa
import sys
import RPi.GPIO as GPIO
import glob

class imageCapture(object):


    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12, GPIO.IN)
        GPIO.output(11,GPIO.LOW)
        self.matches = [] # used in orb method as a variable to pass matches. len(self.matches) will return how many matches there are.
        self.storedImageDes = None #image descriptors paired with file path string.
        self.imagesWithAudio = {}


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
        self.storedImageDes = pickle.load(infile)
        infile.close()


    def get_matches_Kaze(self, capturedImage):

        for image,des2 in self.storedImageDes.items():
            print(image)
            storedImg = cv2.imread(image,0)
            orb = cv2.KAZE_create()
            kp1, des1 = orb.detectAndCompute(capturedImage, None) #this finds keypoints and descriptors with SIFT
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1,des2, k=2)

            # Apply the ratio test
            good = []
            for m,n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])

            if(len(self.matches) < len(good)):
                self.matches = good
                if(len(self.matches) > 20): # set as a temporary threshold so it doesnt return matches with the ceiling.
                    self.image = image
                else:
                    self.image = None

            print("curr="+str(len(good)))
            print("best="+str(len(self.matches)))

        good = []  # resets the matches for the constant loop once a match is found.
        self.matches = [] # resets the matches for the constant loop once a match is found.
        return(self.image) # returns the match as an image file path string.


    def bookLookup(self):
        while True:
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
                if(counter >= 1):
                    self.read_Book(current_matching)
                    counter = 0
                    round = 0
                    break

    def populate_dict(self):
        pathname = '/home/pi/FYP/Image&Audio'
        globjpg = glob.glob(pathname + '/*.jpg')
        globwav = glob.glob(pathname + '/*.wav')

        for image in globjpg:
            for sound in globwav:
                if(image[:-4] == sound[:-4]):
                    self.imagesWithAudio[image] = sound #Tie the jpg with the wav in a dict if match found.

    def read_Book(self, match):
        print("IMAGE FOUND. IT IS = " + match)

        for x,y in self.imagesWithAudio.items(): # dictionary used to tie audio with an image and play the corresponding audio with the matched image path.
            if(match == x):
                wave_obj = sa.WaveObject.from_wave_file(y)
                play_obj = wave_obj.play()
                GPIO.output(11,GPIO.HIGH)

                while play_obj.is_playing():
                    input_value = GPIO.input(12)
                    if input_value == False: #Detects if the button is pressed.
                        print('Button has been pressed')
                        while input_value == False: #Stops it from picking up mulitple button presses.
                            input_value = GPIO.input(12)
                        play_obj.stop() #stops the book if the button has been pressed.
                        GPIO.output(11,GPIO.LOW)
                    time.sleep(0.5)  #small buffer so that the while loop isn't checking constantly which can be intensive on the OS.

                play_obj.wait_done()
            else:
                continue



testobj = imageCapture()
testobj.populate_dict()
testobj.unpickle_database()
testobj.bookLookup()
