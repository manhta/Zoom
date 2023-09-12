import cv2

def nothing(x):
    pass

def show_webcam(mirror=False):
    scale= 50
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('frame')
    cv2.createTrackbar('zoom','frame',1,10,nothing)
    cur_zoom = 1

    while True:
        ret_val, image = cam.read()
        if mirror: 
            image = cv2.flip(image, 1)

        zoom = cv2.getTrackbarPos('zoom','frame')

        if cur_zoom!=zoom:
            if zoom==0: 
                scale = 50
            else:
                scale = int(round(50/zoom))
                cur_zoom=zoom
        
        #get the webcam size
        height, width, channels = image.shape
        height = int(height*1.5)
        width = int(width*1.5)
        #prepare the crop
        centerX,centerY=int(height/2),int(width/2)
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)
        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY
        cropped = image[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height))
        cv2.putText(resized_cropped,str(scale),(50,50),cv2.FONT_HERSHEY_COMPLEX,1.5,(0,0,255),1)

        cv2.imshow('frame', resized_cropped)

        if cv2.waitKey(1) == ord('q'):
            break  # esc to qui
        #add + or - 5 % to zoo
    cv2.destroyAllWindows()
    
def main():
    show_webcam(mirror=True)

if __name__ == '__main__':
    main()