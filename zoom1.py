import cv2

def show_webcam(mirror=False):
    scale= 50
    rate = 5
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('my webcam',cv2.WINDOW_NORMAL)
    cv2.moveWindow('my webcam',0,0)
    cv2.setWindowProperty('my webcam',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    Text = 'Nhap tu ban phim: '
    key = ''
    while True:
        ret_val, image = cam.read()
        if mirror: 
            image = cv2.flip(image, 1)

        #get the webcam size
        height, width, channels = image.shape
        height = height*2
        width = width*2
        image = cv2.resize(image,(width,height))


        #prepare the crop
        centerX,centerY=int(height/2),int(width/2)
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)
        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY
        cropped = image[minY:maxY, minX:maxX]
        resized_cropped = cv2.resize(cropped, (width, height))
        cv2.putText(resized_cropped,Text+key,(50,50),cv2.FONT_HERSHEY_COMPLEX,1.5,(0,0,255),1)
        cv2.imshow('my webcam', resized_cropped)
        if cv2.waitKey(1) == ord('q'):
            break  # esc to qui
        #add + or - 5 % to zoo
        if cv2.waitKey(20) == ord('d') and scale < 50:
            scale += rate  # +
            key = 'd'
        if cv2.waitKey(20) == ord('i') and scale>rate:
            scale -= rate  # + 
            key ='i'
    cv2.destroyAllWindows()
def main():
    show_webcam(mirror=True)

if __name__ == '__main__':
    main()