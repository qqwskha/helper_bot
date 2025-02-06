# src/bot.py
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
from src.config import (FEEDBACK_CHANNEL_ID, PRACTICAL_WORKS, ADMIN_ID)
from src.main_menu import MainMenu
from src.order_manager import OrderManager
from .titles_mapping import TITLES_MAPPING, REVERSED_TITLES_MAPPING
from src.user_state import UserState

# Логирование
logging.basicConfig(level=logging.INFO)


class TelegramBot:
    def __init__(self, api_token, payment_token):
        self.bot = Bot(token=api_token)
        self.dp = Dispatcher(self.bot)
        self.dp.middleware.setup(LoggingMiddleware())
        self.user_states = {}  # Хранение состояний пользователей
        self.feedback_messages = {}  # Хранение обратной связи
        self.order_manager = OrderManager(payment_token)
        self.main_menu = MainMenu(self.bot, self.dp, self.user_states)

    def start(self):
        self.main_menu.register_handlers()

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            user_id = message.from_user.id
            self.user_states[user_id] = UserState()
            await self.main_menu.send_main_menu(user_id, message.from_user.first_name)
            logging.info(f"Handled /start command for user {user_id}")

        @self.dp.message_handler(commands=['info'])
        async def info(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /info without starting the bot")
                return
            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_info(user_id)
            logging.info(f"Handled /info command for user {user_id}")

        @self.dp.message_handler(commands=['prices'])
        async def prices(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /prices without starting the bot")
                return
            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_prices(user_id)
            logging.info(f"Handled /prices command for user {user_id}")

        @self.dp.message_handler(commands=['help'])
        async def help_command(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /help without starting the bot")
                return
            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_help(user_id)
            logging.info(f"Handled /help command for user {user_id}")

        @self.dp.message_handler(commands=['search_work'])
        async def search_work(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /search_work without starting the bot")
                return
            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_disciplines_menu(user_id)
            logging.info(f"Handled /search_work command for user {user_id}")

        @self.dp.message_handler(commands=['feedback'])
        async def feedback(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /feedback without starting the bot")
                return
            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_feedback_request(user_id)
            logging.info(f"Handled /feedback command for user {user_id}")

        @self.dp.message_handler(commands=['get_chat_id'])
        async def get_chat_id(message: types.Message):
            chat_id = message.chat.id
            await message.answer(f"ID текущего чата: {chat_id}")
            logging.info(f"Sent chat ID {chat_id} to user {message.from_user.id}")

        @self.dp.message_handler(
            lambda message: message.text and message.from_user.id in self.user_states and self.user_states[
                message.from_user.id].state == "awaiting_feedback"
        )
        async def handle_feedback(message: types.Message):
            user_id = message.from_user.id
            feedback_text = message.text

            # Сохраняем сообщение
            self.feedback_messages[user_id] = feedback_text

            await message.answer("Спасибо за ваше сообщение! Мы обязательно рассмотрим его.")
            logging.info(f"Handled feedback message from user {user_id}")

            # Сбрасываем состояние
            self.user_states[user_id].state = None

        @self.dp.message_handler(commands=['admin_feedback'])
        async def admin_feedback(message: types.Message):
            user_id = message.from_user.id

            # Проверяем, что команда вызвана администратором
            if user_id != ADMIN_ID:
                await message.answer("У вас нет прав для выполнения этой команды.")
                return

            if not self.feedback_messages:
                await message.answer("Нет новых сообщений.")
                return

            # Формируем список сообщений с кликабельными user_id
            feedback_list = "Список сообщений:\n\n"
            for user_id, feedback_text in self.feedback_messages.items():
                # Создаем кликабельную ссылку для user_id
                feedback_list += f"ID пользователя: `{user_id}` ([нажмите для копирования](tg://user?id={user_id}))\n"
                feedback_list += f"Текст: {feedback_text}\n\n"

            # Отправляем список администратору с Markdown форматированием
            await message.answer(feedback_list, parse_mode="Markdown")
            logging.info(f"Sent feedback list to admin {user_id}")

        @self.dp.message_handler(commands=['answer'])
        async def answer(message: types.Message):
            user_id = message.from_user.id

            # Проверяем, что команда вызвана администратором
            if user_id != ADMIN_ID:
                await message.answer("У вас нет прав для выполнения этой команды.")
                return

            try:
                # Разбираем аргументы команды
                args = message.get_args().split()
                target_user_id = int(args[0])
                response_text = " ".join(args[1:])
            except Exception as e:
                await message.answer("Неверный формат команды. Используйте: /answer <user_id> <текст>")
                logging.error(f"Error parsing /answer command: {e}")
                return

            try:
                # Отправляем ответ пользователю
                await self.bot.send_message(target_user_id, response_text)
                await message.answer(f"Сообщение отправлено пользователю с ID {target_user_id}.")
                logging.info(f"Sent response to user {target_user_id} from admin {user_id}")
            except BotBlocked:
                await message.answer(f"Пользователь с ID {target_user_id} заблокировал бота.")
                logging.error(f"User {target_user_id} blocked the bot.")
            except Exception as e:
                await message.answer(f"Не удалось отправить сообщение пользователю с ID {target_user_id}.")
                logging.error(f"Error sending message to user {target_user_id}: {e}")

        @self.dp.message_handler(
            lambda message: message.chat.id == FEEDBACK_CHANNEL_ID and message.reply_to_message and message.reply_to_message.text.startswith(
                "Новое сообщение от пользователя")
        )
        async def answer_feedback(message: types.Message):
            try:
                # Логируем текст сообщения для отладки
                logging.info(f"Reply message text: {message.reply_to_message.text}")

                # Извлекаем user_id
                if "(ID: " not in message.reply_to_message.text:
                    logging.error("Invalid feedback message format")
                    await message.answer("Не удалось извлечь ID пользователя из сообщения.")
                    return

                user_id = int(message.reply_to_message.text.split("(ID: ")[1].split("):")[0])
                logging.info(f"Extracted user_id: {user_id}")

                # Форматируем текст ответа с префиксом
                admin_response = f"Ответ от администратора:\n{message.text}"

                # Отправляем ответ пользователю
                await self.bot.send_message(user_id, admin_response)
                await message.answer(f"Сообщение отправлено пользователю с ID {user_id}.")
            except BotBlocked:
                logging.error(f"User {user_id} blocked the bot.")
                await message.answer(f"Пользователь с ID {user_id} заблокировал бота.")
            except Exception as e:
                logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
                await message.answer(f"Не удалось отправить сообщение пользователю с ID {user_id}.")

        @self.dp.message_handler(commands=['search'])
        async def search(message: types.Message):
            user_id = message.from_user.id

            # Проверяем, что пользователь начал работу с ботом
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} tried to use /search without starting the bot")
                return

            # Удаляем предыдущее сообщение
            await self.main_menu.delete_previous_message(user_id)

            # Запрашиваем у пользователя поисковый запрос
            await message.answer("Введите ключевое слово для поиска:")
            self.user_states[user_id].state = "awaiting_search_query"
            logging.info(f"Sent search request to user {user_id}")

        @self.dp.message_handler(
            lambda message: message.text and message.from_user.id in self.user_states and self.user_states[
                message.from_user.id].state == "awaiting_search_query"
        )
        async def handle_search_query(message: types.Message):
            user_id = message.from_user.id
            query = message.text.lower()  # Приводим запрос к нижнему регистру

            # Выполняем поиск
            results = []
            for discipline, practical_types in PRACTICAL_WORKS.items():
                # Ищем по ключу или значению в дисциплинах
                if query in discipline.lower() or query in TITLES_MAPPING.get(discipline, "").lower():
                    original_name = TITLES_MAPPING.get(discipline, discipline)  # Полное название
                    key_name = REVERSED_TITLES_MAPPING.get(original_name, discipline)  # Ключ
                    results.append((key_name, original_name))  # Сохраняем пару (ключ, значение)

                for practical_type, variants in practical_types.items():
                    # Ищем по ключу или значению в типах работ
                    if query in practical_type.lower() or query in TITLES_MAPPING.get(practical_type, "").lower():
                        original_name = TITLES_MAPPING.get(practical_type, practical_type)  # Полное название
                        key_name = REVERSED_TITLES_MAPPING.get(original_name, practical_type)  # Ключ
                        # Добавляем приписку "Практическая работа - (название)"
                        display_name = f"Практическая работа - ({original_name})"
                        results.append((key_name, display_name))

                    for variant, data in variants.items():
                        # Ищем по ключу или значению в вариантах
                        if query in variant.lower() or query in TITLES_MAPPING.get(variant, "").lower():
                            original_name = TITLES_MAPPING.get(variant, variant)  # Полное название
                            key_name = REVERSED_TITLES_MAPPING.get(original_name, variant)  # Ключ
                            results.append((key_name, original_name))

            # Формируем результат
            if results:
                keyboard = InlineKeyboardMarkup(row_width=1)
                for key_name, display_name in results[:10]:  # Первые 10 результатов
                    # Создаем кнопку с текстом "ключ (значение)"
                    button_text = f"{display_name}"
                    keyboard.add(InlineKeyboardButton(button_text, callback_data=f"select_{key_name}"))
                await message.answer("Выберите из найденных:", reply_markup=keyboard)
            else:
                await message.answer("Ничего не найдено.")

            # Сбрасываем состояние
            self.user_states[user_id].state = None
            logging.info(f"Handled search query '{query}' for user {user_id}")

        from .titles_mapping import TITLES_MAPPING, REVERSED_TITLES_MAPPING

        @self.dp.callback_query_handler(lambda query: query.data.startswith("select_"))
        async def handle_search_result(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use select_ callback without starting the bot")
                return

            # Извлекаем ключ из callback_data
            key = query.data.split("_", 1)[1]

            # Преобразуем ключ, если он находится в TITLES_MAPPING
            practical_key = REVERSED_TITLES_MAPPING.get(key, key)

            # Находим соответствующие данные в PRACTICAL_WORKS
            found = False
            for discipline, practical_types in PRACTICAL_WORKS.items():
                for practical_type, variants in practical_types.items():
                    # Проверяем, является ли ключ типом работы
                    if practical_key == practical_type:
                        # Сохраняем состояние пользователя
                        self.user_states[user_id].discipline = discipline
                        self.user_states[user_id].practical_type = practical_type

                        # Переходим к выбору вариантов
                        await self.main_menu.delete_previous_message(user_id)
                        await self.main_menu.send_variants_menu(user_id, practical_type)
                        await query.answer()
                        logging.info(f"Handled search result for practical type '{practical_key}' for user {user_id}")
                        found = True
                        break

                    # Проверяем, является ли ключ вариантом
                    for variant, data in variants.items():
                        if practical_key == variant:
                            # Сохраняем состояние пользователя
                            self.user_states[user_id].discipline = discipline
                            self.user_states[user_id].practical_type = practical_type
                            self.user_states[user_id].variant = variant

                            # Отправляем изображение-пример
                            image_path = data.get("image")
                            if not image_path or not isinstance(image_path, str):
                                logging.error(f"Image path is missing or invalid for variant '{variant}'")
                                await query.message.answer(
                                    "Извините, изображение не найдено. Пожалуйста, свяжитесь с администратором.")
                                await query.answer()
                                return

                            try:
                                with open(image_path, "rb") as image:
                                    await self.main_menu.delete_previous_message(user_id)
                                    message = await query.message.answer_photo(
                                        image,
                                        caption="Вот пример для выбранного варианта. Подтвердите ваш выбор.",
                                        reply_markup=self.main_menu.get_confirmation_keyboard(practical_type, variant),
                                    )
                                    self.user_states[user_id].message_id = message.message_id
                                    found = True
                            except FileNotFoundError as e:
                                logging.error(f"File not found: {e}")
                                await query.message.answer(
                                    "Извините, изображение не найдено. Пожалуйста, свяжитесь с администратором.")
                                await query.answer()
                                return

            if not found:
                await query.message.answer(
                    "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова.")
                await query.answer()
                logging.error(f"Key '{key}' not found in PRACTICAL_WORKS")
                return

            await query.answer()
            logging.info(f"Handled search result for key '{key}' for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data.startswith("disc_"))
        async def select_discipline(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use disc_ callback without starting the bot")
                return
            discipline = query.data.split("_", 1)[1]
            self.user_states[user_id].discipline = discipline
            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_practical_types_menu(user_id, discipline)
            await query.answer()
            logging.info(f"Handled disc_ callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data.startswith("pr_"))
        async def select_practical_type(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use pr_ callback without starting the bot")
                return

            practical_type = query.data.split("_", 1)[1]
            self.user_states[user_id].practical_type = practical_type

            # Логируем состояние пользователя
            logging.info(f"User {user_id} selected practical type: {practical_type}")

            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_variants_menu(user_id, practical_type)
            await query.answer()
            logging.info(f"Handled pr_ callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data.startswith("var_"))
        async def select_variant(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use var_ callback without starting the bot")
                return

            variant = query.data.split("_", 1)[1]
            self.user_states[user_id].variant = variant

            # Отправляем изображение-пример
            discipline = self.user_states[user_id].discipline
            practical_type = self.user_states[user_id].practical_type
            variant_data = PRACTICAL_WORKS[discipline][practical_type][variant]
            image_path = variant_data["image"]

            try:
                with open(image_path, "rb") as image:
                    await self.main_menu.delete_previous_message(user_id)
                    message = await query.message.answer_photo(
                        image,
                        caption="Вот пример для выбранного варианта. Подтвердите ваш выбор.",
                        reply_markup=self.main_menu.get_confirmation_keyboard(practical_type, variant),
                    )
                    self.user_states[user_id].message_id = message.message_id
            except FileNotFoundError as e:
                logging.error(f"File not found: {e}")
                await query.message.answer("Извините, изображение не найдено. Пожалуйста, свяжитесь с администратором.")
                await query.answer()
            logging.info(f"Handled var_ callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data == "confirm_choice")
        async def confirm_choice(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use confirm_choice callback without starting the bot")
                return
            await self.confirm_order(user_id)
            await query.answer()
            logging.info(f"Handled confirm_choice callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data.startswith("back_to_practicals_"))
        async def back_to_practicals(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use back_to_practicals callback without starting the bot")
                return
            discipline = self.user_states[user_id].discipline
            practical_type = query.data.split("_")[-1]  # Извлекаем тип практической работы
            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_practical_types_menu(user_id, discipline)
            await query.answer()
            logging.info(f"Handled back_to_practicals callback for user {user_id}")

        @self.dp.callback_query_handler(lambda query: query.data.startswith("back_to_variants_"))
        async def back_to_variants(query: types.CallbackQuery):
            user_id = query.from_user.id
            if user_id not in self.user_states:
                await query.message.answer("Пожалуйста, начните с команды /start.")
                await query.answer()
                logging.info(f"User {user_id} tried to use back_to_variants callback without starting the bot")
                return

            # Извлекаем полный тип практической работы
            practical_type = "_".join(query.data.split("_")[3:])  # Все части после "back_to_variants_"
            discipline = self.user_states[user_id].discipline

            # Проверяем, что discipline и practical_type существуют в PRACTICAL_WORKS
            if discipline not in PRACTICAL_WORKS or practical_type not in PRACTICAL_WORKS[discipline]:
                await query.message.answer("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте снова.")
                logging.error(f"Invalid discipline or practical_type: {discipline}, {practical_type}")
                return

            await self.main_menu.delete_previous_message(user_id)
            await self.main_menu.send_variants_menu(user_id, practical_type)
            await query.answer()
            logging.info(f"Handled back_to_variants callback for user {user_id}")

        @self.dp.pre_checkout_query_handler(lambda query: True)
        async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
            await self.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

        @self.dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
        async def successful_payment(message: types.Message):
            user_id = message.from_user.id
            user_state = self.user_states[user_id]
            # Получаем пути к файлам из структуры данных
            discipline = user_state.discipline
            practical_type = user_state.practical_type
            variant = user_state.variant
            files = PRACTICAL_WORKS[discipline][practical_type][variant]["files"]
            # Отправляем все три файла
            for file_path in files:
                with open(file_path, "rb") as file:
                    await message.answer_document(file)
            await message.answer("Все файлы отправлены! Спасибо за покупку.")
            logging.info(f"Handled successful payment for user {user_id}")

        @self.dp.message_handler()
        async def unknown_command(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.user_states:
                await message.answer("Пожалуйста, начните с команды /start.")
                logging.info(f"User {user_id} sent an unknown command without starting the bot")
                return
            await message.answer("Неизвестная команда. Пожалуйста, используйте одну из доступных команд.")
            logging.info(f"User {user_id} sent an unknown command")

        executor.start_polling(self.dp, skip_updates=True)



    async def confirm_order(self, user_id):
        user_state = self.user_states[user_id]
        if not user_state.is_complete():
            await self.bot.send_message(user_id, "Пожалуйста, выберите все параметры перед подтверждением заказа.")
            logging.info(f"User {user_id} tried to confirm order without completing selection")
            return
        discipline = user_state.discipline
        practical_type = user_state.practical_type
        variant = user_state.variant
        variant_data = PRACTICAL_WORKS[discipline][practical_type][variant]
        price = variant_data["price"]
        order_details = (
            f"Вы выбрали:\n"
            f"Дисциплина: {discipline}\n"
            f"Тип практической работы: {practical_type}\n"
            f"Вариант: {variant}\n"
            f"Стоимость: {price} рублей\n"
            f"Оплатить?"
        )
        invoice_data = self.order_manager.create_invoice(user_id, order_details, price)
        try:
            await self.bot.send_invoice(**invoice_data)
            logging.info(f"Sent invoice to user {user_id}")
        except Exception as e:
            logging.error(f"Error sending invoice to user {user_id}: {e}")
            await self.bot.send_message(user_id, "Произошла ошибка при создании счета. Пожалуйста, попробуйте позже.")