import cv2 as cv

ScaleMax = 2520
StartZoom = False
Mouse = False
evt = 0
MousePnt = []
StartPntArr = []
StartPnt = []
EndPnt = []
rw = 0
rh = 0
roi = []

# Trackbar
def nothing(x):
    pass

def TrackBarROI(roi,zoom):
    global ScaleMax

    if zoom == 0:
        zoom = 1
    
    scale = ScaleMax/zoom

    height,width = roi.shape[0:2]
    # height = height*2
    # width = width*2
    
    CenterPnt_ROI = [int(width/2),int(height/2)]
    RadiusX,RadiusY = int(width/(2*zoom)),int(height/(2*zoom))
    StartPnt_ROI = [int(CenterPnt_ROI[0]-RadiusX),int(CenterPnt_ROI[1]-RadiusY)]
    EndPnt_ROI = [int(CenterPnt_ROI[0]+RadiusX),int(CenterPnt_ROI[1]+RadiusY)]

    ROI = roi[StartPnt_ROI[1]:EndPnt_ROI[1],StartPnt_ROI[0]:EndPnt_ROI[0]]
    ROI = cv.resize(ROI,(width,height))

    return ROI

# Mouse 
def MouseCallback(event,x,y,flag,param):
    global evt,MousePnt
    if event == cv.EVENT_LBUTTONDOWN:
        evt = 1
        MousePnt = [x,y]
    if event == cv.EVENT_LBUTTONUP:
        evt = 2
        MousePnt = [x,y]
    if event == cv.EVENT_MOUSEMOVE:
        MousePnt = [x,y]

def MouseROI(roi,evt):
    global StartZoom
    global rh,rw
    global StartPntArr,StartPnt,EndPnt

    h,w = roi.shape[0:2]
    # h = h*2
    # w = w*2
    
    if evt == 1:
            StartPntArr.append(MousePnt)
            StartZoom = True
    if evt == 2:
        if StartZoom:  
            EndPnt.append(MousePnt)
            StartPnt.append(StartPntArr[0])
            StartPntArr.clear()
            StartZoom = False
        if len(EndPnt) < 2:
            rw = EndPnt[0][0] - StartPnt[0][0]
            rh = EndPnt[0][1] - StartPnt[0][1]  
        else:
            X = StartPnt[0][0]
            Y = StartPnt[0][1]
            StartPnt[0][0] = X + int(StartPnt[1][0]*(rw/w))
            StartPnt[0][1] = Y + int(StartPnt[1][1]*(rh/h))
            EndPnt[0][0] = X + int(EndPnt[1][0]*(rw/w))
            EndPnt[0][1] = Y + int(EndPnt[1][1]*(rh/h))
            
            StartPnt.pop(1)
            EndPnt.pop(1)

    if len(StartPnt)>0 and len(EndPnt)>0:
        if StartPnt[0][0] > EndPnt[0][0]:
            temp = StartPnt[0][0]
            StartPnt[0][0] = EndPnt[0][0]
            EndPnt[0][0] = temp
        if StartPnt[0][1] > EndPnt[0][1]:
            temp = StartPnt[0][1]
            StartPnt[0][1] = EndPnt[0][1]
            EndPnt[0][1] = temp

        roi = roi[StartPnt[0][1]:EndPnt[0][1],StartPnt[0][0]:EndPnt[0][0]]

    roi = cv.resize(roi,(w,h))

    return roi

def main():
    global evt
    global Mouse
    global StartPntArr,StartPnt,EndPnt,roi

    cam = cv.VideoCapture(0)
    cv.namedWindow('zoom')
    # cv.setWindowProperty('zoom',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    cv.createTrackbar('bar1','zoom',1,10,nothing)
    # cv.setMouseCallback('zoom',MouseCallback)

    while True:
        ret, frame = cam.read()

        h,w = frame.shape[0:2]
        # h=h*2
        # w=w*2
        frame = cv.resize(frame,(w,h))
        roi = frame.copy()
        roi = cv.flip(roi,1)

        if Mouse == True:
            roi = MouseROI(roi,evt)

        zoom = cv.getTrackbarPos('bar1','zoom')
        roi = TrackBarROI(roi,zoom)
        cv.imshow('zoom',roi)

        if cv.waitKey(20) == ord('m'):
            cv.setMouseCallback('zoom',MouseCallback)
            Mouse = True
        if cv.waitKey(20) == ord('s'):
            cv.setMouseCallback('zoom',lambda *args : None)
            Mouse = False
        if cv.waitKey(20) == ord('b'):
            cv.setMouseCallback('zoom',lambda *args : None)
            Mouse = False
            StartPnt.clear()
            EndPnt.clear()
            roi = []
        if cv.waitKey(20) == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()