import cv2 as cv
from cv2 import dnn_superres

sr = dnn_superres.DnnSuperResImpl.create()

sr.readModel('EDSR_x4.pb')

sr.setModel('edsr',4)

cam = cv.VideoCapture('but.mp4')


while True: 
    ret,frame = cam.read()
    print(cam.get(cv.CAP_PROP_FPS))
    h,w = frame.shape[0:2]

    res = frame[int(h/4):int((3*h)/4),int(w/4):int((3*w)/4)]
    res = sr.upsample(res)
    print(res)

    cv.imshow('img',res)
    if cv.waitKey(20)==ord('q'):
        break

cam.release()
cv.destroyAllWindows()