from SimpleCV import *
from SimpleCV.Features import FeatureExtractorBase
import time, os, orange, orngSVM, string

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

print "SVM ================================================================="
print svm.train(trainPaths,classes,verbose=True)


#print "TREE ================================================================="
print tree.train(trainPaths,classes,verbose=True)

print knn.train(trainPaths,classes,verbose=True)

print bayes.train(trainPaths,classes,verbose=True)

#print "SVM test ================================================================="
#print svm.test(testPaths,classes,verbose=True)

cam = Camera(1)
disp = Display()
n = 0
svmclassName = "Waiting...."
knnclassName = "Waiting...."
treeclassName = "Waiting...."
bayesclassName = "Waiting...."

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
	img.drawText(svmclassName[6:], 10, 10, fontsize=40, color=Color.RED)
	img.drawText(knnclassName[6:], 10, 60, fontsize=40, color=Color.BLUE)
	img.drawText(treeclassName[6:], 10, 110, fontsize=40, color=Color.BLACK)
	img.drawText(bayesclassName[6:], 10, 160, fontsize=40, color=Color.ORANGE)
	img.show()
	if disp.mouseRight:
		break



#print "TREE test ================================================================="
#print tree.test(testPaths,classes,verbose=True)

# Original directory - originalwd = os.getcwd()

# Change directory - os.chdir("/home/")     disp.mouseX < 640

svm.save("SVMClass")

print os.getcwd()
