import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
i = 1

while(True):
    print i
    i += 1
    ret, frame1 = cap.read()  
    #gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    #ret, frame2 = cap.read()
    #gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    #frame = cv2.absdiff(gray1,gray2)
    cv2.imshow('frame',frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
for i in range (1,5):
    cv2.waitKey(1)
