from typing import Optional

from pydantic import BaseModel


class ProductImage(BaseModel):
    id: int
    src: str


class Product(BaseModel):
    id: int
    name: str
    slug: str
    permalink: str
    description: str
    short_description: str
    sku: str
    price: str
    images: list[ProductImage]


class ShippingItem(BaseModel):
    method_id: str = "flat_rate"
    total: str = "10.00"


class Billing(BaseModel):
    first_name: str
    last_name: str
    address_1: str
    address_2: str = ""
    city: str
    state: str = "Moscow"
    postcode: str = "101010"
    country: str
    email: Optional[str]
    phone: Optional[str]


class Shipping(BaseModel):
    first_name: str
    last_name: str
    address_1: str
    address_2: str = ""
    city: str
    state: str = "Moscow"
    email: Optional[str]
    phone: Optional[str]
    postcode: str = "101010"
    country: str


class LineItem(BaseModel):
    product_id: int
    quantity: int


class OrderBase(BaseModel):
    billing: Billing
    shipping: Shipping
    payment_method: str = "bacs"
    set_paid: bool = True
    line_items: list[LineItem]
    shipping_lines: list[ShippingItem]


class CreateOrder(OrderBase):
    pass


class Order(OrderBase):
    id: int
    number: int
