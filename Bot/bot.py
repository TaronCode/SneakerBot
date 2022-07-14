import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from Parsing.nike import parserNike
from Parsing.reebok import reebok_parser
class SneakerBot:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher(self.bot)
        nike_shop = KeyboardButton("Nike")
        reebok_shop = KeyboardButton("Reebok")
        all_shops = KeyboardButton("All")
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard.add(all_shops).add(nike_shop).add(reebok_shop)

        self.bot_work()
        self.start_bot()


    def bot_work(self):
        async def help(message : types.Message):
            await message.answer("Я помогу тебе купить брендовые кроссовки со скидкой в разных магазинах")
            await message.answer("Выбери магазин", reply_markup=self.keyboard)


        async def get_nike_sneakers(message : types.Message):
            await message.answer("Waiting...")

            parserNike.get_data()

            with open("nike_result.json") as file:
                nike_data = json.load(file)

            for item in nike_data:
                card = f"Name : {item.get('title')} \n" \
                f"Link : {item.get('link')} \n" \
                f"Total price : {item.get('total price')} \n" \
                f"Previous price : {item.get('previous price')} \n" \
                f"Sale : {item.get('sale')}"

                await message.answer(card)

        async def get_reebok_sneakers(message : types.Message):
            await message.answer("Waiting...")

            reebok_parser.get_data()

            with open("reebok_results.json") as file:
                reebok_data = json.load(file)

            for item in reebok_data:
                card = f"Name : {item.get('title')} \n" \
                f"Link : {item.get('link')} \n" \
                f"Total price : {item.get('total price')} \n" \
                f"Previous price : {item.get('previous price')} \n" \
                f"Sale : {item.get('sale')}"

                await message.answer(card)



        def register_handlers(dp : Dispatcher):
            dp.register_message_handler(help, commands="start")
            dp.register_message_handler(help, commands="help")
            dp.register_message_handler(get_nike_sneakers, Text(equals="Nike"))
            dp.register_message_handler(get_reebok_sneakers, Text(equals="Reebok"))

        register_handlers(self.dp)


    def start_bot(self):
        executor.start_polling(self.dp, skip_updates=True)



sneaker = SneakerBot()


