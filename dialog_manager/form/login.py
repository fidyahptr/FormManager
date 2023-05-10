import re

class Login:
    """_summary_
    """
    
    def __init__(self):
        pass
    
    # regex
    format = re.compile(r'\[.*?\]')
    email_regex = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # deklarasi slot, use dict pyhton
    # value : {'email': None, 'pass': None}
    slot_login = dict.fromkeys(['email', 'pass', 'response'])


    def cek_email(self, result):
        # cek email match to regex, apakah email valid
        if self.email_regex.match(result):
            # add value email to slot
            self.slot_login['email'] = self.email_regex.findall(result)[0]
        # jika tidak sesuai format, system print email tidak valid
        else:
            return self.slot_login

    def login(self, user_input):
        self.slot_login['response'] = None
        # get isi dari format
        list_input = self.format.findall(user_input)
        j = 0
        # cek satu" inputan user
        if list_input:
            for i in list_input:
                # remove tanda kurung
                result = i.replace('[', '').replace(']', '')
                # jika input urutan pertama, masukkan ke slot value email
                if j == 0:
                    self.cek_email(result)
                # inputan ke 2, masukkan value ke self.slot_login password
                else:
                    self.slot_login['pass'] = result
                    if self.slot_login['email'] and self.slot_login['pass']:
                        return self.slot_login
                j += 1
        else:
            self.slot_login['response'] = "Maaf kak, formatnya kurang tanda kurung siku [ ] :(" 

        return self.slot_login

    def delete_slot_login(self):
        self.slot_login['email'] = None
        self.slot_login['pass'] = None