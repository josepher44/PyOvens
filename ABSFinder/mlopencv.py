# -*- coding: utf-8 -*-
from SimpleCV import *
from SimpleCV.Features import FeatureExtractorBase
import time, os, orange, orngSVM, string, copy

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

def saveImg(path, img):
	os.chdir(path)
	pathList = os.listdir(path)
	n = 0
	for string in pathList:
		string = string.lstrip("img").rstrip(".png")
		pathList[n] = int(string)
		n +=1
	n =max(pathList)
	n +=1
	imgName = "img" + str(n) + ".png"
	img.save(imgName)
	print "Saved as: " + imgName
	print("recorded image at " + path+"/"+imgName)
	os.chdir("..")
	os.chdir("..")

originalwd = os.getcwd()
path = os.getcwd() + "/pieces"


hhfe = HueHistogramFeatureExtractor()
#haarfe = HaarLikeFeatureExtractor(fname='C:/Users/Owner/git/pyOvens/ABSFinder/SimpleCV/SimpleCV/Features/haar.txt')
ehfe = EdgeHistogramFeatureExtractor()
myfe = MorphologyFeatureExtractor()
#lfe = LegoFeatureExtractor()
extractors = [hhfe, ehfe, myfe]#, lfe]#	, haarfe]
props ={
'KernelType':'Poly', #default is a RBF Kernel
'SVMType':'C', #default is C
'nu':None, # NU for SVM NU
'c':None, #C for SVM C - the slack variable
'degree':None, #degree for poly kernels - defaults to 3
'coef':None, #coef for Poly/Sigmoid defaults to 0
'gamma':None, #kernel param for poly/rbf/sigma - default is 1/#samples
}
svm = SVMClassifier(extractors,props)
tree = TreeClassifier(extractors)
knn = KNNClassifier(extractors)
bayes = NaiveBayesClassifier(extractors)

trainPaths = []
n = 1
for folder in [x[0] for x in os.walk(path)]:
	if folder != path:
		trainPaths.append(folder)

offset = trainPaths[1].replace("/", " ", trainPaths[1].count("/")-1).find("/")
classes = []
for string in trainPaths:
	classes.append(string[offset-len(string)+1:])

testPaths = []
for string in trainPaths:
	testPaths.append(string.replace("pieces", "test"))

print trainPaths
print testPaths
print classes

print "TRAINING ================================================================="
print svm.train(trainPaths,classes,verbose=True)
print tree.train(trainPaths,classes,verbose=True)
print knn.train(trainPaths,classes,verbose=True)
print bayes.train(trainPaths,classes,verbose=True)

print "LOADING"
#svm = SVMClassifier.load('SVMClass.xml')
#tree = TreeClassifier.load('TreeClass.xml')
#bayes = NaiveBayesClassifier.load('BayesClass.xml')
#knn = KNNClassifier.load('KNNClass.xml')

#print "SVM test ================================================================="
#print svm.test(testPaths,classes,verbose=True)

cam = Camera(1)
disp = Display()
n = 0
stable = 0
svmclassName = "Waiting...."
knnclassName = "Waiting...."
treeclassName = "Waiting...."
bayesclassName = "Waiting...."
path = ""

while disp.isNotDone():
	#Crop out the border from the image
	imgdisp = cam.getImage().crop(200,200,200,200)
	cv2img = normalizedimage(imgdisp.getNumpyCv2())
	img = Image(cv2img.transpose(1, 0, 2)[:, :, ::-1])

	#Run the classifier every 4th loop, for speed purposes
	if n > 4:
		svmclassName = svm.classify(img)
		knnclassName = knn.classify(img)
		treeclassName = tree.classify(img)
		bayesclassName = bayes.classify(img)
		n = 0
	else:
		n +=1

	"""
	Scale the image for display. Make a copy for processing purposes, then
	proceed to perform additional image manipulation on the base image
	"""
	imgdisp=img.scale(400, 400)
	imgraw = copy.deepcopy(imgdisp)

	#Create a layer containing readouts of each classificatoin
	newlayer = DrawingLayer(imgdisp.size())
	newlayer.setFontSize(40)
	newlayer.text(svmclassName[6:], (10, 10), color=Color.RED)
	newlayer.text(knnclassName[6:], (10, 60), color=Color.BLUE)
	newlayer.text(treeclassName[6:], (10, 110), color=Color.BLACK)
	newlayer.text(bayesclassName[6:], (10, 160), color=Color.ORANGE)
	imgdisp.addDrawingLayer(newlayer)

	#Save additional images if their is four way, stable agreement on the class
	if (svmclassName == knnclassName and treeclassName == bayesclassName and
			treeclassName == knnclassName):
		stable +=1
	else:
		stable=0
	if stable > 50:
		saveImg(os.getcwd() + "/pieces" + svmclassName[6:], imgraw)
		stable=0

	#Refresh the display
	disp.writeFrame(imgdisp.applyLayers())

	#Save an image corresponding to the labeled classification the user clicks
	partname=""
	if disp.mouseLeft:
		if disp.leftButtonDownPosition():
			if disp.leftButtonDownPosition()[1]<60:
				print("SVN Region")
				path = os.getcwd() + "/pieces" + svmclassName[6:]
				partname = svmclassName[6:]
			elif disp.leftButtonDownPosition()[1] < 110:
				print("KNN Region")
				path = os.getcwd() + "/pieces" + knnclassName[6:]
				partname = knnclassName[6:]
			elif disp.leftButtonDownPosition()[1] < 160:
				print("Tree Region")
				path = os.getcwd() + "/pieces" + treeclassName[6:]
				partname = treeclassName[6:]
			elif disp.leftButtonDownPosition()[1] < 210:
				print("Bayes region")
				path = os.getcwd() + "/pieces" + bayesclassName[6:]
				partname = bayesclassName[6:]

			saveImg(path, imgraw)
			stable=0

	#End program on right click
	if disp.mouseRight:
		break

#Save trained model data (doesn't work right)
svm.save("SVMClass.dat")
tree.save("TreeClass.dat")
bayes.save("BayesClass.dat")
knn.save("KNNClass.dat")

print os.getcwd()
