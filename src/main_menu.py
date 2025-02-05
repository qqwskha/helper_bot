#src/main_menu.py
import logging
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.config import PRACTICAL_WORKS
from src.titles_mapping import TITLES_MAPPING
from src.user_state import UserState

# Логирование
logging.basicConfig(level=logging.INFO)


class MainMenu:
    def __init__(self, bot, dp, user_states):
        self.bot = bot
        self.dp = dp
        self.user_states = user_states

    def register_handlers(self):
        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            user_id = message.from_user.id
            self.user_states[user_id] = UserState()
            await self.send_main_menu(user_id, message.from_user.first_name)
            logging.info(f"Handled /start command for user {user_id}")

        @self.dp.message_handler(commands=['info'])
        async def info(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /info without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_info(user_id)
            logging.info(f"Handled /info command for user {user_id}")

        @self.dp.message_handler(commands=['prices'])
        async def prices(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /prices without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_prices(user_id)
            logging.info(f"Handled /prices command for user {user_id}")

        @self.dp.message_handler(commands=['help'])
        async def help_command(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /help without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_help(user_id)
            logging.info(f"Handled /help command for user {user_id}")

        @self.dp.message_handler(commands=['search_work'])
        async def search_work(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /search_work without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_disciplines_menu(user_id)
            logging.info(f"Handled /search_work command for user {user_id}")

        @self.dp.message_handler(commands=['feedback'])
        async def feedback(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /feedback without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_feedback_request(user_id)
            logging.info(f"Handled /feedback command for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data == "main_menu")
        async def main_menu(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use main_menu callback without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_main_menu(user_id, query.from_user.first_name)
            await query.answer()
            logging.info(f"Handled main_menu callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data == "info")
        async def info_callback(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use info callback without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_info(user_id)
            await query.answer()
            logging.info(f"Handled info callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data == "prices")
        async def prices_callback(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use prices callback without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_prices(user_id)
            await query.answer()
            logging.info(f"Handled prices callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data == "search_work")
        async def search_work_callback(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use search_work callback without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_disciplines_menu(user_id)
            await query.answer()
            logging.info(f"Handled search_work callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data == "feedback")
        async def feedback_callback(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use feedback callback without starting the bot")
                return
            await self.delete_previous_message(user_id)
            await self.send_feedback_request(user_id)
            await query.answer()
            logging.info(f"Handled feedback callback for user {user_id}")

    async def send_main_menu(self, user_id, first_name):
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(InlineKeyboardButton("Информация", callback_data="info"))
        keyboard.add(InlineKeyboardButton("Цены", callback_data="prices"))
        keyboard.add(InlineKeyboardButton("Перейти к поиску работы", callback_data="search_work"))
        keyboard.add(InlineKeyboardButton("Обратная связь", callback_data="feedback"))
        greeting_message = f"Добро пожаловать, {first_name}!"
        message = await self.bot.send_message(user_id, greeting_message, reply_markup=keyboard)
        self.user_states[user_id].message_id = message.message_id
        logging.info(f"Sent main menu to user {user_id}")

    async def send_info(self, user_id):
        keyboard = self.get_back_to_main_menu_keyboard()
        await self.bot.send_message(
            user_id,
            "Информация о боте:\n\n"
            "Этот бот помогает выбрать и оплатить практические работы.\n"
            "Для начала выберите дисциплину, затем практическую работу и вариант.",
            reply_markup=keyboard,
        )
        logging.info(f"Sent info message to user {user_id}")

    async def send_prices(self, user_id):
        keyboard = self.get_back_to_main_menu_keyboard()
        prices_info = "Цены на практические работы:\n\n"
        for discipline, practical_types in PRACTICAL_WORKS.items():
            prices_info += f"**{discipline}**:\n"
            for practical_type, variants in practical_types.items():
                prices_info += f"  • {practical_type}:\n"
                for variant, data in variants.items():
                    prices_info += f"    - {variant}: {data['price']} рублей\n"
            prices_info += "\n"
        await self.bot.send_message(
            user_id,
            prices_info,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
        logging.info(f"Sent prices message to user {user_id}")

    async def send_help(self, user_id):
        keyboard = self.get_back_to_main_menu_keyboard()
        await self.bot.send_message(
            user_id,
            "Список доступных команд:\n"
            "/start - Начать работу с ботом\n"
            "/info - Информация о боте\n"
            "/prices - Цены на практические работы\n"
            "/search_work - Перейти к поиску работы\n"
            "/search - Поиск работ по словам\n"
            "/feedback - Отправить сообщение для обратной связи\n"
            "/help - Помощь",
            reply_markup=keyboard,
        )
        logging.info(f"Sent help message to user {user_id}")

    async def send_disciplines_menu(self, user_id):
        keyboard = InlineKeyboardMarkup(row_width=2)
        disciplines = list(PRACTICAL_WORKS.keys())
        for discipline in disciplines:
            full_title = TITLES_MAPPING.get(discipline, discipline)  # Получаем полное название
            keyboard.insert(InlineKeyboardButton(full_title, callback_data=f"disc_{discipline}"))
        keyboard.add(InlineKeyboardButton("Назад", callback_data="main_menu"))
        message = await self.bot.send_message(user_id, "Выберите дисциплину:", reply_markup=keyboard)
        self.user_states[user_id].message_id = message.message_id
        logging.info(f"Sent disciplines menu to user {user_id}")

    async def send_practical_types_menu(self, user_id, discipline):
        keyboard = InlineKeyboardMarkup(row_width=2)
        practical_types = list(PRACTICAL_WORKS[discipline].keys())
        for practical_type in practical_types:
            full_title = TITLES_MAPPING.get(practical_type, practical_type)  # Получаем полное название
            keyboard.insert(InlineKeyboardButton(full_title, callback_data=f"pr_{practical_type}"))
        keyboard.add(InlineKeyboardButton("Назад", callback_data="main_menu"))
        keyboard.add(InlineKeyboardButton("На главную", callback_data="main_menu"))
        message = await self.bot.send_message(user_id,
                                              f"Выберите тип практической работы для {TITLES_MAPPING.get(discipline, discipline)}:",
                                              reply_markup=keyboard)
        self.user_states[user_id].message_id = message.message_id
        logging.info(f"Sent practical types menu for {discipline} to user {user_id}")

    async def send_variants_menu(self, user_id, practical_type):
        keyboard = InlineKeyboardMarkup(row_width=2)
        discipline = self.user_states[user_id].discipline
        variants = list(PRACTICAL_WORKS[discipline][practical_type].keys())
        for variant in variants:
            full_title = TITLES_MAPPING.get(variant, variant)  # Получаем полное название
            keyboard.insert(InlineKeyboardButton(full_title, callback_data=f"var_{variant}"))
        keyboard.add(InlineKeyboardButton("Назад", callback_data=f"back_to_practicals_{practical_type}"))
        keyboard.add(InlineKeyboardButton("На главную", callback_data="main_menu"))
        message = await self.bot.send_message(user_id,
                                              f"Выберите вариант для {TITLES_MAPPING.get(practical_type, practical_type)}:",
                                              reply_markup=keyboard)
        self.user_states[user_id].message_id = message.message_id
        logging.info(f"Sent variants menu for {practical_type} to user {user_id}")

    async def send_feedback_request(self, user_id):
        keyboard = self.get_back_to_main_menu_keyboard()
        await self.bot.send_message(
            user_id,
            "Введите ваше сообщение для обратной связи:",
            reply_markup=keyboard,
        )
        self.user_states[user_id].state = "awaiting_feedback"
        logging.info(f"Sent feedback request to user {user_id}")

    def get_confirmation_keyboard(self, practical_type, variant):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Подтвердить", callback_data="confirm_choice"))
        keyboard.add(InlineKeyboardButton("Назад", callback_data=f"back_to_variants_{practical_type}"))
        keyboard.add(InlineKeyboardButton("На главную", callback_data="main_menu"))
        return keyboard

    def get_back_to_main_menu_keyboard(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("На главную", callback_data="main_menu"))
        return keyboard

    async def delete_previous_message(self, user_id):
        user_state = self.user_states[user_id]
        if user_state.message_id is not None:
            try:
                await self.bot.delete_message(user_id, user_state.message_id)
            except Exception as e:
                logging.error(f"Error deleting message: {e}")
        logging.info(f"Tried to delete previous message for user {user_id}")