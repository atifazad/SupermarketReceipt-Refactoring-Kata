import math
from model_objects import Offer, BundleOffer, Receipt, Discount
from enums import SpecialOfferType, BundleOfferType


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}
        self.bundle_offers = []

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def add_bundle_offer(self, offer_type, product_quantites, argument):
        self.bundle_offers.append(BundleOffer(offer_type, product_quantites, argument))

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            product = pq.product
            receipt.add_product(product, pq.quantity, self.catalog.unit_price(product))

        self.__handle_offers(the_cart, receipt)

        return receipt

    def product_with_name(self, name):
        return self.catalog.products.get(name, None)

    def __handle_offers(self, the_cart, receipt):   
        bundles_in_cart = self.__find_bundles_in_cart(the_cart)   
        for product in the_cart._product_quantities.keys():
            discount = self.__compute_discounts(product, the_cart, bundles_in_cart)
            if discount:
                receipt.add_discount(discount)

    def __compute_discounts(self, product, the_cart, bundles_in_cart):
        quantity = the_cart._product_quantities[product]
        discount = self.__compute_discount_for_bundles(product, quantity, the_cart, bundles_in_cart)
        if not discount:
            discount = self.__compute_discount_for_single_products(product, quantity)
        
        return discount

    def __compute_discount_for_single_products(self, product, quantity):
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

    def __compute_discount_for_bundles(self, product, quantity, the_cart, bundles_in_cart):
        max_discount = None
        for bundle in bundles_in_cart:
            if product in bundle.product_quantities.keys():
                if bundle.offer_type == BundleOfferType.TEN_PERCENT_DISCOUNT:
                    bundle_frequency = self.__get_frequency_of_bundle(the_cart, bundle)
                    discount = self.__compute_discount_for_x_percent_bundle_discount_offer(product, quantity, bundle, bundle_frequency)
                    if not max_discount or max_discount.discount_amount > discount.discount_amount:
                        max_discount = discount

        return max_discount

    def __get_frequency_of_bundle(self, the_cart, bundle_offer):
        frequencies = [quantity // bundle_offer.product_quantities[product] for product, quantity in the_cart._product_quantities.items() if product in bundle_offer.product_quantities.keys()]
        return min(frequencies)

    def __find_bundles_in_cart(self, the_cart):
        bundles_in_cart = []
        for bundle_offer in self.bundle_offers:
            if self.__bundle_exists_in_cart(the_cart, bundle_offer):
                bundles_in_cart.append(bundle_offer)

        return bundles_in_cart

    def __bundle_exists_in_cart(self, the_cart, bundle_offer):
        cart_products = the_cart._product_quantities.keys()
        bundle_products = bundle_offer.product_quantities.keys()
        is_match = True
        if len(cart_products) < len(bundle_products):
            is_match = False
        else:
            for bundle_product in bundle_products:
                if bundle_product not in cart_products \
                or the_cart._product_quantities[bundle_product] < bundle_offer.product_quantities[bundle_product]:
                    is_match = False
                    break

        return is_match

    def __compute_discount_for_X_for_amount_offer(self, product, quantity, X):
        offer = self.offers[product]
        quantity_as_int = int(quantity)
        number_of_x = math.floor(quantity_as_int / X)
        unit_price = self.catalog.unit_price(product)
        discounted_total = offer.argument * number_of_x + quantity_as_int % X * unit_price
        discount_amount = unit_price * quantity - discounted_total
        discount_description = f"{X} for {offer.argument}"
        return Discount(product, discount_description, -discount_amount)

    def __compute_discount_for_X_for_Y_offer(self, product, quantity, X, Y):
        quantity_as_int = int(quantity)
        number_of_x = math.floor(quantity_as_int / X)
        unit_price = self.catalog.unit_price(product)
        discounted_total = (number_of_x * Y * unit_price) + quantity_as_int % X * unit_price
        discount_amount =  unit_price * quantity - discounted_total
        discount_description = f"{X} for {Y}"
        return Discount(product, discount_description, -discount_amount)

    def __compute_discount_for_x_percent_discount_offer(self, product, quantity):
        offer = self.offers[product]
        unit_price = self.catalog.unit_price(product)
        discount_amount =  unit_price * quantity * offer.argument / 100.0
        discount_description = f"{offer.argument}% off"
        discount = Discount(product, discount_description, -discount_amount)
        return discount

    def __compute_discount_for_x_percent_bundle_discount_offer(self, product, quantity, bundle_offer, bundle_frequency):
        discount = None
        if product in bundle_offer.product_quantities.keys():
            unit_price = self.catalog.unit_price(product)
            discount_quantity = bundle_offer.product_quantities[product] * bundle_frequency
            discount_amount =  unit_price * discount_quantity * bundle_offer.argument / 100.0
            discount_description = f"{bundle_frequency}x{bundle_offer.argument}% bundle offer"
            discount = Discount(product, discount_description, -discount_amount)
        return discount
