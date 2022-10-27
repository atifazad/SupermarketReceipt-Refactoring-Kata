from enums import ProductUnit

class ReceiptPrinter:

    def __init__(self, columns=40):
        self.columns = columns
  
    def print_receipt(self, receipt):
        result = ""
        for item in receipt.items:
            receipt_item = self.__print_receipt_item(item)
            result += receipt_item

        for discount in receipt.discounts:
            discount_presentation = self.__print_discount(discount)
            result += discount_presentation

        result += "\n"
        result += self.__print_total(receipt)
        return str(result)

    def __print_receipt_item(self, item):
        total_price_printed = self.__print_price(item.total_price)
        name = item.product.name
        line = self.__format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self.__print_price(item.price)} * {self.__print_quantity(item)}\n"
        return line

    def __format_line_with_whitespace(self, name, value):
        line = name
        whitespace_size = self.columns - len(name) - len(value)
        for i in range(whitespace_size):
            line += " "
        line += value
        line += "\n"
        return line

    def __print_price(self, price):
        return "%.2f" % price

    def __print_quantity(self, item):
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return '%.3f' % item.quantity

    def __print_discount(self, discount):
        name = f"{discount.description} ({discount.product.name})"
        value = self.__print_price(discount.discount_amount)
        return self.__format_line_with_whitespace(name, value)

    def __print_total(self, receipt):
        name = "Total: "
        value = self.__print_price(receipt.total_price)
        return self.__format_line_with_whitespace(name, value)
