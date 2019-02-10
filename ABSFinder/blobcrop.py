from SimpleCV import *
import time, os, string, cv2


cam = Camera(1)
disp = Display()
imgSave = cam.getImage() #.drawText("No Image File Taken Yet",50,50,color=Color.BLACK,fontsize=48)



# Start saving the new pictures
while disp.isNotDone():
    img = cam.getImage().crop(200,200,200,200).binarize()
    blobs = img.findBlobs()
    blobs[0].drawMinRect(color=Color.BLUE, width=4)
    img = img.crop(blobs[0])
    disp.writeFrame(img)
    if disp.mouseRight:
		break

# Original directory - originalwd = os.getcwd()

# Change directory - os.chdir("/home/")     disp.mouseX < 640

print os.getcwd()
