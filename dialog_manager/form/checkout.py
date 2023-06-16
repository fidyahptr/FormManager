import re
from dialog_manager.form.get_entitas import NER
from datetime import datetime

class Checkout:
    """_summary_

    Returns:
        _type_: _description_
    """
        
    # regex
    check_number = re.compile(r'\b\d+\b')

    # deklarasi slot, use dict pyhton
    # value : {'merk': None, 'tipe': None, 'jumlah': None}
    slot_checkout = dict.fromkeys(['merk', 'tipe', 'jumlah', 'tanggal', 'response', 'multiple'])

    # pertanyaan tiap slot
    question = {
        'merk': 'Apa merk laptop yang ingin anda beli?',
        'tipe': 'Apa tipe dari laptop yang anda inginkan?',
        'jumlah': 'Berapa jumlah laptop yang ingin anda beli?'
    }

    def __init__(self):
        pass
    
    def checkout(self, data):
        # get entitas (just merk&tipe) cannot jumlah
        result = NER().get_entitas(data)
        print('form ' + str(result))
        # result = NER().entity_recognition(data)
        self.slot_checkout['response'] = None
        self.slot_checkout['multiple'] = None
        # cek entitas
        
        #add current date to slot
        self.slot_checkout['tanggal'] = datetime.today().strftime('%Y-%m-%d')
        
        # jika tertedeksi 2 entitas (merk, tipe)
        if result['merk'] and result['tipe']:
            # cek apakah merk tipe match
            print(len(result['tipe']))
            if len(result['tipe']) <= 1:
                print("ga multiple")
                match = NER().check_match()
                # jika match, do slot filling
                if match == 'match':
                    self.slot_checkout['merk'] = result['merk'][0]
                    self.slot_checkout['tipe'] = result['tipe'][0][0]
                # jika tdk match, tdk dilakukan slot filling
                else:
                    self.slot_checkout['response'] = "Maaf, merk dan tipe tidak cocok. <br> Berikut tipe laptop dari merk " + \
                        str(result['merk'][0] + ' : ' +
                            str(NER().get_tipe(result['merk'][0])))
                    # hapus result dan dis
                    del result
                    self.slot_checkout['merk'] = None
                    self.slot_checkout['tipe'] = None
                    NER().remove_merktipe()
            else:
                print(result['tipe'])
                self.slot_checkout['multiple'] = result['tipe']
                # hapus result dan dis
                result['tipe'] = None
                self.slot_checkout['tipe'] = None
                NER().remove_tipe()
        # jika entitas hanya merk
        elif result['merk']:
            if result['tipe']:
                # slot filling
                self.slot_checkout['merk'] = result['merk'][0]
            else:
                # slot filling
                self.slot_checkout['merk'] = result['merk'][0]
                self.slot_checkout['response'] = "Berikut tipe laptop dari merk " + \
                    str(result['merk'][0] + ' : ' +
                        str(NER().get_tipe(result['merk'][0])))
        # jika entitas hanya tipe
        elif len(result['tipe']) > 1:
            self.slot_checkout['multiple'] = result['tipe']
            # hapus result dan dis
            result['tipe'] = None
            self.slot_checkout['tipe'] = None
            NER().remove_tipe()
        elif result['tipe']:
            # slot filling
            self.slot_checkout['tipe'] = result['tipe'][0][0]
        # jika tdk terdeteksi entitas
        else:
            self.slot_checkout['response'] = 'Maaf, merk tidak tersedia.'
            self.slot_checkout['response'] += '<br>Berikut daftar seluruh merk laptop yang tersedia : '
            self.slot_checkout['response'] += str(NER().get_all_merk())

        return self.slot_checkout

    def delete_slot_checkout(self):
        self.slot_checkout['merk'] = None
        self.slot_checkout['tipe'] = None
        self.slot_checkout['jumlah'] = None
        self.slot_checkout['tanggal'] = None