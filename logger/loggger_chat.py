import logging
import re

# buat objek logger
logger = logging.getLogger('user_input_logger')
logger.setLevel(logging.INFO)

# buat formatter
formatter = logging.Formatter('%(message)s')

# buat handler untuk menyimpan log ke dalam file txt
file_handler = logging.FileHandler('logger/user_input_log.txt')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# tambahkan handler ke logger
logger.addHandler(file_handler)

# as per recommendation compile once only
CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

# fungsi untuk menangkap input pengguna dan mencatatnya dalam log
def log_user_input(chat_history):
    for actor, chat in chat_history:
        chat = cleanhtml(chat)
        log = actor + ' : ' + chat
        logger.info(log)