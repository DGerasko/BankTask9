from accounts import Client, Account, CreditAccount, SavingAccount

if __name__ == '__main__':

    first_Client = Client("Ivan", "Ivanov", 20)
    first_acc = Account(first_Client)
    first_acc.deposit(10000)
    first_acc.deposit(10000)
    first_acc.withdrawal(5000)
    first_acc.print_transactions()

    second_acc = SavingAccount(first_Client)
    second_acc.deposit(10000)
    print(second_acc.my_balance())
    print(second_acc.my_interest())
    second_acc.print_transactions()

    third_acc = CreditAccount(first_Client)
    print(third_acc.my_loan_limit())
    third_acc.withdrawal(third_acc.my_loan_limit())
    third_acc.print_transactions()
