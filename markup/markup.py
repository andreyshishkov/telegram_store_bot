from telebot.types import KeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:

    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    @staticmethod
    def set_btn(name, step=0, quantity=0):
        return KeyboardButton(config.KEYBOARD[name])
