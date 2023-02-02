from handlers.handler import Handler


class HandlerCommands(Handler):

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        user = message.from_user.first_name
        self.bot.send_message(
            message.chat.id,
            f'{user}, здравствуйте! Жду дальнейших задач.',
            reply_markup=self.keyboards.start_menu()
        )

    def handle(self):
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
