import json
from pprint import pprint

import requests
from nltk import word_tokenize, pos_tag
from textblob import TextBlob



# engtext=raw_input("Please type your english sentence:")
# print (engtext)
from UrduGenderAnalyzer import UrduGenderAnalyzer

engtext = "Amna is going with Sara"

print("English: " + engtext)

blobObj=TextBlob(engtext)
z=blobObj.translate(from_lang="en", to='ur')
z = z.replace(".", "").replace(",", "")


accessToken = "583e203b-11ed-42bc-893f-ff8459fc6d56"

inputText= str(z)
data = json.dumps({'text': inputText,'token':accessToken})
headers = {'content-type': 'application/json'}
resp = requests.post('https://api.cle.org.pk/v1/pos', data=data, headers=headers)
response = resp.json()


# Kamran's code start
translatedText = response.get('response').get('tagged_text')
tws = UrduGenderAnalyzer.parse_tagged_sentence(translatedText)

gender = UrduGenderAnalyzer.analyze_gender(engtext)

if gender is None:
    exit(1)

isFuture = False
sentenceFinal = ""
for tw in tws:
    if tw.get('p') == "AUXP" or tw.get('p') == "VBF" or (isFuture and tw.get('p') == "AUXT"):
        w = tw.get('w')
        sf = None
        if (w[-1:] == "ی" or w[-1:] == "ے") and gender == "M":
            sf = w[:-1] + w[-1:].replace("ی", "ا")
        elif (w[-1:] == "ا" or w[-1:] == "ے") and gender == "F":
            sf = w[:-1] + w[-1:].replace("ا", "ی")
        if sf is not None:
            tw['w'] = sf
    elif tw.get('p') == "AUXA":
        isFuture = True
    sentenceFinal += " " + tw.get('w')
print(sentenceFinal)

# Kamran's code end


exit(1)

def determine_tense_input(engtext):
   text = word_tokenize(engtext)
   tagged = pos_tag(text)
   tense = {}
   tense["future"] = len([word for word in tagged if word[1] == "MD"])

   tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]])

   tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])

   return (tense)


print(determine_tense_input(engtext))
