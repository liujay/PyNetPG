"""
    Simplified bank operations
    Absolutely no error checking, use it at your own risk!

    Jay S. Liu
    jay.s.liu@gmail.com
    Mar. 14, 2014

    Usage: python Bank_client.py http://Bank_server:port#
    
"""
import sys
import xmlrpclib

def main():

    s = xmlrpclib.ServerProxy(sys.argv[1], allow_none=True)

    def new_account():
        name = raw_input("name: ")
        ib = float(raw_input("initial balance: "))
        rate = float(raw_input("rate: "))
        aid = s.new_account(name, ib, rate)
        print "new account with number: %s" % aid

    def delete_account():
        aid = raw_input("account number: ")
        s.delete_account(aid)
        print "delete account with ID: %s" % aid

    def deposit():
        aid = raw_input("account number: ")
        amount = float(raw_input("amount: "))
        s.deposit(aid, amount)
        print "balance is: %s" % s.get_balance(aid)

    def withdraw():
        aid = raw_input("account number: ")
        amount = float(raw_input("amount: "))
        s.withdraw(aid, amount)
        print "balance is: %s" % s.get_balance(aid)

    def get_balance():
        aid = raw_input("account number: ")
        bl = s.get_balance(aid)
        print "balance is: %s" % bl

    def compound():
        aid = raw_input("account number: ")
        s.compound(aid)
        print "balance is: %s" % s.get_balance(aid)

    def quit():
        sys.exit(0)

    def listall():
        data = s.listall()
        if data:
            for k, v in data.items():
                print "ID %s: %s" % (k, v)
        else:
            print "no account info!"


    PROMPT = """    C. Create new account
    X. delete account
    D. Deposit
    W. Withdraw
    B. get Balance
    I. compounding
    E. Exit
    """

    """ simulate a switch statement
    """
    menu = {'C':new_account, 'X':delete_account, 'D': deposit,
            'W': withdraw, 'B': get_balance, 'I': compound, 'E': quit,
            'c':new_account, 'x':delete_account, 'd': deposit,
            'w': withdraw, 'b': get_balance, 'i': compound, 'e': quit,
            'l': listall }

    while True:
        print PROMPT
        choice = raw_input("Your choice: ")
        menu[choice]()

if __name__ == "__main__":
    main()

