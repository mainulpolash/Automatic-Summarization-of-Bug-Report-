from __future__ import absolute_import
from __future__ import print_function
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.data
import six
__author__ = 'a_medelyan'

import rake
import operator
import io

# EXAMPLE ONE - SIMPLE
stoppath = "data/stoplists/SmartStoplist.txt"

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 5, 3, 4)

for keyword in range(1,2):
	#read the input file
	sample_file = io.open("x/sentence"+str(keyword)+".in", 'r',encoding="iso-8859-1")
	text = sample_file.read()
	text=text.lower()

	#tokenize the sentences 
	text_tokenize = sent_tokenize(text)
	text_main = text_tokenize
	#find the keyword from the text
	#print (text) 
	keywords = rake_object.run(text)  
	# print (keywords)
	#print (text_tokenize)
	sentence_score = [0.0]*(len(text_tokenize)+100)

	for i in range(0,len(keywords)):
		phrase = keywords[i][0]
		score = keywords [i][1]
		line_no=0
		j=0
		for line in text_tokenize:
			line=str(line)
			if line.count(phrase)>0:

				pp=line.count(phrase)

				sentence_score[j]=sentence_score[j]+(score*pp)
				# text1[j]=text1[j].replace(phrase,' ')
				#print (str(pp))

				#print (phrase)
				
				# print (line)

			j+=1	
			line_no+=1
		text=text.replace(phrase,' ')	

	ranked_sentence=[] 
		
	for i in range(0,len(text_tokenize)):
		if sentence_score[i]>0:
			# print (i,sentence_score[i])
			#f.write(str(i)+" "+str(sentence_score[i])+" "+str(text_main[i])+"\n")
			ranked_sentence.append([sentence_score[i],text_main[i]])
	#f.close()

	ranked_sentence=sorted(ranked_sentence, key=lambda x:(x[0]),reverse=True)

	for i in range(0, int (len(ranked_sentence) /2)):
		print (ranked_sentence[i])
		print ("\n")
		#sortedsentences = sorted(six.iteritems(sentence_score), key=operator.itemgetter(1), reverse=True)	
		#text=text.replace(phrase,' ')
		#print (line)
		#print (str(sentence_score[j]))
	# f=open(str(i)+"_score.in","a")
	# for i in range(0,len(text1)):
	# 	if sentence_score[i]>0:
	# 		# print (i,sentence_score[i])
	# 		f.write(str(i)+" "+str(sentence_score[i])+" "+str(text_main[i])+"\n")
	# 		ranked_sentence.append([i,sentence_score[i],text_main[i]])
	# f.close()	

