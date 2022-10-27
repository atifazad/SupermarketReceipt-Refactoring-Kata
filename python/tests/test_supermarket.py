import unittest

from approvaltests import verify

from model_objects import Product, ShoppingCart
from receipt_printer import ReceiptPrinter
from teller import Teller
from tests.fake_catalog import FakeCatalog
from enums import ProductUnit, SpecialOfferType, BundleOfferType


class SupermarketTest(unittest.TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()
        self.teller = Teller(self.catalog)
        self.the_cart = ShoppingCart()

        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.catalog.add_product(self.toothbrush, 0.99)
        self.toothpaste = Product("toothpaste", ProductUnit.EACH)
        self.catalog.add_product(self.toothpaste, 1.49)
        self.rice = Product("rice", ProductUnit.EACH)
        self.catalog.add_product(self.rice, 2.99)
        self.apples = Product("apples", ProductUnit.KILO)
        self.catalog.add_product(self.apples, 1.99)
        self.cherry_tomatoes = Product("cherry tomato box", ProductUnit.EACH)
        self.catalog.add_product(self.cherry_tomatoes, 0.69)

    def test_an_empty_shopping_cart_should_cost_nothing(self):
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_one_normal_item(self):
        self.the_cart.add_item(self.toothbrush)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_two_normal_items(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.rice)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_buy_two_get_one_free(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.toothbrush,
                                      self.catalog.unit_price(self.toothbrush))
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_buy_five_get_one_free(self):
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.the_cart.add_item(self.toothbrush)
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.toothbrush,
                                      self.catalog.unit_price(self.toothbrush))
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_loose_weight_product(self):
        self.the_cart.add_item_quantity(self.apples, 0.5)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount(self):
        self.the_cart.add_item(self.rice)
        self.teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, self.rice, 10.0)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_x_for_y_discount(self):
        self.the_cart.add_item(self.cherry_tomatoes)
        self.the_cart.add_item(self.cherry_tomatoes)
        self.teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, self.cherry_tomatoes, 0.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_five_for_y_discount(self):
        self.the_cart.add_item_quantity(self.apples, 5)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 5.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_five_for_y_discount_with_six(self):
        self.the_cart.add_item_quantity(self.apples, 6)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 5.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_five_for_y_discount_with_sixteen(self):
        self.the_cart.add_item_quantity(self.apples, 16)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 7.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_five_for_y_discount_with_four(self):
        self.the_cart.add_item_quantity(self.apples, 4)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 6.99)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount_on_bundle(self):
        self.the_cart.add_item_quantity(self.toothbrush, 1)
        self.the_cart.add_item_quantity(self.toothpaste, 1)
        bundle_offer_product_quantities = {
            self.toothbrush: 1,
            self.toothpaste: 1
        }
        self.teller.add_bundle_offer(BundleOfferType.TEN_PERCENT_DISCOUNT, bundle_offer_product_quantities, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount_on_bundle_no_match(self):
        self.the_cart.add_item_quantity(self.apples, 1.0)
        self.the_cart.add_item_quantity(self.rice, 1)
        bundle_offer_product_quantities = {
            self.toothbrush: 1,
            self.toothpaste: 1
        }
        self.teller.add_bundle_offer(BundleOfferType.TEN_PERCENT_DISCOUNT, bundle_offer_product_quantities, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount_on_bundle_with_too_few_items(self):
        self.the_cart.add_item_quantity(self.toothbrush, 1)
        self.the_cart.add_item_quantity(self.toothpaste, 1)
        bundle_offer_product_quantities = {
            self.toothbrush: 2,
            self.toothpaste: 2
        }
        self.teller.add_bundle_offer(BundleOfferType.TEN_PERCENT_DISCOUNT, bundle_offer_product_quantities, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount_on_bundle_with_extra_quantity(self):
        self.the_cart.add_item_quantity(self.toothbrush, 2)
        self.the_cart.add_item_quantity(self.toothpaste, 1)
        bundle_offer_product_quantities = {
            self.toothbrush: 1,
            self.toothpaste: 1
        }
        self.teller.add_bundle_offer(BundleOfferType.TEN_PERCENT_DISCOUNT, bundle_offer_product_quantities, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount_on_bundle_with_extra_items(self):
        self.the_cart.add_item_quantity(self.toothbrush, 1)
        self.the_cart.add_item_quantity(self.toothpaste, 1)
        self.the_cart.add_item_quantity(self.cherry_tomatoes, 0.5)
        bundle_offer_product_quantities = {
            self.toothbrush: 1,
            self.toothpaste: 1
        }
        self.teller.add_bundle_offer(BundleOfferType.TEN_PERCENT_DISCOUNT, bundle_offer_product_quantities, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount_on_bundle_with_multiples(self):
        self.the_cart.add_item_quantity(self.toothbrush, 3)
        self.the_cart.add_item_quantity(self.toothpaste, 5)
        bundle_offer_product_quantities = {
            self.toothbrush: 1,
            self.toothpaste: 1
        }
        self.teller.add_bundle_offer(BundleOfferType.TEN_PERCENT_DISCOUNT, bundle_offer_product_quantities, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_percent_discount_on_bundle_with_per_kilo_items(self):
        self.the_cart.add_item_quantity(self.apples, 2.0)
        self.the_cart.add_item_quantity(self.cherry_tomatoes, 3.0)
        bundle_offer_product_quantities = {
            self.apples: 1.0,
            self.cherry_tomatoes: 1.0
        }
        self.teller.add_bundle_offer(BundleOfferType.TEN_PERCENT_DISCOUNT, bundle_offer_product_quantities, 10)
        receipt = self.teller.checks_out_articles_from(self.the_cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))
