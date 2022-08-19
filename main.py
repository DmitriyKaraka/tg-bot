import logging

import telebot
from pydantic import parse_obj_as

from core import settings
from client import Client
from schemas import (
    LineItem,
    CreateOrder,
    Product,
    Order,
    Shipping,
    ShippingItem,
    Billing,
)
from templates import get_product_keyboard

telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

client = Client(
    settings.API_HOST,
    settings.CLIENT_KEY,
    settings.CLIENT_SECRET,
)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, "Привет, мир!")


@bot.message_handler(commands=["catalog"])
def send_catalog(message: telebot.types.Message):
    chat_id = message.chat.id
    response = client.get("products").json()
    products = parse_obj_as(list[Product], response)
    for product in products:
        bot.send_message(
            chat_id,
            f"Товар: {product.name}, цена: {product.price}, <a href='{product.images[0].src}'> &#8205; </a>",
            parse_mode="HTML",
            reply_markup=get_product_keyboard(product.id),
        )


@bot.callback_query_handler(func=lambda q: "order_" in q.data)
def order_handler(query: telebot.types.CallbackQuery):
    chat_id = query.message.chat.id
    product_id = query.data.split("_")[1]
    line_item = LineItem(product_id=product_id, quantity=1)
    shipping_item = ShippingItem(product_id=product_id, quantity=1)
    billing_info = Billing(
        first_name=query.from_user.first_name,
        last_name=query.from_user.last_name,
        address_1=query.from_user.id,
        city="San Francisco",
        country="US",
        email="john.doe@example.com",
        phone="(555) 555-5555",
    )
    shipping_info = Shipping(
        first_name=query.from_user.first_name,
        last_name=query.from_user.last_name,
        address_1=query.from_user.id,
        city="San Francisco",
        country="US",
        email="john.doe@example.com",
        phone="(555) 555-5555",
    )
    order = CreateOrder(
        billing=billing_info,
        shipping=shipping_info,
        line_items=[line_item],
        shipping_lines=[shipping_item],
    )

    order_json = order.json()

    response = client.post("orders", data=order_json)

    created_order = parse_obj_as(Order, response.json())

    bot.send_message(
        chat_id,
        f"Ваш заказ успешно создан! Номер заказа: {created_order.number}",
    )


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
