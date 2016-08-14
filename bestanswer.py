#determinig the best answer
"""
parameter: average sentence length
		average word length
		words in the dictniory
"""
dict=['hello','hi','how','computer','sir','useful','know','fuck','compute','giant','answer','efficiently','piece']

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize,sent_tokenize
def max(a,b):
	if a>b :
		return a
	else:	
		return b
	

def avg_sent_lenght(a):
	toks=[]
	toks=sent_tokenize(a)
	sentLen = 0
	for sens in toks:
		sentLen += len(sens.split())

	if len(toks):
		s_l= sentLen/float(len(toks))
	else:
		return 0
	if s_l:
		return 100/float(s_l)
	else:
		return s_l
	
def avg_word_len(a):
        toks=[]
        toks=word_tokenize(a)
	w_l= len(a)/float(len(a.split()))
	if w_l:
		return 100/float(w_l)
	else:
		return w_l
	
	
def familier(a,dic):
	toks=[]
	toks=word_tokenize(a)
	count=0
	for tok in toks:
		for word in dic :
			if tok==word:
				count+=1
	fam= count/float(len(dic))
	return 100*float(fam)

def get_score(content):
	wa1= avg_sent_lenght(content)        
	wa1+= avg_word_len(content)
	wa1+= familier(content,dict)
	return wa1
