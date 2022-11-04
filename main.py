import cv2
import numpy as np

global camwidth, camheight, upperline, centerline, bottomline, linecolor, ret, frame
global lowerrange, upperrange, threshold

lowerrange = 0
upperrange = 0

def nothing(x):
    pass

'''
cv2.namedWindow('Settings')
cv2.createTrackbar('Upper Line', 'Settings', 0, int(0.5*camwidth), nothing)
cv2.setTrackbarPos('Upper Line', 'Settings', int(0.3*camwidth))
cv2.createTrackbar('Bottom Line', 'Settings', 0, int(0.5*camwidth), nothing)
cv2.setTrackbarPos('Bottom Line', 'Settings', int(0.4*camwidth))
cv2.createTrackbar('Center Line', 'Settings', 0, camheight, nothing)
cv2.setTrackbarPos('Center Line', 'Settings', int(0.5*camheight))
cv2.createTrackbar('Threshold', 'Settings', 0, 255, nothing)
cv2.setTrackbarPos('Threshold', 'Settings', 30)
'''

threshold = 30 #cv2.getTrackbarPos('Threshold', 'Settings')

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("Camera is not detected.")
    exit()

camwidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
camheight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

def mousecallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        color = frame[y, x]
        pixelbgr = np.uint8([[color]])
        pixelhsv = cv2.cvtColor(pixelbgr, cv2.COLOR_BGR2HSV)
        pixelhsv = pixelhsv[0][0]
        #print(color)
        #print(pixelbgr)
        print(pixelhsv)
    if pixelhsv[0] < 10:
        lowerrange = np.array([pixelhsv[0]-10+180, threshold, threshold])
        upperrange = np.array([pixelhsv[0]+10, 255, 255])
    elif pixelhsv[0] > 170:
        lowerrange = np.array([pixelhsv[0]-10, threshold, threshold])
        upperrange = np.array([pixelhsv[0]+10-180, 255, 255])
    else:
        lowerrange = np.array([pixelhsv[0]-10, threshold, threshold])
        upperrange = np.array([pixelhsv[0]+10, 255, 255])
    

cv2.namedWindow('Jump King But It\'s Real Jump')
cv2.setMouseCallback('Jump King But It\'s Real Jump', mousecallback)

while True:
    ret, frame = capture.read()
    upperline = int(0.3*camwidth) #cv2.getTrackbarPos('Upper Line', 'Settings')
    centerline = int(0.5*camheight) #cv2.getTrackbarPos('Center Line', 'Settings')
    bottomline = int(0.4*camwidth) #cv2.getTrackbarPos('Bottom Line', 'Settings')
    frame = cv2.flip(frame, 1)
    cv2.line(frame, (upperline, 0), (upperline, centerline), (0, 0, 255), 1)
    cv2.line(frame, (camwidth-upperline, 0), (camwidth-upperline, centerline), (0, 0, 255), 1)
    cv2.line(frame, (0, centerline), (camwidth, centerline), (0, 0, 255), 1)
    cv2.line(frame, (bottomline, camheight), (bottomline, centerline), (0, 0, 255), 1)
    cv2.line(frame, (camwidth-bottomline, camheight), (camwidth-bottomline, centerline), (0, 0, 255), 1)

    camhsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(camhsv, lowerrange, upperrange)
    result = cv2.bitwise_and(frame, frame, mask=mask)


    cv2.imshow('Jump King But It\'s Real Jump', frame)
    cv2.imshow('result', result)

    if cv2.waitKey(1) & 0xFF == 27:
        break


capture.release()
cv2.destroyAllWindows()