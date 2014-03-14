"""
    Simplified bank operations
    Absolutely no error checking, use it at your own risk!

    Jay S. Liu
    jay.s.liu@gmail.com
    Mar. 14, 2014

    Usage: Python Bank_server.py port#

"""

import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer

class BankAccount(object):
    """Bank account class
        supports min. operations, no exception is thrown, no error is checked
    """
    def __init__(self, name, initial_balance=0,rate=0.01):
        self.name = name
        self.balance = initial_balance
        self.rate = rate
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        self.balance -= amount
    def set_rate(self, rate):
        self.rate = rate
    def overdrawn(self):
        return self.balance < 0
    def compound(self):
        self.balance *= (1.0 + self.rate)
    def get_balance(self):
        return self.balance
    def get_info(self):
        return self.name, self.balance, self.rate


class Bank():
    """Bank class
        data for accounts are stored in a dictionary +
        operations
    """

    def __init__(self):
        self.data_store = {}
        self.next_account_number = 1000
        self.hide_listAll = False

    def listall(self):
        if not self.hide_listAll:
            for k, v in self.data_store.items():
                print "ID %s: (%s, %s, %s)" %(k, v.name, v.balance, v.rate)
        return self.data_store

    def new_account(self, name, ib, rate):
        data = BankAccount(name, ib, rate)
        aid = self.next_account_number
        self.data_store[str(aid)] = data
        self.next_account_number += 1
        return aid

    def delete_account(self, aid):
        del self.data_store[aid]

    def deposit(self, aid, amount):
        data = self.data_store[aid]
        data.deposit(amount)
        self.data_store[aid] = data

    def withdraw(self, aid, amount):
        data = self.data_store[aid]
        data.withdraw(amount)
        self.data_store[aid] = data

    def get_balance(self, aid):
        data = self.data_store[aid]
        return data.get_balance()

    def compound(self, aid):
        data = self.data_store[aid]
        data.compound()
        self.data_store[aid] = data

def main():
    server = SimpleXMLRPCServer(("", int(sys.argv[1])), allow_none=True)
    server.register_introspection_functions()
    server.register_instance(Bank())
    print "Server ready"
    server.serve_forever()


if __name__ == "__main__":
    main()

