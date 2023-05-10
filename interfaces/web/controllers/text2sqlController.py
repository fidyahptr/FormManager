from flask import render_template, request, jsonify, make_response
from config import mysql
from nlu.entities.ner_detection_stok import NER
from dialog_manager.text2sql.parsing import Parsing
from dialog_manager.text2sql.translating import Translating
from dialog_manager.text2sql.database.db import DB
from nlu.intents.intent_detection import IntentDetection

temp = []
intent_history = []

def text2sql():

    deteksi_intent = IntentDetection()
    chat_history = []
    
    if request.method == 'POST':

        # get user response
        user_resp = request.form['user_response'].lower()
        chat_history.append(('user', user_resp))
        temp.append(('user', user_resp))
        intent = deteksi_intent.prediction(user_resp)
        print(intent)
        # check_bool = False

        # check entitas
        er = NER().entity_recognition(user_resp)
        print(er)

        if er['merk']:

            parsing = Parsing().parsing(er, temp[0][1])
            translating = Translating().translate2sql(er, parsing)
            print(translating)

            if er['tipe']:
                # check_bool = True 
                result = DB().query(translating)

                if result:
                    bot_resp = "Laptop {} tipe {} masih ada, stoknya masih {}".format(er['merk'], er['tipe'], result)
                    chat_history.append(('bot', bot_resp))
                    chat_history.append(('bot', 'Ada lagi yang bisa dibantu?'))  
                
            else:

                # re-ask
                chat_history.append(('bot', 'apa tipe laptopnya?'))

                # get user response for entitas tipe
                tipe = request.form['user_response'].lower()
                NER().add_entities_slot(tipe)

                result = DB().query(translating)
                chat_history.append(('bot', result))

        else:
            chat_history.append(('bot', 'silahkan masukkan merk yang sesuai'))
    

        # if check_bool:
        #     NER().get_entities().clear()
        #     check_bool = False

        return render_template('result.html', chat_history=chat_history)
         
    else:
        return render_template('user_form.html')