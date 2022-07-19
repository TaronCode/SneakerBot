import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from Parsing.nike import parserNike
from Parsing.reebok import reebok_parser
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os

class FSM_states(StatesGroup):
    change_gender = State()


class SneakerBot:
    def __init__(self):
        self.storage = MemoryStorage()
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.gender = None
        nike_shop = KeyboardButton("Nike")
        reebok_shop = KeyboardButton("Reebok")
        gender_key = KeyboardButton("Выбрать пол")
        all_shops = KeyboardButton("All")
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard.add(all_shops).add(nike_shop).add(reebok_shop).add(gender_key)

        self.gender_change_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        male = KeyboardButton("Мужчина")
        female = KeyboardButton("Женшина")
        self.gender_change_keyboard.add(male).add(female)

        self.bot_work()
        self.start_bot()


    def bot_work(self):
        async def help(message : types.Message):
            await message.answer("Я помогу тебе купить брендовые кроссовки со скидкой в разных магазинах")
            await message.answer("Выбери магазин", reply_markup=self.keyboard)

        async def get_nike_sneakers(message : types.Message):
            await message.answer("Waiting...")

            if self.gender == "Мужчина":
                parserNike.get_data(url="https://api.nike.com/product_feed/rollup_threads/v2?filter=marketplace%28US%29&filter=language%28en%29&filter=employeePrice%28true%29&filter=attributeIds%280f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C5b21a62a-0503-400c-8336-3ccfbff2a684%2C193af413-39b0-4d7e-ae34-558821381d3f%29&anchor=0&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24")
                with open("nike_result.json") as file:
                    nike_data = json.load(file)

                for item in nike_data:
                    card = f"Name : {item.get('title')} \n" \
                           f"Link : {item.get('link')} \n" \
                           f"Total price : {item.get('total price')} \n" \
                           f"Previous price : {item.get('previous price')} \n" \
                           f"Sale : {item.get('sale')}"

                    await message.answer(card)

            elif self.gender == "Женшина":
                parserNike.get_data(url="https://api.nike.com/product_feed/rollup_threads/v2?filter=marketplace%28US%29&filter=language%28en%29&filter=employeePrice%28true%29&filter=attributeIds%2816633190-45e5-4830-a068-232ac7aea82c%2C7baf216c-acc6-4452-9e07-39c2ca77ba32%2C5b21a62a-0503-400c-8336-3ccfbff2a684%2C193af413-39b0-4d7e-ae34-558821381d3f%29&anchor=0&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24")
                with open("nike_result.json") as file:
                    nike_data = json.load(file)

                for item in nike_data:
                    card = f"Name : {item.get('title')} \n" \
                           f"Link : {item.get('link')} \n" \
                           f"Total price : {item.get('total price')} \n" \
                           f"Previous price : {item.get('previous price')} \n" \
                           f"Sale : {item.get('sale')}"

                    await message.answer(card)

            else:
                await message.answer("Выберите пол")




        async def get_reebok_sneakers(message : types.Message):
            await message.answer("Waiting...")

            if self.gender == "Мужчина":
                reebok_parser.get_data(url="https://www.reebok.com/api/plp/content-engine?sitePath=us&query=men-classics-shoes-sale")
                with open("reebok_results.json") as file:
                    reebok_data = json.load(file)

                for item in reebok_data:
                    card = f"Name : {item.get('title')} \n" \
                           f"Link : {item.get('link')} \n" \
                           f"Total price : {item.get('total price')} \n" \
                           f"Previous price : {item.get('previous price')} \n" \
                           f"Sale : {item.get('sale')}"

                    await message.answer(card)
                os.remove("reebok_results.json")
            elif self.gender == "Женшина":
                reebok_parser.get_data(url="https://www.reebok.com/api/plp/content-engine?sitePath=us&query=women-classics-shoes-sale")
                with open("reebok_results.json") as file:
                    reebok_data = json.load(file)

                for item in reebok_data:
                    card = f"Name : {item.get('title')} \n" \
                           f"Link : {item.get('link')} \n" \
                           f"Total price : {item.get('total price')} \n" \
                           f"Previous price : {item.get('previous price')} \n" \
                           f"Sale : {item.get('sale')}"

                    await message.answer(card)
                os.remove("reebok_results.json")
            else:
                await message.answer("Выберите пол")




        async def change_gender(message : types.Message):
            await FSM_states.change_gender.set()
            await message.answer("Выберите ваш пол", reply_markup=self.gender_change_keyboard)

        async def set_gender(message : types.Message, state=FSMContext):
            if message.text == "Мужчина":
                self.gender = "Мужчина"
            if message.text == "Женшина":
                self.gender = "Женшина"

            await state.finish()

            await message.answer(f"Ваш пол {self.gender}", reply_markup=self.keyboard)
        def register_handlers(dp : Dispatcher):
            dp.register_message_handler(help, commands="start")
            dp.register_message_handler(help, commands="help")
            dp.register_message_handler(get_nike_sneakers, Text(equals="Nike"))
            dp.register_message_handler(get_reebok_sneakers, Text(equals="Reebok"))
            dp.register_message_handler(change_gender, Text(equals="Выбрать пол"), state=None)
            dp.register_message_handler(set_gender, state=FSM_states.change_gender)

        register_handlers(self.dp)


    def start_bot(self):
        executor.start_polling(self.dp, skip_updates=True)



sneaker = SneakerBot()


