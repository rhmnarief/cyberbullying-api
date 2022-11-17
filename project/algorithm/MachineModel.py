import re
import pickle
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
import emoji
from nltk.tokenize import word_tokenize
import unidecode
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

class MachineModel(object):
    def __init__(self):
        try:
            self.ModelML = pickle.load(open("./project/share/model.pkl", "rb"))
            self.dataset = pd.read_csv('./project/share/dataset.csv')
            print('SUCCESS TO INIT MACHINE MODEL')
            self.lemmatizer = WordNetLemmatizer()
            self.stemmer = SnowballStemmer("english")
            print('SUCCESS TO INIT STEMMER LEMATIZER')
            STOPWORDS.update([
                    "rt","mkr","didn","bc","n","m","im","ll","y","ve","u",
                    "ur","don","p","t","s","aren","kp","o","kat","de","re","amp","will",])
            print('SUCCESS TO INIT STOPWORDS')
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                np.array(self.dataset["text_clean"]),
                np.array(self.dataset["sentiment Label"]),
                test_size=0.25,
                random_state=0,
            )
            print('SUCCESS TO SPLIT DATA')
            # TF-IDF
            self.TFIDFVector = TfidfVectorizer(
                use_idf=True, tokenizer=word_tokenize, min_df=0.00002, max_df=0.70
            )
            self.X_train_tf = self.TFIDFVector.fit_transform(self.X_train.astype("U"))
            self.X_test_tf = self.TFIDFVector.transform(self.X_test.astype("U"))
            print('SUCCESS TO VECTORIZER')
        except Exception as ex:
            print('*********')
            print('FAILED TO INIT MODEL & DATASET')
            print(ex)
        
    def clean_text(self, data_string):
        try:
            case_convert = data_string.lower()
            remove_specials = re.sub(r"[^a-zA-Z]", " ", case_convert)
            remove_https = re.sub(r'http\S+', '', remove_specials)
            remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
            remove_accents = unidecode.unidecode(remove_com)
            remove_specials = re.sub(r"[^a-zA-Z]", " ", remove_accents)
            remove_space = re.sub("\s\s+", " ", remove_specials)
            return remove_space
        except Exception as ex:
            print('*********')
            print('FAILED CLEANING DATA')
            print(ex)

    def preprocess_tweet(self, data_string):
        try:
            tweet = re.sub(r"won\'t", "will not", data_string)
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
            tweet = " ".join([self.stemmer.stem(word) for word in tweet.split()])
            tweet = [
                self.lemmatizer.lemmatize(word)
                for word in tweet.split()
                if not word in set(STOPWORDS)
            ]
            tweet = " ".join(tweet)
            return tweet
        except Exception as ex:
            print('*********')
            print('FAILED PREPROCESS DATA')
            print(ex)

    def difine_result(self, data_string):
        try:
            response = ""
            if data_string == 0:
                response = "Not Cyberbullying"
            elif data_string == 1:
                response = "Gender"
            elif data_string == 2:
                response = "Ethnicity"
            elif data_string == 3:
                response = "Religion"
            elif data_string == 4:
                response = "Age"
            else:
                response = "Value is non type of Cyberbullying"
            return response
        except Exception as ex:
            print('*********')
            print('FAILED TO DEFINE RESULT')
            print(ex)

       