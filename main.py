import cv2 as cv

# A: ZOOM
ScaleMax = 2520
StartZoom = False
LeftMouse = False
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
    
    scale = ScaleMax/zoom

    height,width = roi.shape[0:2]
    
    CenterPnt_ROI = [int(width/2),int(height/2)]
    RadiusX,RadiusY = int(width/(2*zoom)),int(height/(2*zoom))
    StartPnt_ROI = [int(CenterPnt_ROI[0]-RadiusX),int(CenterPnt_ROI[1]-RadiusY)]
    EndPnt_ROI = [int(CenterPnt_ROI[0]+RadiusX),int(CenterPnt_ROI[1]+RadiusY)]

    ROI = roi[StartPnt_ROI[1]:EndPnt_ROI[1],StartPnt_ROI[0]:EndPnt_ROI[0]]
    ROI = cv.resize(ROI,(width,height))

    return ROI

# Mouse 
def LeftMouseCallback(event,x,y,flag,param):
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
    if evt == 1:
            StartPntArr.append(MousePnt)
            StartZoom = True
    if evt == 2:
        if StartZoom:  
            EndPnt.append(MousePnt)
            StartPnt.append(StartPntArr[0])
            StartPntArr.clear()
            StartZoom = False
        if len(StartPnt)>0 and len(EndPnt)>0:
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

    roi = cv.resize(roi,(w,h),interpolation=cv.INTER_LANCZOS4)

    return roi

# B: DI CHUYEN
RootPnt = [0,0]
RightMouse = False
Move = False
MoveStartPnt = []
MoveEndPnt = []
cur_zoom = 1

def RightMouseCallback(event,x,y,flag,param):
    global evt
    global MousePnt,RootPnt

    if event == cv.EVENT_RBUTTONDOWN:
        evt = 1
        RootPnt = [x,y]
    if event == cv.EVENT_RBUTTONUP:
        evt = 2
    if event == cv.EVENT_MOUSEMOVE:
        evt = 3
        MousePnt = [x,y]

def MoveROI(roi,frame,new_zoom):
    global evt,cur_zoom,rh,rw
    global RootPnt,MousePnt,MoveStartPnt,MoveEndPnt,StartPnt,EndPnt
    global Move
    h,w = frame.shape[0:2]

    if len(StartPnt)==0:
        if len(MoveStartPnt)==0:
            print(cur_zoom)
            MoveStartPnt = [(int(w/2)-int(w/(2*cur_zoom))),(int(h/2)-int(h/(2*cur_zoom)))]
            MoveEndPnt = [(int(w/2)+int(w/(2*cur_zoom))),(int(h/2)+int(h/(2*cur_zoom)))]
        else:
            if cur_zoom!=new_zoom:
                cur_zoom = new_zoom
                MoveStartPnt = [(int(w/2)-int(w/(2*cur_zoom))),(int(h/2)-int(h/(2*cur_zoom)))]
                MoveEndPnt = [(int(w/2)+int(w/(2*cur_zoom))),(int(h/2)+int(h/(2*cur_zoom)))]
    else:
        CenterPnt = [int((EndPnt[0][0]+StartPnt[0][0])/2),int((EndPnt[0][1]+StartPnt[0][1])/2)]
        if len(MoveEndPnt)==0 and len(MoveStartPnt)==0:
            MoveStartPnt = [CenterPnt[0]-int(((EndPnt[0][0]-StartPnt[0][0])/(2*new_zoom))),CenterPnt[1]-int(((EndPnt[0][1]-StartPnt[0][1])/(2*new_zoom)))]
            MoveEndPnt = [CenterPnt[0]+int(((EndPnt[0][0]-StartPnt[0][0])/(2*new_zoom))),CenterPnt[1]+int(((EndPnt[0][1]-StartPnt[0][1])/(2*new_zoom)))]
        else:
            if cur_zoom!=new_zoom:
                cur_zoom = new_zoom
                MoveStartPnt = [CenterPnt[0]-int(((EndPnt[0][0]-StartPnt[0][0])/(2*new_zoom))),CenterPnt[1]-int(((EndPnt[0][1]-StartPnt[0][1])/(2*new_zoom)))]
                MoveEndPnt = [CenterPnt[0]+int(((EndPnt[0][0]-StartPnt[0][0])/(2*new_zoom))),CenterPnt[1]+int(((EndPnt[0][1]-StartPnt[0][1])/(2*new_zoom)))]

    if evt == 1:
        RootPnt = MousePnt
        Move = True
    if evt == 2:
        Move = False
    if Move:
        if RootPnt!=MousePnt:
            x_dif = MousePnt[0]-RootPnt[0]
            y_dif = MousePnt[1]-RootPnt[1]

            if x_dif<0:
                if (MoveStartPnt[0]+x_dif)>=0:
                    MoveStartPnt[0] = MoveStartPnt[0]+x_dif
                    MoveEndPnt[0] = MoveEndPnt[0]+x_dif
            else:
                if (MoveEndPnt[0]+x_dif)<=w:
                    MoveStartPnt[0] = MoveStartPnt[0]+x_dif
                    MoveEndPnt[0] = MoveEndPnt[0]+x_dif
            if y_dif<0:
                if (MoveStartPnt[1]+y_dif)>=0:
                    MoveStartPnt[1] = MoveStartPnt[1]+y_dif
                    MoveEndPnt[1] = MoveEndPnt[1]+y_dif
            else:
                if (MoveEndPnt[1]+y_dif)<=h:
                    MoveStartPnt[1] = MoveStartPnt[1]+y_dif
                    MoveEndPnt[1] = MoveEndPnt[1]+y_dif

            RootPnt = MousePnt
    if len(StartPnt)>0 and len(EndPnt)>0:
        StartPnt[0] = MoveStartPnt
        EndPnt[0] = MoveEndPnt
        rw = EndPnt[0][0] - StartPnt[0][0]
        rh = EndPnt[0][1] - StartPnt[0][1]
    print(MoveStartPnt,MoveEndPnt)
    if len(MoveStartPnt)>0 and len(MoveEndPnt)>0:
        roi = frame[MoveStartPnt[1]:MoveEndPnt[1],MoveStartPnt[0]:MoveEndPnt[0]]
    roi = cv.resize(roi,(w,h),interpolation=cv.INTER_LANCZOS4)
    return roi

# C: MAIN
def main():
    global evt,rh,rw
    global LeftMouse,RightMouse,Move
    global StartPntArr,StartPnt,EndPnt,roi,MoveStartPnt,MoveEndPnt

    cam = cv.VideoCapture(0)
    cv.namedWindow('zoom')
    # cv.setWindowProperty('zoom',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    cv.createTrackbar('bar1','zoom',1,10,nothing)
    cv.setMouseCallback('zoom',RightMouseCallback)

    while True:
        ret, frame = cam.read()

        h,w = frame.shape[0:2]
        # h=h*2
        # w=w*2
        frame = cv.resize(frame,(w,h),interpolation=cv.INTER_LANCZOS4)
        frame = cv.flip(frame,1)
        roi = frame.copy()

        zoom = cv.getTrackbarPos('bar1','zoom')
        if zoom == 0:
            zoom = 1

        if LeftMouse:
            if len(MoveStartPnt)>0 and len(StartPnt)==0:
                StartPnt.append(MoveStartPnt)
                EndPnt.append(MoveEndPnt)
                rh = EndPnt[0][1]-StartPnt[0][1]
                rw = EndPnt[0][0]-StartPnt[0][0]
                cv.setTrackbarPos('bar1','zoom',1)
            roi = MouseROI(roi,evt)

        if RightMouse:
            roi = MoveROI(roi,frame,zoom)

        if RightMouse==False:
            roi = TrackBarROI(roi,zoom)

        cv.imshow('zoom',roi)

        if cv.waitKey(20) == ord('z'):
            cv.setMouseCallback('zoom',LeftMouseCallback)
            RightMouse = False
            LeftMouse = True
            evt = 0
        if cv.waitKey(20) == ord('r'):
            cv.setMouseCallback('zoom',RightMouseCallback)
            RightMouse = True
            LeftMouse = False
            evt = 0
        if cv.waitKey(20) == ord('s'):
            cv.setMouseCallback('zoom',lambda *args: None)
            LeftMouse = True
            RightMouse = False
        if cv.waitKey(20) == ord('b'):
            cv.setMouseCallback('zoom',lambda *args: None)
            LeftMouse = False
            RightMouse = False
            rw = 0
            rh = 0
            StartZoom = False
            MoveStartPnt.clear()
            MoveEndPnt.clear()
            StartPntArr.clear()
            MousePnt.clear()
            StartPnt.clear()
            EndPnt.clear()
            roi = []

        if cv.waitKey(20) == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()