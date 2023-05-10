from system.NER import NER
from system.parsing import Parsing
from system.translating import Translating

class Chat:
    """
        Ini adalah kelas chat.
        Kelas ini digunakan untuk menampung dan 
        memproses teks bahasa alami kedalam fungsi-fungsi
        yang telah dideklarasikan.
    """

    def __init__(self, text):
        self.__text = text
        self.__NER = NER()
        self.__parsing = Parsing()
        self.__translating = Translating()

    def respond(self):
        ner = self.__NER.entity_recognition(self.__text)

        for entity_name, value in self.__NER.get_entities().items():
            if 'tipe' in entity_name and value:
                parsing = self.__parsing.parsing(ner, self.__text)
                result = self.__translating.translate2sql(ner, parsing)
            else:
                self.__NER.add_entities_slot(self.__text)
                parsing = self.__parsing.parsing(ner, self.__text)

        result = self.__NER.get_entities()
        return result