import math
import os


import matplotlib
import numpy as np


matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# import tkinter as tk
import seaborn as sb
import pandas as pd
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import naive_bayes
from sklearn import svm
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import pickle


from os.path import dirname, join
current_dir = dirname(__file__)


class IntentDetection:
    """ Kelas Deteksi Intent """


    ML_NB = 'NAIVE_BAYES'
    ML_SVM = 'SVM'


    __data = None
    __data_test = None
    __data_x = None  # TEXTS
    __data_y = None  # INTENTS


    __train_x = None  # 80%
    __test_x = None  # 20%
    __train_y = None  # 80%
    __test_y = None  # 20%


    __train_y_vect = None  # 80% - label jadi numerik
    __test_y_vect = None  # 20% - label jadi numerik
    __data_y_vect = None  # 100% - label jadi numerik


    __tfidf_vect = None  # data vektor tf-idf
    __train_x_vect = None  # 80% - vektor tf-idf
    __test_x_vect = None  # 20% - vektor tf-idf
    __data_x_vect = None  # 100% - vektor tf-idf


    def __int__(self):
        self.__data = self.__data_test = self.__data_x = self.__data_y = self.__train_x = self.__test_x = self.__train_y = self.__test_y = self.__train_y_vect = self.__test_y_vect = self.__data_y_vect = self.__tfidf_vect = self.__train_x_vect = self.__test_x_vect = self.__data_x_vect = None


    def load_dataset(self, ds_file):
        data = pd.read_csv(ds_file, encoding='latin-1')
        print('\nINFORMASI DATASET')
        print('>>> Lokasi Dataset\t:', os.path.dirname(os.path.abspath(ds_file)))
        print('>>> Nama Dataset\t:', os.path.basename(ds_file))
        print('>>> Jumlah Kolom\t: 2 (KELAS, TEKS)')
        print('>>> Jumlah Baris\t: {} (100%) / {} (80%) / {} (20%)'.format(len(data), math.floor(80 * len(data) / 100),
                                                                           math.ceil(20 * len(
                                                                               data) / 100)))  # lihat floor dan ceil
        self.__data = data


    def __pre_processing(self):
        # print(self.__data_x)
        # print(self.__data_y)
        if (self.__data_x == None) or (self.__data_y == None):
            self.__data['TEKS'] = [t.lower() for t in self.__data['TEKS']]
            self.__data_x = self.__data['TEKS']
            self.__data_y = self.__data['KELAS']
        else:
            print('Fungsi __pre_processing belum dijalankan!')


    def __split_and_encode(self):
        if self.__data_y_vect != []:
            # split dataset
            self.__train_x, self.__test_x, self.__train_y, self.__test_y = model_selection.train_test_split(
                self.__data_x, self.__data_y, test_size=0.2, random_state=25)


            encoder = LabelEncoder()
            self.__train_y_vect = encoder.fit_transform(self.__train_y)
            self.__test_y_vect = encoder.fit_transform(self.__test_y)
            self.__data_y_vect = encoder.fit_transform(self.__data_y)


            # y_asli_encoder = [(self.__data_y[i], self.__data_y_vect[i]) for i in range(0, 50)]
            # sorted(set(y_asli_encoder))
        else:
            print('Fungsi __split_and_selection belum dijalankan!')


    def __vector_space_model(self):
        if self.__data_x_vect != []:
            # buat vektor data untuk train dan test (tf-idf)
            self.__tfidf_vect = TfidfVectorizer(max_features=5000)
            self.__tfidf_vect.fit(self.__data_x)  # vocabulary tf-idf
            self.__train_x_vect = self.__tfidf_vect.transform(self.__train_x)
            self.__test_x_vect = self.__tfidf_vect.transform(self.__test_x)
            self.__data_x_vect = self.__tfidf_vect.transform(self.__data_x)
        else:
            print('Fungsi __vector_space_model belum dijalankan!')


    def __pipeline(self):
        self.__pre_processing()
        self.__split_and_encode()
        self.__vector_space_model()


    # cuma bisa menampilkan informasi skor cross-validation! tidak bisa menyimpan model hasil pelatihan
    def cross_validation(self, model_name):
        match model_name:
            case self.ML_NB:
                model = naive_bayes.MultinomialNB()
                model_label = self.ML_NB
            case self.ML_SVM:
                model = svm.SVC(C=1.0, kernel='rbf')
                model_label = self.ML_SVM


        self.__pipeline()


        print('\nCROSS-VALIDATION')
        print('>>> proses cross-validation sedang berjalan, silakan tunggu...')
        cross_val = cross_val_score(model, self.__data_x_vect, self.__data_y_vect, cv=10)
        print('>>> proses selesai.')


        print('\nINFORMASI HASIL CROSS-VALIDATION')
        print('>>> Nama Machine Learn.\t:', model_label)
        cross_val_format = [float('{:.2f}'.format(n)) for n in cross_val]
        print('>>> 10-Cross-Validation\t:', cross_val_format)
        print('>>> Rata-Rata Akurasi\t:', '{:.2f}'.format(sum(cross_val) / len(cross_val) * 100), '%\n')


    def model_training(self, model_name):
        match model_name:
            case self.ML_NB:
                model = naive_bayes.MultinomialNB()
                model_label = self.ML_NB
            case self.ML_SVM:
                model = svm.SVC(kernel='linear')
                model_label = self.ML_SVM


        self.__pipeline()


        print('\nPELATIHAN MODEL')
        print('>>> Proses pelatihan model "{}" sedang berjalan, silakan tunggu...'.format(model_label))
        model.fit(self.__train_x_vect, self.__train_y_vect)
        y_pred = model.predict(self.__test_x_vect)
        cm = confusion_matrix(self.__test_y_vect, y_pred)
        print('>>> Proses selesai.')


        path_model = join(current_dir, '../../models/model_{}.pkl'.format(model_label))
        file_model = open(path_model, 'wb')
        pickle.dump((model, self.__tfidf_vect), file_model)  # model+vocab (dimensi)


        print('\nINFORMASI PELATIHAN MODEL')
        print('>>> Nama machine learn.\t:', model_label)
        print('>>> Lokasi file model\t:', os.path.abspath(path_model))
        # y_asli_encoder = [(self.__data_y[i], self.__data_y_vect[i]) for i in range(0, 50)]
        y_asli_encoder = [(self.__data_y[i], self.__data_y_vect[i]) for i in range(0, len(self.__data))]
        print('>>> (Kelas, Encoded)\t:', sorted(set(y_asli_encoder)))
        for k, e in sorted(set(y_asli_encoder)):
            print(f'{e}: {k}')


        print('\nINFORMASI HASIL PELATIHAN')
        print(classification_report(self.__test_y_vect, y_pred))


        print('INFORMASI CONFUSION MATRIX')
        print(cm)


        print('Precision: {}'.format(precision_score(self.__test_y_vect, y_pred, average='weighted')))
        print('Recall: {}'.format(recall_score(self.__test_y_vect, y_pred, average='weighted')))
        print('F1-Score: {}'.format(f1_score(self.__test_y_vect, y_pred, average='weighted')))
        print('Accuracy: {}'.format(accuracy_score(self.__test_y_vect, y_pred)))


        # plt.figure(figsize=(10, 8))
        # # were 'cmap' is used to set the accent colour (flare, mako, vlag, YlGnBu, Blues, BuPu, Greens, PiYG,
        # sb.heatmap(cm, annot=True, cmap='mako', fmt='d', cbar=True)
        # plt.xlabel('Predicted Label')
        # plt.ylabel('Truth Label')
        # plt.title('Confusion Matrix - Intent Classification')
        # plt.show()


    def model_testing(self, path_model):
        # load model
        file = open(path_model, 'rb')
        model, vocab = pickle.load(file)
        data_vek = vocab.transform(self.__data_test['TEKS'])


        y_pred = model.predict(data_vek)


        hasil = [(self.__data_test['TEKS'][i], y_pred[i]) for i in range(0, len(y_pred))]
        for i, j in hasil:
            print('{}\t: {}'.format(j, i))


    def prediction(self, teks):
        # load model
        path_model = join(current_dir, '../../models/model_SVM.pkl')
        file = open(path_model, 'rb')
        model, vocab = pickle.load(file)
        d = {'TEKS': [teks]}
        data = pd.DataFrame(data=d)
        data_vek = vocab.transform(data['TEKS'])

        y_pred = model.predict(data_vek)

        hasil = [(data['TEKS'][i], y_pred[i]) for i in range(0, len(y_pred))]
        
        res = y_pred[0]
        return res
        # for i, j in hasil:
        #     print('{}\t: {}'.format(j, i))

# np.random.seed(500)

# train = 0

# if not train:
#     ###### CONTOH TRAINING MODEL
#     ds_file = join(current_dir, "../../data/dataset_intents.csv")
#     # ds_file = '../../data/dataset_intents_mhs.csv'
#     # ds_file = '../../data/dataset_analisis_sentimen_train_val.csv'
#     deteksi_intent = IntentDetection()
#     deteksi_intent.load_dataset(ds_file)


#     # deteksi_intent.cross_validation(deteksi_intent.ML_SVM)
#     deteksi_intent.model_training(deteksi_intent.ML_SVM)
# else:
#     ###### CONTOH TESTING MODEL
#     deteksi_intent = IntentDetection()
#     model_label = deteksi_intent.ML_SVM
#     path_ds = '../../data/dataset_analisis_sentimen_test.csv'
#     path_model = '../../models/model_{}.pkl'.format(model_label)


#     # deteksi_intent.load_dataset_test(path_ds)
#     # deteksi_intent.model_testing(path_model)


#     teks = 'makasih'
#     deteksi_intent.prediction(path_model, teks)