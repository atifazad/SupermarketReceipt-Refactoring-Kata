from enum import Enum


class Product:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class ProductQuantity:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4

class Offer:
    def __init__(self, offer_type, product, argument):
        self.offer_type = offer_type
        self.product = product
        self.argument = argument


class Discount:
    def __init__(self, product, description, discount_amount):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount


class ReceiptItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = quantity * price


class Receipt:
    def __init__(self):
        self._items = []
        self._discounts = []

    @property
    def total_price(self):
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]

    def add_product(self, product, quantity, price):
        self._items.append(ReceiptItem(product, quantity, price))

    def add_discount(self, discount):
        self._discounts.append(discount)
