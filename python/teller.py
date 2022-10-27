import math
from model_objects import Offer, Receipt, Discount
from enums import SpecialOfferType


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            product = pq.product
            receipt.add_product(product, pq.quantity, self.catalog.unit_price(product))

        self.handle_offers(the_cart, receipt)

        return receipt

    def handle_offers(self, the_cart, receipt):
        for product in the_cart._product_quantities.keys():
            quantity = the_cart._product_quantities[product]
            discount = self.__compute_discount(product, quantity)
            if discount:
                receipt.add_discount(discount)

    def product_with_name(self, name):
        return self.catalog.products.get(name, None)

    def __compute_discount(self, product, quantity):
        discount = None
        if product in self.offers.keys():
            offer = self.offers[product]
            quantity_as_int = int(quantity)
            if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                discount = self.__compute_discount_for_X_for_Y_offer(product, quantity, 3, 2)

            elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT and quantity_as_int >= 2:
                discount = self.__compute_discount_for_X_for_amount_offer(product, quantity, 2)

            elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                discount = self.__compute_discount_for_X_for_amount_offer(product, quantity, 5)
            
            elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                discount = self.__compute_discount_for_x_percent_discount_offer(product, quantity)
        
        return discount

    def __compute_discount_for_X_for_amount_offer(self, product, quantity, X):
        offer = self.offers[product]
        quantity_as_int = int(quantity)
        number_of_x = math.floor(quantity_as_int / X)
        unit_price = self.catalog.unit_price(product)
        discounted_total = offer.argument * number_of_x + quantity_as_int % X * unit_price
        discount_amount = unit_price * quantity - discounted_total
        return Discount(product, str(X) + " for " + str(offer.argument), -discount_amount)

    def __compute_discount_for_X_for_Y_offer(self, product, quantity, X, Y):
        quantity_as_int = int(quantity)
        number_of_x = math.floor(quantity_as_int / X)
        unit_price = self.catalog.unit_price(product)
        discounted_total = (number_of_x * Y * unit_price) + quantity_as_int % X * unit_price
        discount_amount =  unit_price * quantity - discounted_total
        return Discount(product, str(X) + " for " + str(Y), -discount_amount)

    def __compute_discount_for_x_percent_discount_offer(self, product, quantity):
        offer = self.offers[product]
        unit_price = self.catalog.unit_price(product)
        discount_amount =  unit_price * quantity * offer.argument / 100.0
        discount = Discount(product, str(offer.argument) + "% off", -discount_amount)
        return discount
    