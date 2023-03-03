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

        # получаем количество товара по каждой позиции в заказе
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)

        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['order_number'].format(self.step + 1),
            parse_mode='HTML',
        )

        self.bot.send_message(
            message.chat.id,
            MESSAGES['order'].format(
                self.DB.select_single_product_name(product_id),
                self.DB.select_single_product_title(product_id),
                self.DB.select_single_product_price(product_id),
                self.DB.select_order_quantity(product_id, message.from_user.id)
            ),
            parse_mode='HTML',
            reply_markup=self.keyboards.orders_menu(self.step, quantity, message.from_user.id)
        )

    # buttons of order menu
    def pressed_btn_up(self, message):
        count = self.DB.select_all_product_id(message.from_user.id)

        quantity_order = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])

        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1

            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.DB.update_order_value(count[self.step], message.from_user.id, 'quantity', quantity_order)

        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        count = self.DB.select_all_product_id(message.from_user.id)

        quantity_order = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])

        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1

            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.DB.update_order_value(count[self.step], message.from_user.id, 'quantity', quantity_order)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        # get list of ordered product ids
        count = self.DB.select_all_product_id(message.from_user.id)

        if len(count) > 0:
            # amount of certain position in order
            quantity_order = self.DB.select_order_quantity(count[self.step], message.from_user.id)
            quantity_product = self.DB.select_single_product_quantity(count[self.step])

            quantity_product += quantity_order

            self.DB.delete_order(count[self.step])
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.step -= 1

        count = self.DB.select_all_product_id(message.from_user.id)
        if len(count) > 0:
            quantity_order = self.DB.select_order_quiantity(count[self.step], user_id=message.from_user.id)
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            self.bot.send_message(
                message.chat.id,
                MESSAGES['no_orders'],
                parse_mode='HTML',
                reply_markup=self.keyboards.category_menu()
            )

    def pressed_btn_back_step(self, message):
        if self.step > 0:
            self.step -= 1

        count = self.DB.select_all_product_id(message.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)

        self.send_message_order(
            count[self.step],
            quantity,
            message
        )

    def pressed_btn_next_step(self, message):
        if self.step < (self.DB.count_rows_order(message.from_user.id) - 1):
            self.step += 1

        count = self.DB.select_all_product_id(message.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)

        self.send_message_order(
            count[self.step],
            quantity,
            message
        )

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
                if self.DB.count_rows_order(message.from_user.id) > 0:
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

            #  menu of order
            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)
            if message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_down(message)
            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)
            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)
            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)
