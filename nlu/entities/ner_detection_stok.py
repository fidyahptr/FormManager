import re
import itertools
from nlu.entities.produk_info import list_merk, original_tipe
from fuzzywuzzy import fuzz
# from produk_info import list_merk, permutation_types, original_tipe


class NER:
    """
        Ini ada kelas NER atau Named Entity Recognition.
        Kelas ini digunakan untuk untuk mengenali
        entitas merk dan entitas tipe pada laptop.
    """
    entities = {
        'merk' : [],
        'tipe' : []
    }

    def entity_recognition(self, text):
        """
            Fungsi ini digunakan untuk mengenali
            entitas merk dan entitas tipe
            pada text bahasa alami.
        """            

        # deteksi entitas merk
        for merk in list_merk():
            sim_ratio = fuzz.partial_ratio(merk, text)
            if sim_ratio >= 80:
                self.entities['merk'] = merk

        # deteksi entitas tipe
        numerator = 0
        most_similiar_tipe = []
        for type in original_tipe():
            intersection = list(set(type.split()) & set(text.split()))

            if intersection:

                if len(intersection) > numerator:
                    numerator = len(intersection)
                    most_similiar_tipe = [type]

                elif len(intersection) == numerator:
                    most_similiar_tipe.append(type)

            else:
                sim_ratio = fuzz.WRatio(type, text)

                if sim_ratio >= 80:
                    most_similiar_tipe.append(type)


        for tipe in most_similiar_tipe:
            self.entities['tipe'].append(tipe)


        # deteksi entitas tipe
        # for tipe in original_tipe():
        #     sim_ratio = fuzz.WRatio(tipe, text)


        #     if sim_ratio >= 90:
        #         self.entities['tipe'] = tipe


        return self.entities

    def add_entities_slot(self, text):
        """
            Fungsi ini digunakan untuk mengecek
            apakah entitas merk dan entitas tipe terisi.
            Jika belum terisi maka tanya ulang dan tambahkan.
        """

        for tipe in original_tipe():
            sim_ratio = fuzz.WRatio(tipe, text)


            if sim_ratio >= 90:
                self.entities['tipe'] = tipe


        # return self.entities
        # pattern_tipe = re.compile('|'.join(permutation_types()), re.IGNORECASE)
        # find_tipe = re.findall(pattern_tipe, text)


        # list_tipe = []
        # for item in find_tipe:
        #     types = item.split()
        #     pers = set(itertools.permutations(types))
        #     for per in pers:
        #         list_tipe.append(' '.join(per))  
 
        # for item in list(set(list_tipe).intersection(original_tipe())):
        #     self.entities['tipe'] = item  


    def get_entities(self):
        """
            Fungsi ini dibuat agar fungsi lain dapat menggunakan
            entitas merk dan entitas tipe.
        """
        return self.entities


    def reset_entities(self):
        """
            Fungsi ini digunakan untuk mereset nilai dari entitas
            merk dan entitas tipe.
        """
        self.entities['merk'] = None
        self.entities['tipe'] = None

    def reset_entities_tipe(self):
        self.entities['tipe'] = None