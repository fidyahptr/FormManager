import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

class SVM:
    """ Kelas untuk metode machine/deep learning """

    def __int__(self):
        pass

    def load_dataset(self):
        # df = pd.read_csv('C:\\Users\\andre\Downloads\chatbot\data\dataset_intents_new.csv', index_col=False)
        # df = pd.read_csv('..\..\data\dataset_intents.csv', index_col=False)
        print(df)

        train_x, test_x, train_y, test_y = model_selection.train_test_split(df['TEXTS'], df['INTENTS'], test_size=0.2)

        Encoder = LabelEncoder()
        train_y = Encoder.fit_transform(train_y)
        test_y = Encoder.fit_transform(test_y)

        print(train_y)
        print(test_y)

        tfidf_vect = TfidfVectorizer(max_features=5000)
        # tfidf_vect.fit(df['TEKS'])
        tfidf_vect.fit(df['TEXTS'])
        train_x_tfidf = tfidf_vect.transform(train_x)
        test_x_tfidf = tfidf_vect.transform(test_x)
        print(tfidf_vect.vocabulary_)
        print(train_x_tfidf)

        # fit the training dataset on the NB classifier
        Naive = naive_bayes.MultinomialNB()
        Naive.fit(train_x_tfidf, train_y)
        # predict the labels on validation dataset
        predictions_NB = Naive.predict(test_x_tfidf)
        # Use accuracy_score function to get the accuracy
        print("Naive Bayes Accuracy Score -> ", accuracy_score(predictions_NB, test_y) * 100)

        # Classifier - Algorithm - SVM
        # fit the training dataset on the classifier
        SVM = SVC(kernel='linear', C=1, degree=3, gamma='auto')

        SVM.fit(train_x_tfidf, train_y)
        # predict the labels on validation dataset
        predictions_SVM = SVM.predict(test_x_tfidf)
        # Use accuracy_score function to get the accuracy
        print("SVM Accuracy Score -> ", accuracy_score(predictions_SVM, test_y) * 100)


    def run(self):
        self.load_dataset()


class ModelTraining:
    """ Kelas untuk training model """

    def __int__(self):
        pass


class ModelTesting:
    """ Kelas untuk testing model """

    def __int__(self):
        pass


class IntentDetection:
    """Kelas untuk deteksi intent"""

    def __int__(self):
        pass

    def deteksi(self, teks):
        print(teks)

###=========================TEST

svm = SVM()
svm.run()
