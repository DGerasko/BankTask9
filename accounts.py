import consts
import datetime as dt

# -------------- utilities functions --------------- #


def now():
    return dt.datetime.now()


def year_diff_from_now(year):
    return now().year - year


def add_years(d, years):
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return dt.datetime(d.year + years, 3, 1)  # feb 29 -> march 1


# -------------- Exceptions --------------- #

class InvalidWithdrawalException(Exception):
    """Not enough money on this account"""
    pass


# -------------- Classes --------------- #
class Transaction:
    def __init__(self, transaction_type, date, transfer_funds):
        self.transaction_type = transaction_type    # deposit, withdrawal
        self.date = date
        self.transfer_funds = transfer_funds        # how much funds will be transferred

    def __str__(self):
        return (f"transaction type = {self.transaction_type}\t"
                f"date = {self.date}\t"
                f"transfer funds = {self.transfer_funds}")


class Client:
    accounts = []

    def __init__(self, name, surname, age):
        self.__name = name
        self.__surname = surname
        self.__age = age


class Account:
    __transactions = []
    __money = 0

    def __init__(self, client, acc_type="deposit"):
        self.client = client        # info about the customer
        self.acc_type = acc_type    # deposit, saving, credit
        self.client.accounts.append(self)

    def my_balance(self):
        return self.__money

    def deposit(self, money):
        self.__money += money
        self.__transactions.append(Transaction("deposit", now(), money))

    def withdrawal(self, money):
        try:
            if self.__money < money:
                raise InvalidWithdrawalException
            else:
                self.__money -= money

        except InvalidWithdrawalException:
            print("Not enough money on this account")

        self.__transactions.append(Transaction("withdrawal", now(), money))

    def my_transactions(self):
        return self.__transactions

    def print_transactions(self):
        for tr in self.__transactions:
            print(tr)


class CreditAccount(Account):
    __limit = consts.BASE_CREDIT_LIMIT          # default limit
    __credit_rate = consts.BASE_CREDIT_RATE     # default credit rate
    __money = 0
    __transactions = []

    def __init__(self, client):
        super().__init__(client, "credit")

    def my_loan_limit(self):
        return self.__limit

    def my_loan_rate(self):
        return self.__credit_rate

    def withdrawal(self, money):
        try:
            if self.__money + self.__limit < money:
                raise InvalidWithdrawalException
            else:
                self.__money -= money

        except InvalidWithdrawalException:
            print("Not enough money on this account")

        self.__transactions.append(Transaction("withdrawal", now(), money))


class SavingAccount(Account):
    __interest = consts.BASE_INTEREST_RATE  # default interest rate
    __last_upd_interest_date = now()        # interest will be paid once per year
    __money = 0
    __transactions = []

    def __init__(self, client):
        super().__init__(client, "saving")

    # check if client should get interest money
    def update_balance(self):
        year_diff = year_diff_from_now(self.__last_upd_interest_date.year)
        if year_diff >= 1:
            self.__money *= pow(1 + self.__interest, year_diff)
            add_years(self.__last_upd_interest_date, year_diff)

    def my_balance(self):
        self.update_balance()
        super().my_balance()

    def withdrawal(self, money):
        self.update_balance()
        super().withdrawal(money)

    def my_interest(self):
        return self.__interest

    def deposit(self, money):
        self.update_balance()
        self.__last_upd_interest_date = now()
        super().deposit(money)
