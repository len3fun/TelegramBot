import logging
import telebot
import controller
from markups import generate_start_markup, generate_cart_markup, \
    generate_menu_markup, generate_dish_markup, \
    generate_category_markup


def main():
    try:
        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)
        token = controller.get_token_from_file()
        bot = telebot.TeleBot(token)

        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            logger.info(f"user_id: {message.from_user.id} click /start")
            msg = controller.welcome(message)
            bot.send_message(message.from_user.id, msg, reply_markup=generate_start_markup())

        @bot.message_handler(func=lambda message: message.text == "Меню")
        def menu(message):
            logger.info(f"user_id: {message.from_user.id} click Меню")
            msg = "Выберите категорию"
            bot.send_message(message.from_user.id, msg, reply_markup=generate_menu_markup())

        @bot.message_handler(func=lambda message: message.text == "Отменить")
        def undo(message):
            bot.send_message(message.from_user.id, 'Отменено', reply_markup=generate_start_markup())
            logger.info(f"user_id: {message.from_user.id} click Отменить")

        @bot.message_handler(func=lambda message: message.text == "Назад")
        def back(message):
            bot.send_message(message.from_user.id, 'Ок.', reply_markup=generate_start_markup())
            logger.info(f"user_id: {message.from_user.id} click Назад")

        @bot.message_handler(func=lambda message: message.text == 'Бургеры')
        def burgers(message):
            logger.info(f"user_id: {message.from_user.id} click Бургеры")
            msg = controller.get_burgers()
            bot.send_message(message.from_user.id, msg, reply_markup=generate_menu_markup())

        @bot.message_handler(func=lambda message: message.text == 'Роллы')
        def rolls(message):
            logger.info(f"user_id: {message.from_user.id} click Роллы")
            msg = controller.get_rolls()
            bot.send_message(message.from_user.id, msg, reply_markup=generate_menu_markup())

        @bot.message_handler(func=lambda message: message.text == 'Пицца')
        def pizzas(message):
            logger.info(f"user_id: {message.from_user.id} click Пицца")
            msg = controller.get_pizzas()
            bot.send_message(message.from_user.id, msg, reply_markup=generate_menu_markup())

        @bot.message_handler(func=lambda message: message.text == 'Шаурма')
        def shaurma(message):
            logger.info(f"user_id: {message.from_user.id} click Шаурма")
            msg = controller.get_shaurma()
            bot.send_message(message.from_user.id, msg, reply_markup=generate_menu_markup())

        @bot.message_handler(func=lambda message: message.text == 'Напитки')
        def drinks(message):
            logger.info(f"user_id: {message.from_user.id} click Напитки")
            msg = controller.get_drinks()
            bot.send_message(message.from_user.id, msg, reply_markup=generate_menu_markup())

        @bot.message_handler(func=lambda message: message.text == "Оформить заказ")
        def make_order(message):
            controller.init_order(message, bot)

        @bot.message_handler(func=lambda message: message.text == "Очистить корзину")
        def clear_cart(message):
            controller.clear_user_cart(message.from_user.id)
            bot.send_message(message.from_user.id, 'Ваша корзина очищена', reply_markup=generate_start_markup())

        @bot.message_handler(func=lambda message: message.text == 'Мои заказы')
        def my_orders(message):
            logger.info(f"user_id: {message.from_user.id} click Мои заказы")
            msg = controller.user_orders(message.from_user.id)
            bot.send_message(message.from_user.id, msg, reply_markup=generate_start_markup())

        @bot.message_handler(func=lambda message: message.text == 'Моя корзина')
        def my_cart(message):
            msg = controller.my_cart(message)
            bot.send_message(message.from_user.id, msg, reply_markup=generate_cart_markup(message.from_user.id))

        @bot.message_handler(func=lambda message: message.text == 'В главное меню')
        def to_main_menu(message):
            bot.send_message(message.from_user.id, 'Ок!', reply_markup=generate_start_markup())

        @bot.callback_query_handler(func=lambda message: True)
        def callback_query(message):
            msg = controller.callback_keyboard_handler(message)
            bot.answer_callback_query(message.id, msg)

        @bot.message_handler(func=lambda message: message.content_type == 'text' and message.text.startswith('/dish'))
        def dish(message):
            msg = controller.dish_handler(message)
            dish_id = controller.get_dish_id_from_message(message)
            category_id = controller.get_category_id_by_dish_id(dish_id)
            bot.send_message(message.from_user.id, "Типа фото", reply_markup=generate_category_markup(category_id))
            bot.send_message(message.from_user.id, msg, reply_markup=generate_dish_markup(dish_id))

        @bot.message_handler(func=lambda message: message.content_type == 'text')
        def handle_text(message):
            """Обработка текста, который не является командой."""
            msg = "Вы ввели несуществующую команду. Попробуйте еще раз."
            bot.send_message(message.from_user.id, msg, reply_markup=generate_start_markup())

        @bot.message_handler(func=lambda message: message.content_type not in ["text"])
        def handle_not_text_messages(message):
            """Обработка отправки не текста."""
            msg = "Некорректный ввод. Доступны только текстовые комманды."
            bot.send_message(message.from_user.id, msg, reply_markup=generate_start_markup())

        bot.polling()
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
