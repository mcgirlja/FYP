import cv2
import time
import pickle
import simpleaudio as sa
import RPi.GPIO as GPIO
import glob

class pibook(object):


    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12, GPIO.IN)
        GPIO.output(11,GPIO.LOW)
        self.matches = [] # used in get_matches_kaze() method as a variable to pass matches.
        self.storedImageDes = None #image descriptors paired with file path string.
        self.imagesWithAudio = {}  #Used to pair image file path string with corresponding audio path string.
        
    
    def capture_Image(self):
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
        self.storedImageDes = pickle.load(infile) #stores the precomputed descriptors.
        infile.close()


    def get_matches_Kaze(self, capturedImage):
        
        for image,des2 in self.storedImageDes.items():
            print(image)
            kaze = cv2.KAZE_create() #initialise feature descriptor.
            kp1, des1 = kaze.detectAndCompute(capturedImage, None) #this finds keypoints and descriptors.
            bf = cv2.BFMatcher() #initalise brute-force feature matcher.
            matches = bf.knnMatch(des1,des2, k=2) #match features.
            
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

            print("current book="+str(len(good))+" matches")
            print("best so far="+str(len(self.matches))+ " matches")

        good = []  # resets the matches for the constant loop once a match is found.
        self.matches = [] # resets the matches for the constant loop once a match is found.
        return(self.image) # returns the match as an image file path string.


    def book_Lookup(self):
        while True:
            counter = 0
            round = 0
            match_found = None
            current_matching = None
            start_time = time.time()
            while True:
                round += 1
                print("Round " + str(round))
                captured_img = self.capture_Image()#captured image
                match_found = self.get_matches_Kaze(captured_img) #wait for matches.
                if(match_found != None):
                    if(current_matching == match_found):
                        counter += 1
                    else:
                        current_matching = match_found
                        counter = 0
                if(counter >= 1): #return the same book twice in a row.
                    end_time = time.time()
                    print("This took " + str(end_time - start_time) + " seconds.")
                    self.read_Book(current_matching) #pass jpg book cover image to read book.
                    counter = 0
                    round = 0
                    break
                
    def populate_dict(self):
        pathname = '/home/pi/FYP/Files' 
        globjpg = glob.glob(pathname + '/*.jpg') #find images
        globwav = glob.glob(pathname + '/*.wav') #find audiobooks

        for image in globjpg:
            for sound in globwav:   
                if(image[:-4] == sound[:-4]):
                    self.imagesWithAudio[image] = sound #Tie the jpg with the wav in a dict if match found.

    def read_Book(self, match):
        print("IMAGE FOUND. IT IS = " + match)

        for book,audio in self.imagesWithAudio.items(): # dictionary used to tie audio with an image and play the corresponding audio with the matched image path.
            if(match == book):
                wave_obj = sa.WaveObject.from_wave_file(audio)
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
                    time.sleep(0.2)  #small buffer so that the while loop isn't checking constantly which can be intensive on the OS.
                    
                play_obj.wait_done()
            else:
                continue


def main():
    testobj = pibook()
    testobj.unpickle_database()
    testobj.populate_dict()
    testobj.book_Lookup()
        
    
if __name__ == "__main__":
    main()
    

