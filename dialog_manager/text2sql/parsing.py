from dialog_manager.text2sql.kamus import kamus
import re

class Parsing:
    """
        Kelas ini digunakan untuk mengidentifikasi
        kata-kata pada teks bahasa alami berdasarkan komponen
        penyususn SQL (Structured Query Language).
    """

    def __identify_word(self, text):
        """
            Fungsi ini digunakan untuk mengidentifikasi
            setiap kata pada teks bahasa alami berdasarkan komponen
            penyusun SQL yang telah didefinisikan pada kamus kata.
        """

        word_list = {}
        for keywoard, word in kamus().items():
            for item in word:
                for w in re.findall(r'%s\b' % item, text):
                    if keywoard not in word_list:
                        word_list[keywoard] = []

                    word_list[keywoard].append(w)

        return word_list

    def __parse2sql_component(self, identified_word, entities):
        """
            Fungsi ini digunakan untuk memparsing entitas 
            dan kata-kata yang telah didentifikasi kedalam
            bentuk penyusun SQL, seperti SELECT, FROM, dan WHERE.
        """

        sql_component = []

        # parsing entities
        for entities_name, value in entities.items():
            if value:
                sql_component.append(('WHERE', '{} = "{}"'.format(entities_name, value)))

        # parsing identifued keywoard
        for keywoard, word in identified_word.items():
            if 'perintah' in keywoard:
                sql_component.append(('SELECT', 'SELECT *'))
            elif 'view' in keywoard:
                sql_component.append(('FROM', 'FROM Produk'))
            elif 'tanya_stok' in keywoard:
                sql_component.append(('WHERE', 'STOK > 0'))

        # if there is no 'perintah'
        for item in sql_component:
            if 'perintah' not in item and (('FROM' and 'WHERE') in item[0]):
                sql_component.append(('SELECT', 'SELECT *'))
        

        return sql_component
    
    def parsing(self, entities, text):
        """
            Melakukan parsing.
        """
        result = self.__identify_word(text)
        result = self.__parse2sql_component(result, entities)

        return result