import cv2 as cv

evt = 0
root = True
MousePnt = []
StartPnt = []
EndPnt = []

def Callback(event,x,y,flag,param):
    global evt,MousePnt,root

    if event == cv.EVENT_LBUTTONDOWN:
        evt = 1
        root = False
        MousePnt = (x,y)
    if event == cv.EVENT_LBUTTONUP:
        evt = 2
        MousePnt = (x,y)
    if event == cv.EVENT_RBUTTONDOWN:
        evt = 3

cv.namedWindow('test',cv.WINDOW_NORMAL)
cv.setMouseCallback('test',Callback)
cam = cv.VideoCapture(0)

while True:
    ret,frame = cam.read()

    frame = cv.flip(frame,1)
    h,w = frame.shape[0:2]
    
    if root:
        raw = frame.copy()
        cv.imshow('test',raw)
    else:
        if evt==1:
            StartPnt = MousePnt
        if evt == 2:
            EndPnt = MousePnt
            # cv.rectangle(frame,StartPnt,EndPnt,(0,255,0),1)
            roi = frame[StartPnt[1]:EndPnt[1],StartPnt[0]:EndPnt[0]]

            print(StartPnt)
            print(EndPnt)
            roi = cv.resize(roi,(w,h),interpolation=cv.INTER_NEAREST)
            cv.imshow('test',roi)
        if evt == 3:
            root = True

    if cv.waitKey(20)==ord('b'):
        root = True 
    if cv.waitKey(20)==ord('q'):
        break

print(StartPnt)
print(EndPnt)
cam.release()
cv.destroyAllWindows()
