#Source for AWS:PyLenin, https://www.youtube.com/watch?v=_cQEuLGv45o
#source for nltk: Dhilip Subramanian, https://towardsdatascience.com/synonyms-and-antonyms-in-python-a865a5e14ce8
import csv       #import csv module
import boto3      # import AWS module to use rekognition funcionallity
import nltk
import inflect # from: https://stackoverflow.com/questions/18902608/generating-the-plural-form-of-a-noun

nltk.download('wordnet') 
from nltk.corpus import wordnet as wn

with open('credentials.csv', 'r') as input:   #iterate over the csv containing our API
	next(input)  #skip first row, move onto next
	objRead = csv.reader(input) #read the csv file
	for i in objRead:    #find the access key
		accKeyID = i[2] # the 3rd item in the file is the access Key ID
		secAccKey = i[3] #the 4th item in the file is the secret access key

#Below is the demo list: ask judges for random images to download to show
#demolist=[]

# below is the images that we tested
UserInput = ['orange2.JPG','demo.JPG','box.JPG','popcan.png','aluminium.JPG','battery.JPG','cardboard.JPG','chair.JPG','fruit.JPG','laptop.JPG','meat.JPG','milkjug.JPG','orangepeel.JPG','paper.JPG','pen.JPG','soupcan.JPG','tire.JPG'] #Load the image to be tested

itemList = []
#create a client , pass in secret access key and access key id
for pic in UserInput:
	client = boto3.client('rekognition',region_name = 'us-west-2',aws_access_key_id = accKeyID,aws_secret_access_key = secAccKey) 
#convert image into base-64 bytes
	with open(pic, 'rb') as original:
		originalBytes = original.read()  # the bytes are what will be passed into the rekognition detect labels method
		
	estimate = client.detect_labels(Image={'Bytes': originalBytes},MaxLabels = 10)	#get the image
	itemList.append(estimate['Labels'][0]['Name'].upper())
#print(itemList)

def wordSplitList(word):
	word = str(word)
	word2=''
	for i in range(8,len(word)):
		if word[i] != '.':
			word2+=word[i]
		if word[i]=='.':
			return word2
def itemCheck(item):
	oragnicList=['Fruit','Peel','Plant','Food','Vegtable','Apple','Burger','Flower','Leaf', 'Meat','Meal','Lunch','Breakfast','Supper','Dinner','Carrot','Pea','Lettuce','Water','Pork','Beef']
	for i in range(len(oragnicList)):
		oragnicList[i] = oragnicList[i].upper()
		oragnicList.append(oragnicList[i].upper()+'S')
	synOrgList = []
	for i in oragnicList:
		synonym = wn.synsets(i)
		synOrgList.append(synonym)
	for i in synOrgList:
		for j in i:
			oragnicList.append(wordSplitList(j).upper())
			oragnicList.append(wordSplitList(j).upper()+'S')
			engine = inflect.engine()
			plural = engine.plural(wordSplitList(j).upper())
			oragnicList.append(plural)
	#print(oragnicList)

	recyclingList =['Milk','Soda','Can','Tin','Paper','Steel','Cardboard','Box','Soup','Spoupcan','Plastic','Wrap','Foil','Drink','Beverage','Glass','Bottle']
	for i in range(len(recyclingList)):
		recyclingList[i] = recyclingList[i].upper()
		recyclingList.append(recyclingList[i].upper()+'S')
	synRecList = []
	for i in recyclingList:
		synonym = wn.synsets(i)
		synRecList.append(synonym)
	for i in synRecList:
		for j in i:
			recyclingList.append(wordSplitList(j).upper())
			recyclingList.append(wordSplitList(j).upper()+'S')
			engine = inflect.engine()
			plural = engine.plural(wordSplitList(j).upper())
			recyclingList.append(plural)
	#print(recyclingList)

	garbageOrElectronics = ['Pen','Chair','Pc','Fuse','TV','Microwave','Garbage','Battery','Tire','Trash','Computer']
	for i in range(len(garbageOrElectronics)):
		garbageOrElectronics[i] = garbageOrElectronics[i].upper()
		garbageOrElectronics.append(garbageOrElectronics[i].upper()+'S')
	synGarbList = []
	for i in garbageOrElectronics:
		synonym = wn.synsets(i)
		synGarbList.append(synonym)
	for i in synGarbList:
		for j in i:
			garbageOrElectronics.append(wordSplitList(j).upper())
			garbageOrElectronics.append(wordSplitList(j).upper()+'S')
			engine = inflect.engine()
			plural = engine.plural(wordSplitList(j).upper())
			garbageOrElectronics.append(plural)	
	#print(garbageOrElectronics)

	if item in oragnicList:
		print('This is a '+ item + ', please place it in your organics bin or compost.')
		return 0
	if item in recyclingList:
		print('This is a '+ item + ', please return for a recycle.')
		return 0
	if item in garbageOrElectronics:
		print('This is a '+ item + ', please place all garbage in your gaerbage bin, or take to your local landfill. Please return your unwanted electronics to the nearest pickup location.')
		return 0
	else:
		print(item + ' Unknown category, please consult with your local jusristictions webpage.')
		return 0

def wordSplit(word):
	word = str(word)
	word2=''
	for i in range(8,len(word)):
		if word[i] != '.':
			word2+=word[i]
		if word[i]=='.':
			return word2

synonymList = []
for item in itemList:
	synonym = wn.synsets(item)
	itemCheck(item)
	for i in synonym:
		str(i)
		synonymList.append(wordSplit(i).upper())
#print(synonymList)
#print(len(synonymList))