from SimpleCV import *
from SimpleCV.Features import FeatureExtractorBase
import time, os, orange, orngSVM, string

originalwd = os.getcwd()
path = os.getcwd() + "/pieces"


hhfe = HueHistogramFeatureExtractor()
#haarfe = HaarLikeFeatureExtractor()
ehfe = EdgeHistogramFeatureExtractor()
#lfe = LegoFeatureExtractor()
extractors = [hhfe, ehfe]#, lfe]#	, haarfe]
props ={
'KernelType':'Poly', #default is a RBF Kernel
'SVMType':'C', #default is C
'nu':None, # NU for SVM NU
'c':None, #C for SVM C - the slack variable
'degree':None, #degree for poly kernels - defaults to 3
'coef':None, #coef for Poly/Sigmoid defaults to 0
'gamma':None, #kernel param for poly/rbf/sigma - default is 1/#samples
}
svm = SVMClassifier(extractors,props).load("SVMClass.xml")
tree = TreeClassifier(extractors)

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

print "SVM ================================================================="
#print svm.train(trainPaths,classes,verbose=True)


#print "TREE ================================================================="
#print tree.train(trainPaths,classes,verbose=True)

#print "SVM test ================================================================="
#print svm.test(testPaths,classes,verbose=True)

cam = Camera()
disp = Display()
n = 0
className = "Waiting...."

while disp.isNotDone():
	img = cam.getImage()
	if n > 4:
		className = svm.classify(img)
		n = 0
	else:
		n +=1
	img.drawText(className, 10, 10, fontsize=60, color=Color.RED)
	img.show()
	if disp.mouseRight:
		break



#print "TREE test ================================================================="
#print tree.test(testPaths,classes,verbose=True)

# Original directory - originalwd = os.getcwd()

# Change directory - os.chdir("/home/")     disp.mouseX < 640

svm.save("SVMClass")

print os.getcwd()
