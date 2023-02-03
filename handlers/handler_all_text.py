from handlers.handler import Handler
from settings.message import MESSAGES
from settings import config


class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)
        self.step = 0 # step in order

    def pressed_btn_info(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['trading_store'],
            parse_mode='HTML',
            reply_markup=self.keyboards.info_menu()
        )

    def pressed_btn_settings(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['settings'],
            parse_mode='HTML',
            reply_markup=self.keyboards.settings_menu()
        )

    def pressed_btn_back(self, message):
        self.bot.send_message(
            message.chat.id,
            'Вы вернулись назад',
            reply_markup=self.keyboards.start_menu()
        )

    def pressed_btn_category(self, message):
        self.bot.send_message(
            message.chat.id,
            'Каталог категорий товара',
            reply_markup=self.keyboards.remove_menu()
        )
        self.bot.send_message(
            message.chat.id,
            'Сделайте свой выбор',
            reply_markup=self.keyboards.category_menu()
        )

    def pressed_btn_product(self, message, product):
        exp_product = config.KEYBOARD.get(product)
        self.bot.send_message(
            message.chat.id,
            f'Категория {exp_product}',
            reply_markup=self.keyboards.set_select_category(config.CATEGORY[product])
        )
        self.bot.send_message(
            message.chat.id,
            'Ok',
            reply_markup=self.keyboards.category_menu()
        )

    def pressed_btn_order(self, message):
        self.step = 0

        # получаем список товаров в заказе
        count = self.DB.select_all_product_id(message.from_user.id)

        # получаем количество товара по каждой позиции с заказе
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)

        self.send_message_order(count[self.step], quantity, message)

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):

            # menu
            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:
                if self.DB.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        MESSAGES['no_orders'],
                        parse_mode='HTML',
                        reply_markup=self.keyboards.category_menu()
                    )

            # categories of products
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')
