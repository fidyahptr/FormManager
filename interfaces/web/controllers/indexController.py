from flask import render_template, request
from nlu.entities.ner_detection_stok import NER
from nlu.intents.intent_detection import IntentDetection
# from web.controllers.text2sqlController import text2sql
from dialog_manager.text2sql.parsing import Parsing
from dialog_manager.text2sql.translating import Translating
from dialog_manager.text2sql.database.db import DB
from config import mysql
from dialog_manager.form.login import Login
from dialog_manager.form.register import Register
from dialog_manager.form.checkout import Checkout
from dialog_manager.form.get_entitas import NER
from logger.loggger_chat import log_user_input
import pymysql

class Chatbot():

    __temp_text = []
    __intent_history = []
    __intent = 0

    __bool_check = True

    # form manager
    __chat_opening_index = 0
    __chat_opening_index2 = 0
    __email = None
    __intent_member = None
    __check_regis = None
    __check_checkout = None
    __chat_opening_index_akun = 0

    def __init__(self):
        pass
    
    def index(self):
        
        chat_history = []
        multiple_tipe = None
        if request.method == 'POST':

            # get user response
            user_resp = request.form['user_response'].lower()

            # save user response
            chat_history.append(('user', user_resp))
            self.__temp_text.append(('user', user_resp))
            
            # detect intent
            if self.__bool_check:
                self.__intent = IntentDetection().prediction(user_resp)
                self.__intent_history.append(self.__intent)

            print(self.__intent_history)
            
            if self.__intent == 0 or self.__intent_history[len(self.__intent_history) - 1] == 0:
                self.login_controller(user_resp, chat_history)
                
            elif self.__intent == 1 or self.__intent_history[len(self.__intent_history) - 1] == 1:
                self.regis_controller(user_resp, chat_history)
            
            elif self.__intent == 7 or self.__intent_history[len(self.__intent_history) - 1] == 7:    
                # skenario 2
                if self.__chat_opening_index == 0:
                    print(self.__email)
                    print('opening form checkout')
                    chat_opening = "Halo kak, apa merk laptop yang ingin anda pesan?"
                    chat_history.append(('bot', chat_opening))
                    self.__bool_check = False
                    self.__chat_opening_index+=1
                elif self.__chat_opening_index > 0 and self.__check_checkout == None:
                    print('form checkout')
                    res = Checkout().checkout(user_resp)
                    print('controller' + str(res))
                    if res['response'] and (res['merk'] == None or res['tipe'] == None):
                        chat_history.append(('bot', res['response']))
                        
                    if res['multiple']:
                        multiple_tipe = ''
                        for option in res['multiple']:
                            print(option)
                            multiple_tipe += '<button onclick="multiple_tipe(\'' + str(option[0]) + '\')" class="relative inline-flex items-center justify-center p-0.5 mb-2 mr-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-green-400 to-blue-600 group-hover:from-green-400 group-hover:to-blue-600 hover:text-white focus:ring-4 focus:outline-none focus:ring-green-200"> <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white rounded-md group-hover:bg-opacity-0">' + str(option[0]) + '</span> </button>'    
                        chat_history.append(('bot', "Maksudnya yang ini ya kak?"))
                        chat_history.append(('multiple_tipe', multiple_tipe))
                    # cek input & get slot one by one, response
                    elif res['merk'] == None or res['tipe'] ==  None or res['jumlah'] == None:
                        if res['merk'] == None:
                            response = Checkout().question['merk']
                        elif res['tipe'] == None:
                            response = Checkout().question['tipe']
                        elif res['jumlah'] == None:
                            response = Checkout().question['jumlah']
                            chat_history.append(('bot', response))
                            response = 'Masukkan format angka. contoh : 1/2/3.'
                            res['jumlah'] = 0
                        chat_history.append(('bot', response))
                        
                    elif res['merk'] and res['tipe']:
                        
                        if res['jumlah']:
                            chat_history.append(('bot', res))
                        else:
                            get_number = Checkout().check_number.findall(user_resp)
                            
                            if get_number:
                                Checkout().slot_checkout['jumlah'] = get_number[0]
                                res['jumlah'] = get_number[0]
                                self.__check_checkout = 'selesai'
                            # jika format jumlah salah
                            else:
                                chat_history.append(('bot', 'Maaf, Format anda salah:('))
                                chat_history.append(('bot', 'Masukkan format angka. contoh : 1/2/3.'))
                elif self.__email == None and self.__check_regis == None:
                    if self.__chat_opening_index2 == 1:
                        self.__intent_member = IntentDetection().prediction(user_resp)
                    self.__chat_opening_index2+=1
                    print('arahin ke form')
                    print(self.__chat_opening_index)
                    print('intent member : ' + str(self.__intent_member))
                    if self.__intent_member == 10:
                        print('form login')
                        self.login_controller(user_resp, chat_history)
                    else:
                        print('form regis')
                        self.__check_regis = self.regis_controller(user_resp, chat_history)
                        print(self.__check_regis)
                
                if self.__chat_opening_index2 == 0 and self.__check_checkout and self.__email == None:
                    chat_opening = "Baik, sebelum Anda dapat melakukan pemesanan produk, Anda harus login terlebih dahulu."
                    chat_history.append(('bot', chat_opening)) 
                    chat_history.append(('bot', "Apakah Anda sudah memiliki akun yang terdaftar di website kami?"))
                    self.__chat_opening_index2+=1
                elif self.__check_regis and self.__email == None:
                    print('cek regis')
                    self.login_controller(user_resp, chat_history)
                          
                if self.__email and self.__check_checkout:
                    print('masuk ke insert db')
                    res = Checkout().slot_checkout
                    print(res)
                    #db
                    conn = None
                    cursor = None
                    # execute a SELECT query to check if user exists in database
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    select_produk_query = "SELECT * FROM produk WHERE merk = %s AND tipe = %s"
                    data = (res['merk'], res['tipe'])
                    cursor.execute(select_produk_query, data)
                    produk = cursor.fetchone()
                    if produk:
                        insert_transaksi_query = "INSERT INTO transaksi (email, tanggal, id_produk, jumlah) VALUES (%s, %s, %s, %s)"
                        data_transaksi = (self.__email, res['tanggal'], produk['id'], res['jumlah'])
                        cursor.execute(insert_transaksi_query, data_transaksi)
                        cursor.execute("SELECT LAST_INSERT_ID()")
                        new_data = cursor.fetchone()
                        print(new_data)
                        id_transaksi = Checkout().check_number.findall(str(new_data))
                        id_transaksi = ''.join(id_transaksi)
                        print(id_transaksi)
                        # Check if data has been successfully inserted
                        if cursor.rowcount > 0:
                            # Commit the changes and close the cursor and connection objects
                            conn.commit()
                            cursor.close()
                            conn.close()
                            response = 'Pemesanan anda berhasil diproses. Berikut nota pembayaran anda:)'
                            chat_history.append(('bot', response))
                            harga_total = produk['harga']* float(res['jumlah'])
                            nota = render_template('nota.html', email=self.__email, res=res, produk=produk, id_transaksi=id_transaksi, harga_total=harga_total)
                            chat_history.append(('bot', nota))
                            chat_history.append(('bot', 'Terima kasih telah melakukan pemesanan di toko kami:)'))
                            Checkout().delete_slot_checkout()
                            NER().remove_merktipe()
                            # reset
                            self.__bool_check = True
                            self.__chat_opening_index = 0
                            self.__chat_opening_index2 = 0
                            self.__check_checkout = None
                        else:
                            # Rollback the transaction and close the cursor and connection objects
                            conn.rollback()
                            cursor.close()
                            conn.close()
                            chat_history.append(('bot', 'Maaf, pemesanan gagal:('))
                            
                    else:
                        # show error message if produk tdk ada
                        chat_history.append(('bot', 'Maaf, Produk yang anda cari tidak tersedia:('))
                        
            elif self.__intent == 3:
                chat_history.append(('bot', "Halo kak"))
                chat_history.append(('bot', "Ada yang bisa chippy bantu?"))
            
            elif self.__intent == 8:
                chat_history.append(('bot', "Maaf, saya tidak dapat memberikan rekomendasi laptop :("))
                chat_history.append(('bot', "Chippy hanya dapat membantu Anda melakukan pembelian laptop"))
            
            elif self.__intent == 5:
                chat_history.append(('bot', "Maaf, untuk deskripsi produk belum tersedia ya kak"))
                chat_history.append(('bot', "Chippy hanya dapat membantu Anda melakukan pembelian laptop"))
               
            elif self.__intent == 6:
                chat_history.append(('bot', "Maaf, untuk harga produk belum tersedia ya kak"))
                chat_history.append(('bot', "Chippy hanya dapat membantu Anda melakukan pembelian laptop"))
            
            elif self.__intent == 9:
                chat_history.append(('bot', "Maaf, saya tidak dapat memberikan stok produk"))
                chat_history.append(('bot', "Chippy hanya dapat membantu Anda melakukan pembelian laptop"))
               
            elif self.__intent == 2:
                chat_history.append(('bot', "Terima kasih telah mengunjungi toko kami"))
                
            elif self.__intent == 11:
                chat_history.append(('bot', "Sama-sama kak"))
                
            else:
                chat_history.append(('bot', "Maaf, Chippy hanya dapat membantu Anda melakukan pembelian laptop"))
            
            log_user_input(chat_history)
            return render_template('result.html', chat_history=chat_history)
        else:
            return render_template('user_form.html')
        
    # login
    def login_controller(self, user_resp, chat_history):
        print('masuk ke login controller')
        if self.__chat_opening_index_akun == 0:
            chat_opening = 'Silakan login dengan memasukkan format berikut: [email][password]'
            chat_history.append(('bot', chat_opening))
            chat_opening = 'Contoh: [fidyahputri@gmail.com][secret]'
            chat_history.append(('bot', chat_opening))
            self.__bool_check = False
            self.__chat_opening_index_akun+=1
        else:
            res = Login().login(user_resp)
            print(res)
            # cek jika keluaran ad yg kosong
            if res['email'] and res['pass']:
                conn = None
                cursor = None
                # execute a SELECT query to check if user exists in database
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                select_user_query = "SELECT * FROM pengguna WHERE email = %s AND pass = %s"
                data = (res['email'], res['pass'])
                cursor.execute(select_user_query, data)
                user = cursor.fetchone()
                cursor.close()
                # cek jika user tersedia
                if user:
                    chat_history.append(('bot', 'Login berhasil, ' + user['nama'] + '! Kami senang Anda kembali ke toko online kami.')) 
                    self.__bool_check = True
                    self.__chat_opening_index_akun = 0
                    self.__email = user['email']
                    self.__check_regis = None
                    Login().delete_slot_login()
                    return user['email']
                else:
                    Login().delete_slot_login()
                    # show error message if login fails
                    chat_history.append(('bot', 'Maaf, email/pass anda salah:('))
                    chat_history.append(('bot', 'Silakan login ulang dengan memasukkan format berikut: [email][password]'))
            elif res['response']:
                chat_history.append(('bot', res['response']))
                chat_history.append(('bot', 'Silakan login ulang dengan memasukkan format berikut: [email][password]'))
            else:
                response = 'Email/pass tidak valid!'
                chat_history.append(('bot', response))
                chat_history.append(('bot', 'Silakan login ulang dengan memasukkan format berikut: [email][password]'))
            
    # regis
    def regis_controller(self, user_resp, chat_history):
        print('masuk ke regis controller')
        if self.__chat_opening_index_akun == 0:
            chat_opening = "Silakan registrasi dengan memasukkan format berikut: [nama][email][password]"
            chat_history.append(('bot', chat_opening))
            chat_opening = "Contoh : [Fidyah][fidyahputri@gmail.com][secret]"
            chat_history.append(('bot', chat_opening))
            self.__bool_check = False
            self.__chat_opening_index_akun+=1
        else:
            res = Register().regis(user_resp)
            print('res ' + str(res))
            # cek jika keluaran ad yg kosong
            if res['nama'] and res['email'] and res['pass']:
                try:
                    print(res)
                    conn = None
                    cursor = None
                    # execute a INSERT query to add data to database
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    select_user_query = "INSERT INTO pengguna (email, pass, nama) VALUES (%s, %s, %s)"
                    data = (res['email'], res['pass'], res['nama'])
                    cursor.execute(select_user_query, data)
                    # add try catch to detect Duplicate key (duplikat email)
                    # Check if data has been successfully inserted
                    if cursor.rowcount > 0:
                        # Commit the changes and close the cursor and connection objects
                        conn.commit()
                        cursor.close()
                        conn.close()
                        response = 'Terima kasih atas informasinya, ' + res['nama'] + '. Akun Anda sekarang telah terdaftar di situs kami.'
                        chat_history.append(('bot', response))
                        self.__bool_check = True
                        self.__chat_opening_index_akun = 0
                        # self.__email = res['email']
                        Register().delete_slot_regis()
                        if self.__intent_history[len(self.__intent_history) - 1] != 7:
                            self.__intent_history.append(0)
                            print(self.__intent_history)
                            self.login_controller(user_resp, chat_history)
                        else:
                            print('balik ke checkout')
                            self.__intent_member == 10
                            return 'login'
                        # return res['email']
                    else:
                        # Rollback the transaction and close the cursor and connection objects
                        conn.rollback()
                        cursor.close()
                        conn.close()
                        chat_history.append(('bot', 'Maaf, Registrasi gagal'))
                        Register().delete_slot_regis()
                except:
                    chat_history.append(('bot', 'Wah email anda sudah terdaftar'))
                    chat_history.append(('bot', 'Pake email lain ya kak'))
                    chat_history.append(('bot', 'Silakan registrasi ulang dengan memasukkan format berikut: [nama][email][password]'))
                    # hapus slot value
                    Register().delete_slot_regis()
                    print(res)
            elif res['response']:
                chat_history.append(('bot', res['response']))
                chat_history.append(('bot', 'Silakan registrasi ulang dengan memasukkan format berikut: [nama][email][password]'))
            else:
                response = 'Email/pass tidak valid!'
                chat_history.append(('bot', response))
                chat_history.append(('bot', 'Silakan registrasi ulang dengan memasukkan format berikut: [nama][email][password]'))