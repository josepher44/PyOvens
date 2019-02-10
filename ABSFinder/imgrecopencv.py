from SimpleCV import *
import time, os, string, cv2

def normalizedimage(inputimage):
	blurred = cv2.pyrMeanShiftFiltering(inputimage,31,61)
	grayscaled = cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)

	thresh = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 5)

	edges = cv2.Canny(thresh,100,200)

	kernel = np.ones((5,5), np.uint8)
	img_dilation = cv2.dilate(edges, kernel, iterations=1)
	#img_dilation2 = cv2.dilate(edges, kernel, iterations=1)

	contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	print(len(contours))

	try:
		cnt=contours[0]
		rect = cv2.minAreaRect(cnt)
		box = cv2.cv.BoxPoints(rect)
		box = np.int0(box)
		#cv2.drawContours(img,[box],0,(0,0,255),2)
		#cv.drawContours(thresh, contours, -1(0,0,255),6)

		center, size, theta = rect
		center, size = tuple(map(int, center)), tuple(map(int, size))
		M = cv2.getRotationMatrix2D( center, theta, 1)
		dst = cv2.warpAffine(inputimage, M, inputimage.shape[:2])
		out = cv2.getRectSubPix(dst, size, center)

		return out
	except:
		return inputimage


originalwd = os.getcwd()

delay = 0.1
print "-> What is the name of the new piece?"
piece = raw_input()
chosen = False
path = os.getcwd() + "/pieces/" + piece

# Get name of new piece and check to see if already exists
exists = False
overwrite = False
if os.access(path, os.F_OK):
	exists = True
	print "-> This piece has already been added. Would you like to overwrite all old pictures? (Y/n)"
	while True:
		user = raw_input()
		if user == "Y":
			print "-> Old pictures will be OVERWRITTEN (deleted)"
			overwrite = True
			break
		elif user == "n":
			print "-> Old pictures will be kept"
			break
		else:
			print "-> INVALID ANSWER -- Please type Y or n (case sensetive)"

# Create new directory if required - Clear old directory if overwriting
if exists == False:
	os.makedirs(path)

os.chdir(path)

print "-> The directory of your new piece is: " + path
time.sleep(1)

print "-> Let's start taking the pictures"
time.sleep(delay)
print "-> Use the left mouse button to take an image"
time.sleep(delay)
print "-> Use the right mouse button to retake the image"
time.sleep(delay)
print "-> Press enter in the terminal when you are finished taking images. A minimum of 10 images is recommeded"
time.sleep(delay)
print "-> Press enter to continue"
null = raw_input()

# Delete old pictures if overwriting
if overwrite:
	for eachfile in os.listdir(path):
		eachfilepath = os.path.join(path, eachfile)
		os.unlink(eachfilepath)
	n = 0
elif overwrite == False and exists:
	pathList = os.listdir(path)
	n = 0
	for string in pathList:
		string = string.lstrip("img").rstrip(".png")
		pathList[n] = int(string)
		n +=1
	n =max(pathList)
else:
	n = 0

cam = Camera(1)
disp = Display()
imgSave = cam.getImage() #.drawText("No Image File Taken Yet",50,50,color=Color.BLACK,fontsize=48)



# Start saving the new pictures
while disp.isNotDone():
	rawimg = cam.getImage().crop(200,200,200,200)
	cv2img = normalizedimage(rawimg.getNumpyCv2())
	img = Image(cv2img.transpose(1, 0, 2)[:, :, ::-1])
	if disp.mouseLeft and disp.leftButtonDownPosition()[0] < 239:
		n +=1
		imgName = "img" + str(n) + ".png"
		img.save(imgName)
		imgSave = img
		print "Saved as: " + imgName
	if disp.mouseLeft and disp.leftButtonDownPosition()[0] > 239:
		imgName = "img" + str(n) + ".png"
		img.save(imgName)
		imgSave = img
		print "RE-Saved as: " + imgName
	if disp.mouseRight:
		break
	img.save(disp)
	rawimg.show()

# Original directory - originalwd = os.getcwd()

# Change directory - os.chdir("/home/")     disp.mouseX < 640

print os.getcwd()
