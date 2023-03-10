from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:

    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0, user_id=None):

        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = '{} {} {}'.format(
                step + 1,
                'из',
                str(self.DB.count_rows_order(user_id))
            )

        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = f'{quantity}'

        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')

        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)

        return self.markup

    def info_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')

        self.markup.row(itm_btn_1)

        return self.markup

    def settings_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)

        itm_btn_1 = self.set_btn('<<')

        self.markup.row(itm_btn_1)

        return self.markup

    def orders_menu(self, step, quantity, user_id):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X', step, quantity)
        itm_btn_2 = self.set_btn('DOUWN', step, quantity)
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity, user_id=user_id)
        itm_btn_4 = self.set_btn('UP', step, quantity)

        itm_btn_5 = self.set_btn('BACK_STEP', step, quantity)
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity, user_id=user_id)
        itm_btn_7 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_8 = self.set_btn('APPLAY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)

        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        self.markup.row(itm_btn_9, itm_btn_8)

        return self.markup

    @staticmethod
    def remove_menu():
        return ReplyKeyboardRemove()

    def category_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))

        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))

        return self.markup

    @staticmethod
    def set_inline_btn(name):
        return InlineKeyboardButton(
            str(name),
            callback_data=str(name.id),
        )

    def set_select_category(self, category):
        self.markup = InlineKeyboardMarkup(row_width=1)
        for item in self.DB.select_all_products_category(category):
            self.markup.add(
                self.set_inline_btn(item)
            )
        return self.markup
