from collections import deque
import cv2
"""
HandRecognizer Class
Provides functions to extract hand contours, as well as positional data
from provided contour.
"""
class HandRecognizer():
    """
    Constructor
    :param buffersize
    Constructor initializes deque of size buffersize to track positional data for evaluation of
    hand movement. Initially, deque is filled with zeroes only
    """
    def __init__(self, buffersize = 20):
        self.radius = 0
        self.center = 0,0
        self.max_area = 0
        self.pts = deque(maxlen = buffersize)
        for x in range(buffersize):
            self.pts.appendleft((0,0))

    """
    _extractHand
    Can only be called by functions that provide contours.
    Extracts largest contour (assumed to be hand due to filtering) as well as moments
    and derived "center" of contour, and finds minimum enclosing circle and associated radius
    """
    def _extractHand(self, contours):
        # only starts if provided contours are nonempty
        if contours:
            # finds largest contour in provided contours
            cnt = max(contours, key=cv2.contourArea)
            # finds minimum enclosing circle's radius
            (_, self.radius) = cv2.minEnclosingCircle(cnt)
            # finds optical center of contour by usage of its moments
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if self.radius > 10:
                    # adds current center to deque for tracking
                    self.pts.appendleft(self.center)
                    cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.main_contour = cnt

    """
    getMainContour
    Provides Largest found contour
    """
    def getMainContour(self, contours):
        self._extractHand(contours)
        return self.main_contour

    """
    getCenterXYRadius
    provides X/Y-Coordinates and Radius of calculated "Center" of contour
    """
    def getCenterXYRadius(self, contours):
        self._extractHand(contours)
        return self.center[0], self.center[1], self.radius

    """
    getPts
    provides positional data of hand in deque
    """
    def getPts(self, contours):
        self._extractHand(contours)
        return self.pts