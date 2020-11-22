import json
import logging
import nltk
import operator
import pickle
import re

from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 



def cookies_theorem(cat : dict, len_to_keep):
    keep_list = sorted(cat.items(), key=lambda v : v[1], reverse=True)
    keep_list = keep_list[:len_to_keep]

    max_score, min_score = keep_list[0][1], keep_list[-1][1]

    new_cats = {}
    for k, v in keep_list:
        new_cats[k] = (v-min_score+1)/(max_score+1)
    return new_cats

def getWordsFromFile(categoryName):
    words = {}
    file_doc = open("./categories/{}.json".format(categoryName)) 
    data = json.load(file_doc)

    for entry in data:
        words[entry["word"]] = entry["score"]
    
    file_doc.close()
    return words

global_dict = {}

def loadDictionaries():
    LEN_TO_KEEP = 3000
    global_dict["sports"] = cookies_theorem(getWordsFromFile("sports"), LEN_TO_KEEP)
    global_dict["politics"] = cookies_theorem(getWordsFromFile("politics"), LEN_TO_KEEP)
    global_dict["videogames"] = cookies_theorem(getWordsFromFile("videogames"), LEN_TO_KEEP)
    global_dict["social"] = cookies_theorem(getWordsFromFile("social"), LEN_TO_KEEP)
    global_dict["cars"] = cookies_theorem(getWordsFromFile("cars"), LEN_TO_KEEP)
    global_dict["nature"] = cookies_theorem(getWordsFromFile("nature"),LEN_TO_KEEP)
    global_dict["science"] = cookies_theorem(getWordsFromFile("science"),LEN_TO_KEEP)
    global_dict["food"] = cookies_theorem(getWordsFromFile("food"),LEN_TO_KEEP)
    global_dict["health"] = cookies_theorem(getWordsFromFile("health"),LEN_TO_KEEP)
    global_dict["music"] = cookies_theorem(getWordsFromFile("music"),LEN_TO_KEEP)

def getCategory(tweet):
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(tweet) 
    filtered_sentence = [w for w in word_tokens if w not in stop_words] 
    
    #print("TOKENS:", word_tokens) 

    stemmer = WordNetLemmatizer()
    documents = []
    tweet_arr = filtered_sentence
    for sen in range(0, len(tweet_arr)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(tweet_arr[sen]))
        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)
        # Converting to Lowercase
        document = document.lower()
        # Lemmatization
        document = document.split()
        document = [stemmer.lemmatize(word) for word in document]
        document = [word for word in document if '@' not in word]
        document = [word for word in document if "://" not in word]
        document = [word for word in document if "RT" not in word]
        document = ' '.join(document)
        documents.append(document)

    tweet_arr = documents
    
    scores = {
        "videogames": 0,
        "cars": 0,
        "music": 0,
        "food": 0,
        "health": 0,
        "nature": 0,
        "politics": 0,
        "science": 0,
        "social": 0,
        "sports": 0
    }

    for word in tweet_arr:
        scores['videogames'] += global_dict['videogames'][word] if word in global_dict['videogames'] else 0
        scores['cars'] += global_dict['cars'][word] if word in global_dict['cars'] else 0
        scores['food'] += global_dict['food'][word] if word in global_dict['food'] else 0
        scores['health'] += global_dict['health'][word] if word in global_dict['health'] else 0
        scores['music'] += global_dict['music'][word] if word in global_dict['music'] else 0
        scores['nature'] += global_dict['nature'][word] if word in global_dict['nature'] else 0
        scores['politics'] += global_dict['politics'][word] if word in global_dict['politics'] else 0
        scores['science'] += global_dict['science'][word] if word in global_dict['science'] else 0
        scores['social'] += global_dict['social'][word] if word in global_dict['social'] else 0
        scores['sports'] += global_dict['sports'][word] if word in global_dict['sports'] else 0


    for k, v in scores.items():
        scores[k] = v/len(tweet_arr)


    max_category = max(scores, key=scores.get)
    if scores[max_category] < 0.07:
        return ("None", 0.0)
    else:
        return (max_category, scores[max_category])
    
