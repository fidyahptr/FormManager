from dialog_manager.form.login import Login
from dialog_manager.form.register import Register
from dialog_manager.form.checkout import Checkout
from dialog_manager.form.get_entitas import *
from datetime import datetime

class TestSlotFrameBased:

    login = Login()
    regis = Register()
    checkout = Checkout()

    def test_slot_login(self):
       
        # Arrange
        text = "[fidyah@gmail.com][12345]"
        
        # Act
        slot = self.login.login(text)

        # Assert
        assert slot == {'email': 'fidyah@gmail.com', 'pass': '12345', 'response': None}
    
    def test_slot_login_tanpa_kurung_siku(self):
       
        # Arrange
        self.login.delete_slot_login()
        text = "fidyah@gmail.com 12345"
        
        # Act
        slot = self.login.login(text)

        # Assert
        assert slot == {'email': None, 'pass': None, 'response': 'Maaf kak, formatnya kurang tanda kurung siku [ ] :('}
    
    def test_slot_login_format_email_salah(self):
       
        # Arrange
        self.login.delete_slot_login()
        text = "[fidyah][12345]"
        
        # Act
        slot = self.login.login(text)

        # Assert
        assert slot == {'email': None, 'pass': '12345', 'response': None}
         
    def test_slot_register(self):
       
        # Arrange
        text = "[fidyah][fidyah@gmail.com][12345]"
        
        # Act
        slot = self.regis.regis(text)

        # Assert
        assert slot == {'nama': 'fidyah', 'email': 'fidyah@gmail.com', 'pass': '12345', 'response': None}
        
    def test_slot_register_tanpa_kurung_siku(self):
       
        # Arrange
        self.regis.delete_slot_regis()
        text = "fidyah fidyah@gmail.com 12345"
        
        # Act
        slot = self.regis.regis(text)

        # Assert
        assert slot == {'nama': None, 'email': None, 'pass': None, 'response': 'Maaf kak, formatnya kurang tanda kurung siku [ ] :('}
        
    def test_slot_register_format_email_salah(self):
       
        # Arrange
        self.regis.delete_slot_regis()
        text = "[fidyah][fidyahemail][12345]"
        
        # Act
        slot = self.regis.regis(text)

        # Assert
        assert slot == {'nama': 'fidyah', 'email': None, 'pass': '12345', 'response': None}
   
    def test_slot_checkout(self):
        
        # Arrange
        text = "saya mau beli laptop asus zenbook"
        tanggal = datetime.today().strftime('%Y-%m-%d')
        
        # Act
        slot = self.checkout.checkout(text)

        # Assert
        assert slot == {'merk': 'asus', 'tipe': 'zenbook 13', 'jumlah': None, 'tanggal': tanggal, 'response': None, 'multiple': None}
        
    def test_slot_checkout_merk_tidak_tersedia(self):
        
        # Arrange
        self.checkout.delete_slot_checkout()
        remove_merktipe()
        text = "saya mau beli laptop axioo"
        tanggal = datetime.today().strftime('%Y-%m-%d')
        
        # Act
        slot = self.checkout.checkout(text)

        # Assert
        assert slot == {'merk': None, 'tipe': None, 'jumlah': None, 'tanggal': tanggal, 'response': 'Maaf, merk/tipe tidak tersedia.<br>Berikut daftar seluruh merk laptop yang tersedia : <ul class="list-disc list-outside ml-5"><li>Lenovo</li><li>Asus</li><li>Microsoft</li><li>Dell</li><li>Hp</li><li>Acer</li><li>Apple</li><li>Xiaomi</li><li>Msi</li><li>Infinix</li><li>Samsung</li></ul>', 'multiple': None}
        
    def test_slot_checkout_multiple_tipe(self):
        
        # Arrange
        self.checkout.delete_slot_checkout()
        remove_merktipe()
        text = "saya mau beli laptop asus rog"
        tanggal = datetime.today().strftime('%Y-%m-%d')
        
        # Act
        slot = self.checkout.checkout(text)

        # Assert
        assert slot == {'merk': None, 'tipe': None, 'jumlah': None, 'tanggal': tanggal, 'response': None, 'multiple': [['rog zephyrus g14'], ['rog strix scar 17'], ['rog strix gl553vd']]}