import cv2
import numpy as np

class Filter():
    def __init__(self, cap,  lower_hsv = [69, 16, 27], upper_hsv = [163, 78, 100]):        #capture wird im Konstruktor übergeben
        self.cap = cap
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv
        _, self.frame = self.cap.read()
        self.hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.setColor(self.lower_hsv, self.upper_hsv)

    def setColor(self, lower_hsv, upper_hsv):
        self.low_neon_green = np.array(lower_hsv)  # von 360 deg
        self.high_neon_green = np.array(upper_hsv)

    def maskFrame(self):
        neon_green_mask = cv2.inRange(self.hsv_frame, self.low_neon_green, self.high_neon_green)
        neon_green_mask = cv2.erode(neon_green_mask, None, iterations=2)  # maske verfeinern
        neon_green_mask = cv2.dilate(neon_green_mask, None, iterations=2)
        self.neon_masked_frame = cv2.bitwise_and(self.hsv_frame, self.hsv_frame,
                                                 mask=self.neon_green_mask)  # neongrüne Bereiche werden gefiltert
    def prepareFrame(self):
        self.maskFrame()
        med_blur_frame = cv2.medianBlur(self.neon_masked_frame, 15)  # Blur resulting masked Frame
        _, blur_frame_thresh = cv2.threshold(med_blur_frame, 70, 255, cv2.THRESH_BINARY)
        self.blur_frame_thresh = cv2.cvtColor(blur_frame_thresh, cv2.COLOR_BGR2GRAY)

    def extractContours(self):
        self.prepareFrame()
        self.neon_green_edges = cv2.Canny(self.blur_frame_thresh, 100, 200)  # Extract edges (should only be hand)
        _, self.contours, _ = cv2.findContours(self.neon_green_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def getContours(self):
        self.extractContours()
        return self.contours

    def getMask(self):
        self.maskFrame()
        return self.neon_masked_frame