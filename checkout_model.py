import db_controller
import controller


class CheckoutModel:
    """Модель для оформления заказа."""

    def __init__(self):
        self._user_id = ""
        self._name = ""
        self._telephone_number = ""
        self._delivery_address = ""
        self._delivery_time = ""
        self._comment = ""
        self._is_confirmed = False

    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_name(self, name):
        self._name = name

    def set_telephone_number(self, telephone_number):
        self._telephone_number = telephone_number

    def set_delivery_address(self, delivery_address):
        self._delivery_address = delivery_address

    def set_delivery_time(self, delivery_time):
        self._delivery_time = delivery_time

    def set_comment(self, comment):
        self._comment = comment

    def set_is_confirmed(self, is_confirmed: bool):
        self._is_confirmed = is_confirmed

    def add_order_to_database(self):
        order_id = controller.handle_not_confirmed_orders(self._user_id)
        cart_id = db_controller.get_cart_id(self._user_id)[0][0]
        db_controller.add_user_id_to_order(self._user_id, order_id)
        db_controller.add_user_name_to_order(self._name, order_id)
        db_controller.add_telephone_number_to_order(self._telephone_number, order_id)
        db_controller.add_delivery_address_to_order(self._delivery_address, order_id)
        db_controller.add_delivery_time_to_order(self._delivery_time, order_id)
        db_controller.add_comment_to_order(self._comment, order_id)
        db_controller.set_order_confirmed(order_id)
        db_controller.connect_order_with_cart(order_id, cart_id)

    def __str__(self):
        result = f"Имя: {self._name}\n" \
              f"Номер телефона: {self._telephone_number}\n"\
              f"Адрес доставки: {self._delivery_address}\n" \
              f"Время доставки: {self._delivery_time}\n" \
              f"Комментарий: {self._comment}\n"
        return result
