import nltk
import nltk.data
import requests
import xml.etree.ElementTree as ET
import io
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.data

import rake
import operator
import io

# EXAMPLE ONE - SIMPLE
stoppath = "data/stoplists/SmartStoplist.txt"

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 5, 3, 4)
tree = ET.parse('bugreports.xml')
tree1 = ET.parse ('annotation.xml')
root = tree.getroot()
root1 = tree1.getroot()

# print str(root.findall())
i=0
k=0
bug_no=0
avg=0
avg_sentence_ref = 0
recall = 0
precision = 0
b = 0 
for bug, bug1 in zip(root.findall('BugReport'), root1.findall('BugReport')):

	text=""
	text1=""
	text_with_id=[]
	ID=bug.get('ID')
	id1 = []
	id2 = []
	title = bug.find('Title').text
	title1 = bug1.find('Title').text
	count=0
	# desc = bug.find('description').text
	# title=title.replace('\n',' ')
	# desc=desc.replace('\n',' ')
	# j=1
	# com=""
	b = b+1 
	p = 1
	for annotation in bug1.findall('Annotation'): 


		for extractivesummary in annotation.findall('ExtractiveSummary'):
			if (p==1):
				for sentence1 in extractivesummary.findall('Sentence'):

					sentence_id_1 = sentence1.get('ID')
					text1 = text1+str(sentence_id_1)+str("\n")
					sentence_id_1 =sentence_id_1.replace(' ','')
					id1.append(str(sentence_id_1))
					count = count +1 
				p = p+1

				#text1 = text1+str(sentence_id_1)+str('\n')
				#print (text1)



	for turn in bug.findall('Turn'):
		# print "yes"
		for txt in turn.findall('Text'):

			for sentence in txt.findall('Sentence'):
				# print "YYYY"
				sentence_id=sentence.get('ID')
				sentence_text=sentence.text
				# text.append([])
				text= text+str(sentence_text)
				text_with_id.append([str(sentence_id),str(sentence_text)])
				id2.append(sentence_id)
				# print sentence_text
				# print sentence_id
				# # print len(str(text))
				# if len(str(text))<=10:
				# 	continue
				# text=text.replace('\n',' ')
				# com=com+str(text)+"\n\n"

				# j+=1
	#text_tokenize = sent_tokenize(text)
	# f=io. open("x/sentence"+str(ID)+".in","w")
	# f.write(str(text))
	# f.close()
	#print (text1)
	keywords = rake_object.run(text)

	sentence_score = [0.0]*(len(text_with_id)+100)

	for j in range (0, len(text_with_id)):
		line=str(text_with_id[j][1])
	
		for i in range(0,len(keywords)):
			phrase = keywords[i][0]
			score = keywords [i][1]
			pp=line.count(phrase)
			if (len(phrase)==3):
				sentence_score[j]=sentence_score[j]+(score*pp*3)
				line.replace(phrase,'')
			if (len(phrase)==2):
				sentence_score[j]=sentence_score[j]+(score*pp*2)
				line.replace(phrase,'')	
			else:
				sentence_score[j]=sentence_score[j]+(score*pp*1)
				line.replace(phrase,'')	

		text_with_id[j].append(sentence_score[j])

	# print (str(text_with_id))
	ranked_sentence=sorted(text_with_id, key=lambda x:(x[2]),reverse=True)
	print (ranked_sentence)
	break
	f = io.open("x/reference"+str(ID)+".in","w")
	f.write(text1)
	f.close

	text2 = ""
	for i in range (0,len(id1)):
		text2 = text2 + str (ranked_sentence[i][0]) + str ('\n')


	f = io.open("x/generated"+str(ID)+".in","w")
	f.write(text2)
	f.close	

	# print (id1)
	# print (ranked_sentence[0])
	#print (len(id1))
	true_positive = 0
	false_negative = 0
	false_positive = 0
	
	
	for i in range(0,len(id1)):
		
		#for j in range(0,min(25,len(ranked_sentence))):
		for j in range(0,min(25,len(ranked_sentence))):
			# print (ranked_sentence)
			# print (len(id1))
			# print (len(ranked_sentence[j]))
			if str(id1[i])==str(ranked_sentence[j][0]):
				# print ('yes')
				true_positive+=1
	false_positive = min(25,len(ranked_sentence)) - true_positive
	false_negative = len(id1) - true_positive
	recall = recall + true_positive / (true_positive + false_negative)
	precision = precision + true_positive / (true_positive + false_positive)
	#print (recall)		
	avg+=((1.0)*count)/len(id1)
	avg_sentence_ref+=len(id1)
	# print (avg*100)

		
	# if bug_no>1:
	# 	break

	# bug_no+=1

	# print("\n\n")


avg=avg*100
avg=avg/36
#print (avg)
avg_sentence_ref=avg_sentence_ref/36
recall = recall/36
print ("Evaluation Result for Annotation 1")
print ("Recall:")
print (recall)
precision = precision / 36
print ("precision:")
print (precision)
print ("F1 score:")
f1 = 2 * ((precision * recall)/(precision + recall))
print (f1)
#print (b)
#print (avg_sentence_ref)



	

	# if j<8:
	# 	continue
	
	# loc="data/test/"
	# if bug_no<2000:
	# 	loc="data/train/"
	
# f=open(loc+"title/title"+str(bug_no)+".in","w")
# f.write(str(title))
# f.close()

# f=open(loc+"description/description"+str(bug_no)+".in","w")
# f.write(str(desc))
# f.close()

#f=open(loc+"sentence/sentence"+str(bug_no)+".in","w")

# print (bug_no," ",j)
# bug_no+=1S