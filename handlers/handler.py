from abc import ABC, abstractmethod
from markup.markup import Keyboards
from data_base.dbalchemy import DBManager


class Handler(ABC):

    def  __init__(self, bot):
        self.bot = bot
        self.keyboards = Keyboards()
        self.DB = DBManager()

    @abstractmethod
    def handle(self):
        pass
