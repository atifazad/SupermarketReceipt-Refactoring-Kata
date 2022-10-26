from model_objects import Offer, Receipt

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
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            receipt.add_product(p, quantity, unit_price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt

    def product_with_name(self, name):
        return self.catalog.products.get(name, None)