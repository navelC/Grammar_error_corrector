import re
def decontracted(phrase):

    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"gon na", " going to", phrase)
    phrase = re.sub(r"wan na", " want to", phrase)
    phrase = re.sub(r"gonna", " going to", phrase)
    phrase = re.sub(r"wanna", " want to", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub("\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
        
    return phrase

def clean_text(t):

  #print(t)

  # t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii') #No need to normalize as text is already an  with utf-8 character set
  t = decontracted(t)

  t = re.sub(r'x D', '', t)
  t = re.sub(r': D', '', t)
  t = re.sub(r': P', '', t)

  t = re.sub(r'xD', '', t)
  t = re.sub(r':D', '', t)
  t = re.sub(r':P', '', t)

  #If brackets in text, remove text within brackets
  if '(' in t and ')' in t:
    try:
      t = re.sub(t.split("(")[-1].split(")")[0], '', t)
    except:
      pass
    #t = re.sub("(", '', t)
    #t = re.sub(")", '', t)
  
  #Replace all characters except these with space
  t = re.sub(r'[^A-Za-z;!?.,\-\' ]+', ' ', t)

  #If semicolon in text, remove the part after semicolon till fullstop (since we don't know if the text after semicolon is a continuation of the sentence or a new context altogether)
  #if ';' in t:
  #  t = re.sub(';', ' , ', t)

  t = re.sub(r'\.+',r' .',t)
  t = re.sub(r'!+',r' !',t )
  t = re.sub(r'\?+',r' ?',t )
  t = re.sub(r'\-+',r' - ',t )
  t = re.sub(r'\,+',r' , ',t )
  t = re.sub(r'\'+',r" ' ",t)
  t = re.sub(' +', ' ', t)

  return t
with open('entries.train') as f:
  data = f.readlines()
print(len(data))
file = open('cleaned_text.txt', 'w')
count = 0.00
for i,x in enumerate(data):
  words = x.split("\t")
  if len(words) < 4:
    continue
  if i/len(data) > 0.01:
    if i/len(data) > count:
      count = count + 0.01
      print(i/len(data))
  word = words[4]
  file.write('%s\n' % clean_text(word))
file.close()