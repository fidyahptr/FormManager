import re

class Register():
    """_summary_

    Returns:
        _type_: _description_
    """
    
    def __init__(self):
        pass
    # regex
    format = re.compile(r'\[.*?\]')
    email_regex = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # deklarasi slot, use dict pyhton
    # value : {'email': None, 'pass': None}
    slot_regis = dict.fromkeys(['nama', 'email', 'pass', 'response'])

    def cek_email(self, result):
        # cek email match to regex, apakah email valid
        if self.email_regex.match(result):
            # add value email to slot
            self.slot_regis['email'] = self.email_regex.findall(result)[0]
        # jika tidak sesuai format, system print email tidak valid
        else:
            return self.slot_regis

    def regis(self, user_input):
        self.slot_regis['response'] = None
        # get isi dari format
        list_input = self.format.findall(user_input)
        j = 0
        
        if list_input:
            for i in list_input:
                result = i.replace('[', '').replace(']', '')
                if j == 0:
                    self.slot_regis['nama'] = result
                elif j == 1:
                    # cek email match to regex, apakah email valid
                    self.cek_email(result)
                else:
                    self.slot_regis['pass'] = result
                    if self.slot_regis['nama'] and self.slot_regis['email'] and self.slot_regis['pass']:
                        return self.slot_regis
                j += 1
        else:
            self.slot_regis['response'] = "Maaf kak, formatnya kurang tanda kurung siku [ ] :("

        return self.slot_regis

    def delete_slot_regis(self):
        self.slot_regis['nama'] = None
        self.slot_regis['email'] = None
        self.slot_regis['pass'] = None