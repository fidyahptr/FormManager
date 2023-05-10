from flask import Flask, render_template, request
from config import mysql
from dialog_manager.form.login import login
import pymysql

# login
def login_controller():
    chat_history = []
    chat_opening = 'Silakan login dengan memasukkan format berikut: [email][password]'
    current_route = 'login'
    if request.method == 'POST':
        # Get the form data
        data = request.form['user_response'] 
        chat_history.append(('user', data))
        
        res = login(data)
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
                user_name = user['nama']
                chat_history.append(('bot', user_name))
                return render_template('result.html', chat_history=chat_history, status=user_name)   
            else:
                # show error message if login fails
                chat_history.append(('bot', 'Invalid username or password'))
                return render_template('result.html', chat_history=chat_history)
        else:
            response = 'Email/pass tidak valid! Silakan login dengan memasukkan format berikut: [email][password]'
            chat_history.append(('bot', response))
            return render_template('result.html', chat_history=chat_history)
    else:
        return render_template('chat.html', chat_opening=chat_opening, current_route=current_route)