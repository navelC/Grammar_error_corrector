import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import random
import re

def add_error(text, remove_det = False, nn= False, vform= False, spelling_adj= False):
    text_ = text.split(' ')  #list of words
    words = nltk.word_tokenize(text)
    pos_tag = nltk.pos_tag(words)
    #Add error in spelling of the adjective (angry -> anrgy)
    if spelling_adj == True :
      for i, (word, tag) in enumerate(pos_tag):
        if tag in ['JJ', 'JJR', 'JJS']:
          letters = [l for l in word]
          ran = random.randint(0,2)
          if ran == 0:
          	text_[i] = text_[i] + "ly"
          elif len(letters) > 2:
            exch = letters[int(len(word)/2)]
            letters[int(len(word)/2)] = letters[int(len(word)/2)+1]
            letters[int(len(word)/2)+1] = exch 
            text_[i] = "".join(letters)
          else:
            continue
    #Replace a plural noun with singular version (countries -> country)
    if nn == True:
      for i, (word, tag) in enumerate(pos_tag):
        if tag == 'NNS':
          text_[i] = lemmatizer.lemmatize(word, pos ="n")
        elif tag == 'NN':
          ran = random.randint(0,2)
          if ran == 0:
          	text_[i] = text_[i] + 's'
          else: 
          	text_[i] = text_[i] + 'es'

    if vform == True:
      for i, (word, tag) in enumerate(pos_tag):
        if tag in ['VBP', 'VBZ', "VBN", 'VBD']:  
          text_[i] = lemmatizer.lemmatize(word, pos ="v")

    #Remove an article or determiner (an apple -> apple)
    if remove_det == True:
      for i, (word, tag) in enumerate(pos_tag):
        if tag == 'DT':
          text_.remove(word)
          break    

    return " ".join(text_)


with open('cleaned_text.txt') as f:
  data = f.readlines()

# word = data[54827]
# pos_tag = nltk.pos_tag([word])
# add_error(word, remove_det = True)

file = open('incorrect.txt', 'w')
count = 0.00
for i,x in enumerate(data):
	x = re.sub(r'\n', '', x)
	try:
		ran = random.randint(0, 4)
		if i/len(data) > 0.01:
			if i/len(data) > count:
				count = count + 0.01
				print(i/len(data))
		if ran == 0:
			file.write('%s\n' % add_error(x, remove_det = True))
		elif ran == 2:
			file.write('%s\n' % add_error(x, nn = True))
		elif ran == 1:
			file.write('%s\n' % add_error(x, vform = True))
		else:
			file.write('%s\n' % add_error(x, spelling_adj = True))
	except Exception as e:
		print(i)
		raise e
		break
file.close()
