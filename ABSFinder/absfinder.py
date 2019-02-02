#! python27
import SimpleCV

cam=SimpleCV.Camera(1)
while True:
    img = cam.getImage()
    img.show()
