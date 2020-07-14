# from collections import deque
import numpy as np
import heapq
import time
import warnings


class Order:

    DEFAULT_DICT = {"UID": None, "Price": None, "Type": None}

    def __init__(self, price, id):
        """Actually write this class"""
        if price == 0:
            raise Exception("Price cannot be zero")
        self.price = price
        self.id = id
        self.time = time.time()

    def update_execution_time(self):
        """Sets the execution time of an order that has been filled"""


class Buy(Order):
    def __init__(self, price, id):
        super().__init__(price, id)  # include args.
        # self.type = "buy"


class Sell(Order):
    """docstring for  Put."""

    def __init__(self, price, id):
        super().__init__(price, id)
        # self.type = "sell"


class Heap:
    def __init__(self, key=lambda x: x.price):
        self.key = key
        self._data = []
        self.index = 0

    def push(self, item: Order):
        # pushing a triple touple to the heap of key(item), index, and item
        heapq.heappush(self._data, (self.key(item), self.index, item))
        self.index += 1

    def pop(self):
        if self.size() <= 0:
            return
        self.index -= 1
        return heapq.heappop(self._data)[2]

    def get_max(self):
        if self.size() <= 0:
            return
        return heapq.nlargest(1, self._data)[0]

    def get_min(self):
        if self.size() <= 0:
            return
        return heapq.nsmallest(1, self._data)[0]

    def size(self):
        return len(self._data)


class Market:
    """docstring for BookADT."""

    def __init__(self):

        # the buy book has maximal ordering
        # to do this we invert the object price which allows us to pop the MAXIMAL value
        # our Heap class has the ability to get min and max but only can pop min
        self.buy_book = Heap(key=lambda x: 1 / x.price)
        self.sell_book = Heap(key=lambda x: x.price)
        self.register = []

    def find_order(self):
        """
        Searches through the buy and sell book max/min and finds an order to execute
        returns a tuple of (Buy,Sell) if no order can be made returns False
        """
        if self.buy_book.size() == 0 or self.sell_book.size() == 0:
            # order cannot be created
            # print("booksize zero")
            return False
        # now that we have decent sizes lets look for an order
        max_buy_price = self.buy_book.get_min()[2].price
        min_sell_price = self.sell_book.get_min()[2].price

        if max_buy_price - min_sell_price >= 0:
            # this means that an order can be created:
            execution = (self.buy_book.pop(), self.sell_book.pop())
            self.register.append(execution)
            return execution

        return False

    def add_order_from_dict(self, dict_input: dict):
        order_dict = Order.DEFAULT_DICT
        # now that we have the default let us overwrite any values
        for key in dict_input.keys():
            order_dict[key] = dict_input[key]
        # now we check for Nones as that is what the Default_DICT starts with:
        for key in order_dict:
            if order_dict[key] is None:
                raise Exception(
                    "dict_input did not sucessfully overwrite Order.DEFAULT_DICT order_dict is: {0} dict_input is {1}".format(
                        order_dict, dict_input
                    )
                )
        # now let us construct an order and return it:
        print(order_dict)
        if order_dict["Type"] == "buy":
            order = Buy(order_dict["Price"], order_dict["UID"])
        elif order_dict["Type"] == "sell":
            order = Sell(order_dict["Price"], order_dict["UID"])
        else:
            raise Exception(
                "order_dict['Type']: {0} is not of value 'buy' or 'sell'".format(
                    order_dict["Type"]
                )
            )
        return self.add_order(order)

    def add_order(self, order: Order):
        if isinstance(order, Buy):
            print("adding buy order")
            self.buy_book.push(order)
        # otherwise it is a sell order
        elif isinstance(order, Sell):
            print("adding sell order")
            self.sell_book.push(order)
        # now we run and check for matches
        # commenting out the line below because we can do this manually
        # self.find_executions()

    def find_executions(self):
        execution_list = []
        while True:
            execution = self.find_order()
            if execution is False:
                break
            execution_list.append(execution)
            print("Execution Found!")

        return execution_list


# market = Market()
# b = {'UID': 1, 'Price': 30, 'Type': 'buy'}
# s = {'UID': 2, 'Price': 10, 'Type': 'sell'}
# result = market.add_order_from_dict(b)
# result = market.add_order_from_dict(s)
# print(result)
