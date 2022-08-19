from telebot import types


def get_product_keyboard(product_id: int) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    order_btn = types.InlineKeyboardButton(
        "Заказать",
        callback_data=f"order_{product_id}",
    )
    markup.add(order_btn)
    return markup
