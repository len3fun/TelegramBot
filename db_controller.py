from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from db import execute_selection_query, execute_change_query


def add_new_user(user_id: str, first_name: str, last_name: str, nickname: str) -> None:
    """Добавляет нового пользователя в базу данных."""
    try:
        query = f"INSERT INTO users (user_id, first_name, last_name, nickname)" \
                f" VALUES ({user_id}, '{first_name}', '{last_name}', '{nickname}') "
        execute_change_query(query)
    except UniqueViolation:
        pass


def add_new_order(user_id: str, order_text: str) -> None:
    """Добавление нового заказа в базу данных."""
    try:
        query = f"INSERT INTO orders(user_id, comment) values('{user_id}', '{order_text}')"
        execute_change_query(query)
    except ForeignKeyViolation:
        pass


def get_confirmed_user_orders(user_id: str) -> list:
    """Получение всех подтвержденных заказов пользователя user_id."""
    query = f"""select user_id, order_id, dish, price from(
                select user_id, order_id, cd.cart_id, dish_id from carts
                right join carts_dishes cd on carts.cart_id = cd.cart_id
                where user_id='{user_id}' and order_id is not null) as tmp
            left join dishes
            on tmp.dish_id=dishes.dish_id
            order by order_id;"""
    return execute_selection_query(query)


def get_count_of_dishes_for_confirmed_user_orders(user_id: str) -> list:
    """ Получения количества блюд для каждого подтвержденного заказа пользователя.
        Возвращает кортеж (Количество блюд, номер заказа).
    """
    query = f"""select count(order_id), order_id
                from (
                         select user_id, order_id, cd.cart_id, dish_id
                         from carts
                                  right join carts_dishes cd on carts.cart_id = cd.cart_id
                         where user_id = '{user_id}'
                           and order_id is not null) as tmp
                         left join dishes
                                   on tmp.dish_id = dishes.dish_id
                group by order_id
                order by order_id
            """
    return execute_selection_query(query)


def get_dishes_by_order_id(order_id: int) -> list:
    """Получает блюда и цены из заказа order_id."""
    query = f"""
            select dish, price
            from (
                     select user_id, dish_id, order_id
                     from carts
                              right join carts_dishes cd on carts.cart_id = cd.cart_id
                     where order_id = {order_id}) as tmp
                     left join dishes on tmp.dish_id = dishes.dish_id;
            
            """
    return execute_selection_query(query)


def get_products_and_prices_from_category(category_id: int) -> list:
    """Получение всех блюд и их цен из категории category_id."""
    query = f"SELECT dish, price, dish_id FROM dishes WHERE dishes.category_id={category_id}"
    return execute_selection_query(query)


def get_product_by_id(dish_id: int) -> list:
    """Получение всей информации по блюду с id = dish_id."""
    query = f"SELECT dish, price, category FROM " \
            f"dishes LEFT JOIN categories ON dishes.category_id = categories.category_id WHERE dish_id={dish_id}"
    return execute_selection_query(query)


def create_new_cart(user_id: str) -> None:
    """Создание новой корзины для пользователя с id = user_id."""
    query = f"INSERT INTO carts(user_id) VALUES ('{user_id}')"
    execute_change_query(query)


def add_dish_to_cart(cart_id: int, dish_id: int) -> None:
    """Добавление блюда в корзину."""
    query = f"INSERT INTO carts_dishes(cart_id, dish_id) VALUES ({cart_id}, {dish_id})"
    execute_change_query(query)


def get_dishes_from_user_cart(user_id: str) -> list:
    """Получение всех блюд из корзины пользователя с id = user_id."""
    query = f"""
    select dish, price, order_id 
    from (select user_id, dish, price, order_id
          from (select *
                from carts_dishes left join dishes
                on carts_dishes.dish_id = dishes.dish_id) as tmp
          right join carts
          on carts.cart_id = tmp.cart_id) as tmp2
    where user_id = '{user_id}' and order_id is null;
    """
    return execute_selection_query(query)


def get_cost_of_dishes_in_user_cart(user_id: str) -> list:
    """Получение стоимости всех блюд в козрине пользователя с id = user_id."""
    query = f"""
    select sum(price)
    from (select user_id, price, order_id
          from (select *
                from carts_dishes left join dishes
                on carts_dishes.dish_id = dishes.dish_id) as tmp
                right join carts
          on carts.cart_id = tmp.cart_id) as tmp2
    where user_id = '{user_id}' and order_id is null;
    """
    return execute_selection_query(query)


def get_not_confirmed_orders(user_id: str) -> list:
    """Получает неподтвержденные заказы пользователя."""
    query = f"select * from orders where user_id='{user_id}' and is_confirmed=false"
    return execute_selection_query(query)


def delete_not_confirmed_orders(user_id: str) -> None:
    """Удаляет все неподтвержденные заказы пользователя."""
    query = f"delete from orders where user_id='{user_id}' and is_confirmed=false"
    execute_change_query(query)


def create_new_order(user_id: str) -> None:
    """Создание нового заказа."""
    query = f"insert into orders(user_id) values('{user_id}')"
    execute_change_query(query)


def count_not_confirmed_orders(user_id: str) -> list:
    """Считает количество неподтвержденных заказов пользователя."""
    query = f"select count(*) from orders where user_id='{user_id}' and is_confirmed=false"""
    return execute_selection_query(query)


def get_not_confirmed_order_id(user_id: str) -> list:
    """Получает id неподтвержденного заказа пользователя."""
    query = f"select order_id from orders where user_id='{user_id}' and is_confirmed=false"""
    return execute_selection_query(query)


def add_user_id_to_order(user_id: str, order_id: int) -> None:
    """Добавляет user_id к заказу в базу данных."""
    query = f"update orders set user_id='{user_id}' where order_id={order_id}"
    execute_change_query(query)


def add_user_name_to_order(name: str, order_id: int) -> None:
    """Добавляет имя к заказу в базу данных."""
    query = f"update orders set  name='{name}' where order_id={order_id}"
    execute_change_query(query)


def add_telephone_number_to_order(telephone_number: str, order_id: int) -> None:
    """Добавляет номер телефона к заказу в базу данных."""
    query = f"update orders set telephone_number='{telephone_number}' where order_id={order_id}"
    execute_change_query(query)


def add_delivery_address_to_order(delivery_address: str, order_id: int) -> None:
    """Добавляет адрес к заказу в базу данных."""
    query = f"update orders set delivery_adress='{delivery_address}' where order_id={order_id}"
    execute_change_query(query)


def add_delivery_time_to_order(delivery_time: str, order_id: int) -> None:
    """Добавляет время доставки к заказу в базу данных."""
    query = f"update orders set delivery_time='{delivery_time}' where order_id={order_id}"
    execute_change_query(query)


def add_comment_to_order(comment: str, order_id: int) -> None:
    """Добавляет комментарий к заказу в базу данных."""
    query = f"update orders set comment='{comment}' where order_id={order_id}"
    execute_change_query(query)


def set_order_confirmed(order_id: int):
    """Подтверждает заказ в базе данных."""
    query = f"update orders set is_confirmed=true where order_id={order_id}"
    execute_change_query(query)


def connect_order_with_cart(order_id: int, cart_id: int) -> None:
    """Связывает корзину пользователя с заказом."""
    query = f"update carts set order_id={order_id} where cart_id={cart_id}"
    execute_change_query(query)


def get_cart_id(user_id: str) -> list:
    """Получает id корзины пользователя, которая не привязана к заказу."""
    query = f"select cart_id from carts where user_id='{user_id}' and order_id is null"
    return execute_selection_query(query)


def clear_user_cart(user_id: str) -> None:
    """Очищает корзину пользователя."""
    query = f"delete from carts where user_id='{user_id}' and order_id is null"
    execute_change_query(query)


def get_category_id_by_dish_id(dish_id: int) -> list:
    """Получает id категории по id блюда. Возвращает лист кортежей."""
    query = f"select category_id from dishes where dish_id={dish_id}"
    return execute_selection_query(query)
