'''
Author: Kamran Akram <kamranakram1000@live.com>
Date: 12/11/18
'''
import json
import spacy


class UrduGenderAnalyzer:

    @staticmethod
    def parse_tagged_sentence(s):
        tws = []
        isP = True
        isW = False
        p = w = ""
        for c in s:
            if c is '|':
                isP = not isP
                isW = not isW
            elif c is " ":
                isW = not isW
                isP = not isP
                tw = {'p': p,'w': w}
                tws.append(tw)
                p = w = ""
            else:
                if isP:
                    p += c
                elif isW:
                    w += c
        return tws

    @staticmethod
    def analyze_gender(s):
        spc = spacy.load('en_core_web_sm')
        doc = spc(s)
        sub = None
        for token in doc:
            if token.dep_ == "nsubj":
                sub = token.lower_
                break
        if sub is None:
            print("Unable to find subject in sentence.")
            return None
        with open('names-dataset.json', encoding='utf-8') as f:
            d = json.load(f)
            g = None
            for ns in d:
                if sub == ns.get('name').lower():
                    g = ns.get('gender')
                    return g
            print("Subject is not in dataset.")
        return None




