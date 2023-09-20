import cv2 as cv

evt = 0
root = True
MousePnt = []
Start = False 
StartPntArr = []
StartPnt = []
EndPnt = []

def Callback(event,x,y,flag,param):
    global evt,MousePnt,root

    if event == cv.EVENT_LBUTTONDOWN:
        evt = 1
        root = False
        MousePnt = [x,y]
    if event == cv.EVENT_LBUTTONUP:
        evt = 2
        MousePnt = [x,y]
    if event == cv.EVENT_RBUTTONDOWN:
        evt = 3

cv.namedWindow('test',cv.WINDOW_NORMAL)
cv.setWindowProperty('test',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
cv.setMouseCallback('test',Callback)
cam = cv.VideoCapture(0)

rw = 0
rh = 0
roi = []

while True:
    ret,frame = cam.read()

    frame = cv.flip(frame,1)
    h,w = frame.shape[0:2]
    h = h*2
    w = w*2
    frame = cv.resize(frame,(w,h))

    if root:
        cv.imshow('test',frame)
    else:
        if evt==1:
            if len(StartPntArr)>0:
                StartPntArr.clear()
            StartPntArr.append(MousePnt)
            Start = True

        if evt==2:
            if Start == True:
                EndPnt.append(MousePnt)
                StartPnt.append(StartPntArr[0])
                Start = False

            if len(EndPnt)<2:
                rw = EndPnt[0][0] - StartPnt[0][0]
                rh = EndPnt[0][1] - StartPnt[0][1]  
            else:

                X = StartPnt[0][0]
                Y = StartPnt[0][1]

                StartPnt[0][0] = X + int(StartPnt[1][0]*(rw/w))
                StartPnt[0][1] = Y + int(StartPnt[1][1]*(rh/h))
                EndPnt[0][0] = X + int(EndPnt[1][0]*(rw/w))
                EndPnt[0][1] = Y + int(EndPnt[1][1]*(rh/h))

                rw = EndPnt[0][0] - StartPnt[0][0]
                rh = EndPnt[0][1] - StartPnt[0][1]

                StartPnt.pop(1)
                EndPnt.pop(1)

            if StartPnt[0][0]>EndPnt[0][0]: StartPnt[0][0],EndPnt[0][0] = EndPnt[0][0],StartPnt[0][0]
            roi = frame[StartPnt[0][1]:EndPnt[0][1],StartPnt[0][0]:EndPnt[0][0]]
            roi = cv.resize(roi,(w,h))
            cv.imshow('test',roi)

        if evt==3:
            root = True
            rw = 0
            rh = 0
            StartPnt.clear()
            EndPnt.clear()
            Start = False
            roi = []
        

    if cv.waitKey(20)==ord('b'):
        root = True
        rw = 0
        rh = 0
        StartPnt.clear()
        EndPnt.clear()
        Start = False
        roi = []
    if cv.waitKey(20)==ord('q'):
        break

cam.release()
cv.destroyAllWindows()
