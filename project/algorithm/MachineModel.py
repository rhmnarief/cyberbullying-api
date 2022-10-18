import re
import pickle
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
import emoji
from nltk.tokenize import word_tokenize
import unidecode
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os

try:
    cwd_loct = os.getcwd()
    print('my location', cwd_loct)
except Exception as ex:
    print(cwd_loct)
    print('*********')
    print('Failed to read dataset')
    print(ex)

try:
    model = pickle.load(open("./project/share/model.pkl", "rb"))
    print('SUCCESS TO LOAD MODEL')
except Exception as ex:
    print('*********')
    print('FAILED TO READ MODEL')
    print(ex)

try:
    dataset = pd.read_csv('./project/share/dataset.csv')
    print('SUCCES TO LOAD DATASET')
except Exception as ex:
    print('*********')
    print('FAILED TO READ DATASET')
    print(ex)


try:
    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer("english")
    STOPWORDS.update(
        [
            "rt",
            "mkr",
            "didn",
            "bc",
            "n",
            "m",
            "im",
            "ll",
            "y",
            "ve",
            "u",
            "ur",
            "don",
            "p",
            "t",
            "s",
            "aren",
            "kp",
            "o",
            "kat",
            "de",
            "re",
            "amp",
            "will",
        ]
    )

    def clean_text(data_string):
        case_convert = data_string.lower()
        remove_specials = re.sub(r"[^a-zA-Z]", " ", case_convert)
        remove_https = re.sub(r'http\S+', '', remove_specials)
        remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
        remove_accents = unidecode.unidecode(remove_com)
        remove_specials = re.sub(r"[^a-zA-Z]", " ", remove_accents)
        remove_space = re.sub("\s\s+", " ", remove_specials)
        return remove_space

    def preprocess_tweet(tweet):
        tweet = re.sub(r"won\'t", "will not", tweet)
        tweet = re.sub(r"can\'t", "can not", tweet)
        tweet = re.sub(r"n\'t", " not", tweet)
        tweet = re.sub(r"\'re", " are", tweet)
        tweet = re.sub(r"\'s", " is", tweet)
        tweet = re.sub(r"\'d", " would", tweet)
        tweet = re.sub(r"\'ll", " will", tweet)
        tweet = re.sub(r"\'t", " not", tweet)
        tweet = re.sub(r"\'ve", " have", tweet)
        tweet = re.sub(r"\'m", " am", tweet)
        tweet = re.sub("[^a-zA-Z]", " ", tweet)
        tweet = re.sub(emoji.get_emoji_regexp(), "", tweet)
        tweet = re.sub(r"[^\x00-\x7f]", "", tweet)
        tweet = " ".join([stemmer.stem(word) for word in tweet.split()])
        tweet = [
            lemmatizer.lemmatize(word)
            for word in tweet.split()
            if not word in set(STOPWORDS)
        ]
        tweet = " ".join(tweet)
        return tweet

except Exception as ex:
    print('*********')
    print('Failed to build text cleaning and preprocess text')
    print(ex)


try:
    X_train, X_test, y_train, y_test = train_test_split(
        np.array(dataset["text_clean"]),
        np.array(dataset["sentiment Label"]),
        test_size=0.25,
        random_state=0,
    )
    (unique, counts) = np.unique(y_train, return_counts=True)
    np.asarray((unique, counts)).T
    # TF-IDF
    TFIDFVector = TfidfVectorizer(
        use_idf=True, tokenizer=word_tokenize, min_df=0.00002, max_df=0.70
    )
    X_train_tf = TFIDFVector.fit_transform(X_train.astype("U"))
    X_test_tf = TFIDFVector.transform(X_test.astype("U"))
except Exception as ex:
    print('*********')
    print('Failed to build define split data into tfidf vectorizer')
    print(ex)


try:
    def difine_result(value):
        response = ""
        if value == 0:
            response = "Not Cyberbullying"
        elif value == 1:
            response = "Gender"
        elif value == 2:
            response = "Ethnicity"
        elif value == 3:
            response = "Religion"
        elif value == 4:
            response = "Age"
        else:
            response = "Value is non type of Cyberbullying"
        return response
except Exception as ex:
    print('*********')
    print('Failed to build define result function')
    print(ex)
