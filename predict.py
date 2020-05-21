import re
import joblib
import tkinter as tk
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt


jl = joblib.load('logreg_binary')  # Logistic regression for binary classification (propaganda/non-propaganda)
jl_multiClass = joblib.load('multiclass_logreg')  # Logistic regression for multi Class  (14 classes)


class Prediction:

    def __init__(self, text, jl, jl_multi_class):
        self.text = text
        self.jl = jl
        self.jl_multi_class = jl_multi_class

    def predict_sentence(self):
        propaganda_list = []
        raw_text = self.text.replace("\n", "")
        vector = re.split("[?.!]", raw_text)
        for sentence in vector:
            response = self.jl.predict([sentence])
            if response == "propaganda":
                propaganda_list.append(sentence)
        return propaganda_list

    def predict_technique(self):
        propaganda_dictionary = {}
        list_of_propaganda = self.predict_fragment()
        for sentence in list_of_propaganda:
            label = self.jl_multi_class.predict([sentence])
            if label[0] in propaganda_dictionary:
                propaganda_dictionary[label[0]].append(sentence)
            else:
                propaganda_dictionary[label[0]] = [sentence]
        return propaganda_dictionary

    def predict_fragment(self):
        list_of_spans = []
        longest_sequence = []
        list_of_propaganda = self.predict_sentence()
        for sentence in list_of_propaganda:
            listOfFragments = []
            sentenceList = sentence.split()
            if len(sentenceList) <= 3:
                longest_sequence.append(sentence)
            else:
                for n in range(2, len(sentenceList) - 1):
                    grams = [sentenceList[i:i + n] for i in range(len(sentenceList) - n + 1)]
                    for gram in grams:
                        candidate = " ".join(gram)
                        response = self.jl.predict([candidate])
                        if response == "propaganda":
                            listOfFragments.append(candidate)

                list_of_spans.append(listOfFragments)

        for fragments in list_of_spans:
            longest_sequence.append(max(fragments, key=len))

        return longest_sequence

    def percent_of_propaganda(self):
        a_new_list = []
        dictionary = self.predict_technique()
        for key in dictionary:
            for value in dictionary[key]:
                for fragments in value:
                    a_new_list.append(fragments)
        x = "".join(a_new_list)
        totalNumberOfWords = len(self.text)
        numberOfPropagandaWords = len(x)
        percentOfPropaganda = numberOfPropagandaWords * 100 / totalNumberOfWords
        response = f"\nPercent of Propaganda = {str(percentOfPropaganda)[:5]}%\n\n"
        return response

    def clean_text(self):
        replaceBySpace = re.compile("[/(){}\[\]|@,;]")
        badSymbols = re.compile("[^0-9a-z #+_]")
        cleaned_text = replaceBySpace.sub(' ', self.text)
        post = badSymbols.sub('', cleaned_text)
        return post




class CustomText(tk.Text):

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit",
                                count=count, regexp=regexp)
            if index == "":
                break
            if count.get() == 0:
                break  # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def tags(self):
        self.tag_config("Slogans", background="lawn green")
        self.tag_config("Loaded_Language", background="yellow")
        self.tag_config("Name_Calling,Labeling", background="red")
        self.tag_config("Repetition", background="orange")
        self.tag_config("Exaggeration,Minimisation", background="lawn green")
        self.tag_config("Doubt", background="LightPink1")
        self.tag_config("Appeal_to_fear-prejudice", background="IndianRed1")
        self.tag_config("Flag-Waving", background="light goldenrod")
        self.tag_config("Causal_Oversimplification", background="sky blue")
        self.tag_config("Appeal_to_Authority", background="aquamarine2")
        self.tag_config("Thought-terminating_Cliches", background="brown1")
        self.tag_config("Black-and-White_Fallacy", background="plum2")
        self.tag_config("Whataboutism,Straw_Men,Red_Herring", background="burlywood1")
        self.tag_config("Bandwagon,Reductio_ad_hitlerum", background="cyan3")
