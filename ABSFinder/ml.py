# -*- coding: utf-8 -*-
from SimpleCV import *
from SimpleCV.Features import FeatureExtractorBase
import time, os, orange, orngSVM, string, copy

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
	img = cam.getImage().crop(200,200,200,200)
	if n > 4:
		svmclassName = svm.classify(img)
		knnclassName = knn.classify(img)
		treeclassName = tree.classify(img)
		bayesclassName = bayes.classify(img)
		n = 0
	else:
		n +=1
	img=img.scale(400, 400)
	imgraw = copy.deepcopy(img)

	newlayer = DrawingLayer(img.size())

	newlayer.setFontSize(40)
	newlayer.text(svmclassName[6:], (10, 10), color=Color.RED)
	newlayer.text(knnclassName[6:], (10, 60), color=Color.BLUE)
	newlayer.text(treeclassName[6:], (10, 110), color=Color.BLACK)
	newlayer.text(bayesclassName[6:], (10, 160), color=Color.ORANGE)

	img.addDrawingLayer(newlayer)

	#Save additional images if their is four way, stable agreement on the class
	if svmclassName == knnclassName and treeclassName == bayesclassName and treeclassName == knnclassName:
		stable +=1
	else:
		stable=0
	if stable > 50:
		path = os.getcwd() + "/pieces" + svmclassName[6:]
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
		imgraw.save(imgName)
		imgSave = img
		print "Saved as: " + imgName
		print("recorded image of "+svmclassName[6:])
		stable=0
		os.chdir("..")
		os.chdir("..")
	#img.show()
	disp.writeFrame(img.applyLayers())

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
			imgraw.save(imgName)
			print "Saved as: " + imgName
			print("recorded image of "+partname)
			stable=0
			os.chdir("..")
			os.chdir("..")
	if disp.mouseRight:
		break



#print "TREE test ================================================================="
#print tree.test(testPaths,classes,verbose=True)

# Original directory - originalwd = os.getcwd()

# Change directory - os.chdir("/home/")     disp.mouseX < 640

svm.save("SVMClass.xml")
tree.save("TreeClass.xml")
bayes.save("BayesClass.xml")
knn.save("KNNClass.xml")

print os.getcwd()
