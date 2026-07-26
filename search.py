class SearchEngine:

    def __init__(self, engine):

        self.engine = engine

    def find_order(self, order_number):

        for order in self.engine.orders:

            if order.order_number == order_number:
                return order

        return None

    def find_customer(self, customer):

        results = []

        for order in self.engine.orders:

            if customer.lower() in order.customer.lower():
                results.append(order)

        return results

    def find_destination(self, destination):

        results = []

        for order in self.engine.orders:

            if destination.lower() in order.destination.lower():
                results.append(order)

        return results

    def find_product(self, product):

        results = []

        for order in self.engine.orders:

            if product.lower() in order.product.lower():
                results.append(order)

        return results