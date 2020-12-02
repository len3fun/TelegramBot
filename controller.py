import re
import db_controller
from checkout_model import CheckoutModel
from ids import DRINK_ID, BURGER_ID, SHAURMA_ID, PIZZA_ID, ROLL_ID
from markups import generate_confirm_markup, generate_start_markup, generate_undo_markup, \
    generate_back_undo_markup, generate_no_comment_markup


def get_token_from_file() -> str:
    """Получение токена API."""
    with open('secret.key', 'r') as f:
        return f.read().strip()


def welcome(message) -> str:
    """Логика при команде /start. Возвращает сообщение ответа пользователю."""
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    nickname = message.from_user.username
    db_controller.add_new_user(user_id, first_name, last_name, nickname)
    return f"Hi, {first_name}!"


def make_menu_message(products, product_type: str) -> str:
    """Формирует сообщение с меню из категории category_id."""
    msg = f"{product_type}:\n\n"
    i = 1
    for product in products:
        msg += f"{i}) {product[0]}, Цена: {product[1]}. Подробнее о блюде или добавить в корзину: /dish{product[2]}\n\n"
        i += 1
    return msg


def get_burgers() -> str:
    """Логика при команде 'Бургеры'.
    Получает бургеры и цены из базы данных, формирует сообщение для ответа юзеру.
    """
    burgers = db_controller.get_products_and_prices_from_category(BURGER_ID)
    return make_menu_message(burgers, 'Бургеры')


def get_rolls() -> str:
    """Логика при команде 'Роллы'.
    Получает роллы и цены из базы данных, формирует сообщения для ответа юзеру.
    """
    rolls = db_controller.get_products_and_prices_from_category(ROLL_ID)
    return make_menu_message(rolls, 'Роллы')


def get_pizzas() -> str:
    """Логика при команде 'Пицца'.
    Получает роллы и цены из базы данных, формирует сообщения для ответа юзеру.
    """
    pizzas = db_controller.get_products_and_prices_from_category(PIZZA_ID)
    return make_menu_message(pizzas, 'Пицца')


def get_shaurma() -> str:
    """Логика при команде 'Шаурма'.
    Получает роллы и цены из базы данных, формирует сообщения для ответа юзеру.
    """
    shaurma = db_controller.get_products_and_prices_from_category(SHAURMA_ID)
    return make_menu_message(shaurma, 'Шаурма')


def get_drinks() -> str:
    """Логика при команде 'Напитки'.
    Получает роллы и цены из базы данных, формирует сообщения для ответа юзеру.
    """
    drinks = db_controller.get_products_and_prices_from_category(DRINK_ID)
    return make_menu_message(drinks, 'Напитки')


def get_category_id_by_dish_id(dish_id: int):
    """Получает id категории по id блюда."""
    return db_controller.get_category_id_by_dish_id(dish_id)[0][0]


def get_count_not_confirmed_orders(user_id: str) -> int:
    """Получает количество неподтвержденных заказов пользователя из списка кортежей и возвращает их число."""
    return db_controller.count_not_confirmed_orders(user_id)[0][0]


def get_not_confirmed_order_id(user_id: str):
    """Получает id неподтвержденного заказа пользователя."""
    return db_controller.get_not_confirmed_order_id(user_id)[0][0]


def handle_not_confirmed_orders(user_id: str) -> int:
    """Обработка неподтвержденных заказов пользователя. Возвращает нужный id заказа."""
    count_of_not_confirmed_orders = get_count_not_confirmed_orders(user_id)
    if count_of_not_confirmed_orders == 0:
        db_controller.create_new_order(user_id)
        return get_not_confirmed_order_id(user_id)
    if count_of_not_confirmed_orders == 1:
        return get_not_confirmed_order_id(user_id)
    if count_of_not_confirmed_orders > 1:
        db_controller.delete_not_confirmed_orders(user_id)
        db_controller.create_new_order(user_id)
        return get_not_confirmed_order_id(user_id)


def check_telephone_number_for_correctness(telephone_number: str):
    """Регулярка для проверки правильности ввода номера телефона."""
    pattern = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
    if re.fullmatch(pattern, telephone_number):
        return True
    else:
        return False


def init_order(message, bot) -> None:
    """Инициализация заказа."""
    if len(db_controller.get_cart_id(message.from_user.id)) > 0:
        order = CheckoutModel()
        order.set_user_id(message.from_user.id)
        bot.send_message(message.from_user.id, 'Как к вам обращаться?', reply_markup=generate_undo_markup())
        bot.register_next_step_handler(message, order_name_step, bot, order)
    else:
        msg = f"Чтобы оформить заказ необходимо добавить блюда в корзину. Сейчас ваша корзина пуста."
        bot.send_message(message.from_user.id, msg, reply_markup=generate_start_markup())


def order_name_step(message, bot, order: CheckoutModel) -> None:
    """Проуесс ввода имени пользователя."""
    if message.text == 'Отменить':
        bot.send_message(message.from_user.id, 'Отменено.', reply_markup=generate_start_markup())
        return
    order.set_name(message.text)
    msg = "Укажите ваш номер телефона. Допустимые форматы для ввода:\n" \
          "+71234567890\n+7 123 456 78 90\n" \
          "81234567890\n8 123 456 78 90"
    bot.send_message(message.from_user.id, msg, reply_markup=generate_back_undo_markup())
    bot.register_next_step_handler(message, order_telephone_number_step, bot, order)


def order_telephone_number_step(message, bot, order: CheckoutModel) -> None:
    """Процесс ввода пользователем номера телефона."""
    if message.text == 'Отменить':
        bot.send_message(message.from_user.id, 'Отменено.', reply_markup=generate_start_markup())
        return
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, "Как к вам обращаться?", reply_markup=generate_undo_markup())
        bot.register_next_step_handler(message, order_name_step, bot, order)
    else:
        telephone_number_is_correct = check_telephone_number_for_correctness(message.text)
        if telephone_number_is_correct:
            order.set_telephone_number(message.text)
            msg = f'Введите адрес доставки:'
            next_step = order_delivery_address_step
        else:
            msg = "Вы указали телефонный номер в неверном формате. Введите номер телефона еще раз."
            next_step = order_telephone_number_step
        bot.send_message(message.from_user.id, msg, reply_markup=generate_back_undo_markup())
        bot.register_next_step_handler(message, next_step, bot, order)


def order_delivery_address_step(message, bot, order: CheckoutModel) -> None:
    """Шаг ввода адреса доставки при заказе."""
    if message.text == 'Отменить':
        bot.send_message(message.from_user.id, 'Отменено.', reply_markup=generate_start_markup())
        return
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Введите ваш номер телефона:', reply_markup=generate_back_undo_markup())
        bot.register_next_step_handler(message, order_telephone_number_step, bot, order)
    else:
        order.set_delivery_address(message.text)
        bot.send_message(message.from_user.id, 'Введите время доставки:', reply_markup=generate_back_undo_markup())
        bot.register_next_step_handler(message, order_delivery_time_step, bot, order)


def order_delivery_time_step(message, bot, order: CheckoutModel) -> None:
    """Шаг ввода времени доставки при заказе."""
    if message.text == 'Отменить':
        bot.send_message(message.from_user.id, 'Отменено.', reply_markup=generate_start_markup())
        return
    if message.text == 'Назад':
        msg = f'Введите адрес доставки:'
        bot.send_message(message.from_user.id, msg, reply_markup=generate_back_undo_markup())
        bot.register_next_step_handler(message, order_delivery_address_step, bot, order)
    else:
        order.set_delivery_time(message.text)
        bot.send_message(message.from_user.id, 'Введите комментарий к заказу:',
                         reply_markup=generate_no_comment_markup())
        bot.register_next_step_handler(message, order_comment_step, bot, order)


def order_comment_step(message, bot, order: CheckoutModel) -> None:
    """Шаг ввода комментария при заказе."""
    if message.text == 'Отменить':
        bot.send_message(message.from_user.id, 'Отменено.', reply_markup=generate_start_markup())
        return
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Введите время доставки:', reply_markup=generate_back_undo_markup())
        bot.register_next_step_handler(message, order_delivery_time_step, bot, order)
    else:
        order.set_comment(message.text)
        msg = f"Ваш заказ введен верно?\n\n" + generate_order_text(message, order)
        bot.send_message(message.from_user.id, msg, reply_markup=generate_confirm_markup())
        bot.register_next_step_handler(message, order_confirm_step, bot, order)


def order_confirm_step(message, bot, order: CheckoutModel) -> None:
    """Шаг подтверждения заказа."""
    if message.text == 'Да':
        msg = "Новый заказ!\n\n" + generate_order_text(message, order)
        order.add_order_to_database()
        bot.send_message(-1001463502831, msg)
        bot.send_message(message.from_user.id, "Спасибо за заказ!", reply_markup=generate_start_markup())
    elif message.text == 'Нет':
        bot.send_message(message.from_user.id, "Заказ отменен.", reply_markup=generate_start_markup())
    elif message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Введите комментарий к заказу:',
                         reply_markup=generate_no_comment_markup())
        bot.register_next_step_handler(message, order_comment_step, bot, order)


def generate_order_text(message, order: CheckoutModel) -> str:
    """Генерирует текст с заказом и деталями о доставке."""
    dishes = db_controller.get_dishes_from_user_cart(message.from_user.id)
    dishes_text = transform_dishes_list_to_text(dishes)
    dishes_price = db_controller.get_cost_of_dishes_in_user_cart(message.from_user.id)[0][0]
    text = f"{dishes_text}\n" \
           f"Итого: {dishes_price}₽\n\n" \
           f"{str(order)}"
    return text


def user_orders(user_id: str) -> str:
    """Формирование сообщения с историей заказов пользователя."""
    orders = db_controller.get_confirmed_user_orders(user_id)
    msg = ""
    if len(orders) > 0:
        msg = 'История ваших заказов:\n\n'
        count_of_dishes = db_controller.get_count_of_dishes_for_confirmed_user_orders(user_id)
        i = 1
        for index in count_of_dishes:
            msg += f"Заказ {i}:\n"
            dishes = db_controller.get_dishes_by_order_id(index[1])
            for dish in dishes:
                msg += f"\t\t\t{dish[0]}, цена: {dish[1]}\n"
            i += 1

    elif len(orders) == 0:
        msg = 'У вас еще не было заказов.'

    return msg


def callback_keyboard_handler(message) -> str:
    """Обработчик для inline клавиатуры."""
    if message.data.startswith('add_to_cart'):
        dish_id = message.data[11:]
        add_dish_to_cart(message, dish_id)
        return "Добавлено"


def get_dish_id_from_message(message) -> int:
    """Получение id блюда из сообщения."""
    return int(message.text[5:])


def dish_handler(message) -> str:
    """Обработчик команды /dish."""
    dish_id = get_dish_id_from_message(message)
    dish_info = db_controller.get_product_by_id(dish_id)[0]
    msg = f"{dish_info[0]}\n\nКатегория: {dish_info[2]}\nЦена: {dish_info[1]} ₽\nОписание: В разработке"
    return msg


def add_dish_to_cart(message, dish_id: int) -> None:
    """Добавить блюдо в корзину."""
    cart_id = db_controller.get_cart_id(message.from_user.id)
    if len(cart_id) == 0:
        db_controller.create_new_cart(message.from_user.id)
        cart_id = db_controller.get_cart_id(message.from_user.id)
        db_controller.add_dish_to_cart(cart_id[0][0], dish_id)
    elif len(cart_id) == 1:
        db_controller.add_dish_to_cart(cart_id[0][0], dish_id)


def transform_dishes_list_to_text(dishes: list) -> str:
    """Преобразует список блюд, полученных из базы в текст."""
    text = ""
    i = 1
    for dish in dishes:
        text += f"{i}) {dish[0]}, цена: {dish[1]}₽\n"
        i += 1
    return text


def clear_user_cart(user_id: str) -> None:
    """"Очищает корзину пользователя."""
    db_controller.clear_user_cart(user_id)


def my_cart(message) -> str:
    """Формирование сообщения с корзиной пользователя."""
    dishes_in_cart = db_controller.get_dishes_from_user_cart(message.from_user.id)
    msg = ""
    if len(dishes_in_cart) == 0:
        msg = "Ваша корзина пуста."
    elif len(dishes_in_cart) > 0:
        msg = "Блюда в корзине:\n\n"
        msg += transform_dishes_list_to_text(dishes_in_cart)
        total_price = db_controller.get_cost_of_dishes_in_user_cart(message.from_user.id)
        msg += f"\nИтого: {total_price[0][0]}₽ \n"
    return msg
