from flask import Blueprint
from interfaces.web.controllers.indexController import Chatbot

indexBP = Blueprint('indexBP', __name__)
indexBP.route('/', methods=['GET', 'POST'])(Chatbot().index)
