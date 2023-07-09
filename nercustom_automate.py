import spacy
import re
import pandas as pd
import os
from spacy.training import Example
from spacy.lang.en import English

import json
import cleantext
import random

'''
this file contains the code for generating annoted training
data for custom NER model

throughout the process we will use python's spacy library

for stringprocessing python's cleantext library is used

this code focuses on annoing data for Multiple  entity name
'''

class AutoCreatearr:

    def __init__(self,file):

        self.df = pd.read_csv(file)

    def get_files(self,dir):

        try:
            return sorted([files for files in os.listdir(dir)])
        except Exception as e:
            return e
    
    def processfeature(self,feature):
        
        try:
            self.df[feature] = [word.lower() for word in self.df[feature]]
            return sorted(self.df[feature].unique().tolist())
        except Exception as e:
            return e
    
    def get_values(self,dir,feature):

        try:
            return list(zip(self.get_files(dir) , self.processfeature(feature)))
        except Exception as e:
            return e
        

# creating a user defined class for loading and saving the data
# for creating and loading tge data json files are used
class GetData:
    
    # function for loading the file
    def load_data(self, file):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    # user defined function for saving the file
    def save_data(self, file, data):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

# creating a user defined class StringOperations
# this class holds all the functions required for string processing
class StringOperations:
    def __init__(self):

        # defining list of prefixes
        self.titles = [
            "Dr",
            "Professor",
            "Mr",
            "Mrs",
            "Ms",
            "Miss",
            "Aunt",
            "Uncle",
            "Mr and Mrs",
            "Student",
        ]
    # user defined function to convert string to uppercase
    def convertuppar(self, str_lst):
        try:
            return [word.upper() for word in str_lst]
        except Exception as e:
            return e
    # user defined function to convert string to lowercase
    def convertlower(self, str_lst):
        try:
            return [word.lower() for word in str_lst]
        except Exception as e:
            return e
    # user defined function to join ths strings
    def getjoinstr(self, str_lst):
        try:
            return [
                ("".join(words.split()), "".join(words.capitalize().split()))
                for words in str_lst
            ]
        except Exception as e:
            return e
    # user defined function to split the string
    def splitwords(self, str_lst):
        try:
            datalst = [word.split() for word in str_lst]
            return [
                (text, text.capitalize(), text.upper())
                for word in datalst
                for text in word
            ]
        except Exception as e:
            return e
    # user defined function to convert first letter as capital
    def fistalphaupper(self, str_lst):
        try:
            return [word.capitalize() for word in str_lst]
        except Exception as e:
            return e
    # user defined function to add prefixes
    def addprefixes(self, str_lst):
        try:
            final_characters = list()
            for character in str_lst:
                if "" != character:
                    final_characters.append(character)
                    for title in self.titles:
                        titled_char = f"{title} {character}"
                        final_characters.append(titled_char)
            return final_characters
        except Exception as e:
            return e

# user defiened class for text cleaning
# text cleaning and processing is done using python regulkar expression
# and cleantext library
# calling methods of class String Operations a final corpus is generated

class Generate:
    def __init__(self, file):
        self.load = GetData()
        self.data = self.load.load_data(file)
        self.df = pd.DataFrame(self.data, columns=["text"])

    def generate_better_characters(self):
        return [
            re.sub("[^a-zA-Z]", " ", message.lower())
            for message in self.df["text".lower()]
        ]

    def removewords(self):
        return [
            cleantext.clean(word, stemming=False, stopwords=True)
            for word in self.generate_better_characters()
        ]


class GenerateData(Generate):
    def __init__(self, file):
        self.g = Generate(file)
        self.operations = StringOperations()
        self.data_chr = self.g.removewords()

    def alluppar(self):
        try:
            return self.operations.convertuppar(str_lst=self.data_chr)
        except Exception as e:
            return e
    def allower(self):
        try:
            return self.operations.convertlower(str_lst=self.data_chr)
        except Exception as e:
            return e
    def getjoin(self):
        try:
            return [
                word
                for text in self.operations.getjoinstr(str_lst=self.data_chr)
                for word in text
            ]
        except Exception as e:
            return e

    def getsplit(self):
        try:
            return [
                word
                for text in self.operations.splitwords(str_lst=self.data_chr)
                for word in text
            ]
        except Exception as e:
            return e

    def getfirstupper(self):
        try:
            return self.operations.fistalphaupper(str_lst=self.data_chr)
        except Exception as e:
            return e

    def prefixes(self):
        try:
            return sorted(self.operations.addprefixes(str_lst=self.data_chr))
        except Exception as e:
            return e

    def singlewordprefixes(self):
        try:
            return sorted(set(self.operations.addprefixes(str_lst=self.getsplit())))
        except Exception as e:
            return e

    def finalgenerateddata(self,prefix,split_words):
        try:
            if (prefix == 'apply' or prefix is True) or (split_words == 'apply' or split_words is True):
                return set(sorted(
                    self.data_chr
                    + self.alluppar()
                    + self.allower()
                    + self.getjoin()
                    + self.getsplit()
                    + self.getfirstupper()
                    + self.prefixes()
                    + self.singlewordprefixes()
                ))
            else:
                return set(sorted(
                    self.data_chr
                    + self.alluppar()
                    + self.allower()
                    + self.getjoin()
                    + self.getfirstupper()
                ))
        except Exception as e:
            return e

# user defined class for generating data patterns for our model
# use this technique when you have to train for Multiple Entity
# # value, we will first load all the data realated to each entity
# in an array then map the data to the following entity name
# the entire process can be automated an the model can have 
# multiple Entity patterns

class GeneratePatterns:

    def __init__(self):
        
        
        self.savefile = GetData()
        
        self.patterns = []
        
    # user defined function for generating training corpus
    def create_training_data(self, pair,add_prefix,split_str):
        
        try:
            for data in pair:      # list of files
                self.gd = GenerateData(data[0])  # fetching nfile name
                self.final_list = sorted(self.gd.finalgenerateddata(add_prefix,split_str))
                for item in self.final_list:
                    pattern = {"label": data[1], "pattern": item}  # fetching entity name
                    self.patterns.append(pattern)
            return self.patterns
        except Exception as e:
            return e

    def savedata(self, file_name,pair,add_prefix,split_str):
        try:
            datapatterns = self.create_training_data(pair,add_prefix,split_str)
            self.savefile.save_data(file=file_name, data=datapatterns)
        except Exception as e:
            return e


# user defined class for generating patterns rules
# using spacy's English library
# the final data corpus generated will be passed as patterns for our model

class GenerateRules:

    def __init__(self, data_pair,generatefilejson,prefix,split_words):

       
        self.pat = GeneratePatterns()
        self.pattern_data = self.pat.create_training_data(data_pair,prefix,split_words)
        self.pat.savedata(generatefilejson, data_pair,prefix,split_words)
        self.nlp = English()
        self.results = []
        

    def traindata(self):
        try:
            return self.pattern_data
        except Exception as e:
            return e
        
    # user defined function to create pipe
    # the final training corpus is passed to the model
    # as patterns to learn

    def get_ent_ruler(self):

        try:
            ruler = self.nlp.add_pipe('entity_ruler')
            ruler.add_patterns(self.pattern_data)
            return ruler
        except Exception as e:
            return e
    # user defined function to save the model to disk
    def generate_model(self, model_name):

        try:
            self.get_ent_ruler()
            self.nlp.to_disk(model_name)
        except Exception as e:
            return e

# user defined class for generating annoted training data
# the model we saved earlier will be used on our training corpus
# the result will be [(the text) , (start_pos,end_pos {pattern})]
class GenerateTrainingData:

    def __init__(self,model):

        # loading the model
        self.nlp = spacy.load(model)
        
        #self.traindata = list()
    
    # user defined function for loading the file    
    def load_data(self,file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            return e
       
    # user defined function for saving the data as json file
    def save_data(self,file, data):
        try:
            with open (file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            return e
        
    # testing the model on a dummy data
    # it is better to test our model on some pseudo real data
    # before creating training corpus

    def test_model(self,text):

        try:
            doc = self.nlp(text)
            entities = list()
            for ent in doc.ents:
                entities.append((ent.start_char, ent.end_char, ent.label_))
            if len(entities) > 0:
                self.results = [text, {"entities": entities}]
                return self.results
        except Exception as e:
            return e
    
    # user defined function to create the 
    # final training corpus this generated
    # set of data will be used to train our
    # custom NER model
    def trainingcorpus(self,file):

        data_lst = list()
       
        try:
            with open(file,'r+',encoding='utf-8') as text_file:
                data_str = text_file.read()
                data_arr = data_str.split("\n\n")
                for data in data_arr:
                    data = data.lower()
                    data_text = data.replace("\n","").strip()
                    data_lst.append(data_text)

            return [self.test_model(text=word) for word in data_lst if self.test_model(text=word) != None]
        except Exception as e:
            return e
# user denined class for creating a custom NER model
# model's performance and accuracy depends upon the 
# amount of data we provide
class ModelTraining:

    def __init__(self,pipe_name):
        
        # we will use spacy's blank module
        # for creating our own custom model
        self.nlp = spacy.blank('en')
        self.nlp.add_pipe(pipe_name) 

    # user defined function to train the model
    def trainmodel(self,data,iterations):

        try:

            other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
            with self.nlp.disable_pipes(*other_pipes): 
                optimizer = self.nlp.begin_training()
                for itn in range(iterations):
                    print("Statring iteration " + str(itn))
                    random.shuffle(data)
                    losses = {}
                    for text, annotations in data:
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        self.nlp.update(
                              [example], 
                              drop=0.2,  
                              sgd=optimizer,  
                              losses=losses)
                    print(losses)
            return self.nlp
        except Exception as e:
            return e


if __name__ == "__main__":
    generate = GenerateRules(
        jsonfile="E:\CustomNER\hp_characters.json",
        type="PERSON",
        generatefilejson="generate.json",prefix='apply'
    )
    generate.generate_model(model_name='hp_ner2')
    
        
    




