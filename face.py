import cv2
import time
import imutils

camera=cv2.VideoCapture(0)
time.sleep(1)

firstFrame=None
area=500

while True:
    ret,img=camera.read()
    text='Normal'
    img=imutils.resize(img,width=500)
    greyImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussianblur = cv2.GaussianBlur(greyImage, (15, 15), 0)


    if firstFrame is None:
        firstFrame=gaussianblur
        continue


    imgDiff=cv2.absdiff(firstFrame,gaussianblur)
    threshImg=cv2.threshold(imgDiff,25,255,cv2.THRESH_BINARY)[1]
    threshImg=cv2.dilate(threshImg,None,iterations=2)
    counts=cv2.findContours(threshImg.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    counts=imutils.grab_contours(counts)


    for c in counts:
            if cv2.contourArea(c) < area:
                    continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "FACE DETECTED "
    print(text)


    cv2.putText(img, text, (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('CameraFeed',img)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
