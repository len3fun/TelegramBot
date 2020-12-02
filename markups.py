from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import db_controller
from ids import DRINK_ID, BURGER_ID, SHAURMA_ID, PIZZA_ID, ROLL_ID

my_orders = KeyboardButton('Мои заказы')
my_cart = KeyboardButton('Моя корзина')
undo = KeyboardButton('Отменить')
back = KeyboardButton('Назад')
menu_button = KeyboardButton('Меню')
rolls_button = KeyboardButton('Роллы')
burgers_button = KeyboardButton('Бургеры')
pizzas_button = KeyboardButton('Пицца')
shaurma_button = KeyboardButton('Шаурма')
drink_button = KeyboardButton('Напитки')
checkout = KeyboardButton('Оформить заказ')
clear_cart_button = KeyboardButton('Очистить корзину')
main_menu_markup = KeyboardButton('В главное меню')


def generate_undo_markup():
    """Маркап для отмены."""
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(undo)
    return markup


def generate_no_comment_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    no_comment = KeyboardButton('Без комментария')
    markup.add(no_comment)
    markup.add(undo, back)
    return markup


def generate_back_undo_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(back, undo)
    return markup


def generate_cart_markup(user_id):
    markup = None
    count_of_dishes_in_cart = len(db_controller.get_dishes_from_user_cart(user_id))
    if count_of_dishes_in_cart == 0:
        markup = generate_start_markup()
    elif count_of_dishes_in_cart > 0:
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add(checkout, clear_cart_button, main_menu_markup)
    return markup


def generate_start_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(menu_button)
    markup.add(checkout)
    markup.add(my_cart, my_orders)
    return markup


def generate_menu_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(burgers_button, rolls_button, pizzas_button, shaurma_button, drink_button, back)
    return markup


def generate_confirm_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    agree_yes = KeyboardButton('Да')
    agree_no = KeyboardButton('Нет')
    markup.add(agree_yes, agree_no, back)
    return markup


def generate_category_markup(category_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if category_id == BURGER_ID:
        markup.add(burgers_button)
    elif category_id == ROLL_ID:
        markup.add(rolls_button)
    elif category_id == PIZZA_ID:
        markup.add(pizzas_button)
    elif category_id == SHAURMA_ID:
        markup.add(shaurma_button)
    elif category_id == DRINK_ID:
        markup.add(drink_button)
    return markup


def generate_dish_markup(dish_id):
    """Создание маркапа для блюда."""
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    data = f"add_to_cart{dish_id}"
    markup.add(InlineKeyboardButton("В корзину", callback_data=data))
    return markup
