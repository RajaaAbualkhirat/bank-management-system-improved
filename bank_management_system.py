# Bank management System

import pickle
import os

MIN_SAVING_BALANCE = 5000
MIN_CURRENT_BALANCE = 2000
START_ACCOUNT_NUMBER = 121000


class Customer:
    def __init__(self, account_number):
        self.name = input("Enter Name: ")
        self.account_type = input("Type of Account s/c?: ")
        self.balance = get_integer("Enter Amount: ")
        while True:
            if self.account_type == "s":
                if self.balance < MIN_SAVING_BALANCE:
                    print(f"Min {MIN_SAVING_BALANCE} required")
                    self.balance = get_integer("Please Enter amount again: ")
                else:
                    break
            if self.account_type == "c":
                if self.balance < MIN_CURRENT_BALANCE:
                    print(f"Min {MIN_CURRENT_BALANCE} required")
                    self.balance = get_integer("Please Enter amount again: ")
                else:
                    break
        self.account_number = account_number
        print("Your Account No. is:", self.account_number)

    def display_customer_info(self):
        print(
            "{:<15} {:<15} {:<15} {:<15}".format(
                self.account_number, self.name, self.account_type, self.balance
            )
        )


def get_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input, please enter a number.")


def create_account():
    try:
        bank_file = open("bank.bin", "rb")
        while True:
            customer = pickle.load(bank_file)
            last_account_number = customer.account_number
    except FileNotFoundError:
        last_account_number = START_ACCOUNT_NUMBER
    except EOFError:
        last_account_number = last_account_number + 1
        bank_file.close()
    bank_file = open("bank.bin", "ab")
    new_customer = Customer(last_account_number)
    pickle.dump(new_customer, bank_file)
    bank_file.close()


def view_all_accounts():
    try:
        bank_file = open("bank.bin", "rb")
        print(
            "{:<15} {:<15} {:<15} {:<15}".format(
                "Account No.", "Name", "Type", "Amount"
            )
        )
        while True:
            customer = pickle.load(bank_file)
            customer.display_customer_info()
    except FileNotFoundError:
        print("\nThere Are No Record")
    except EOFError:
        bank_file.close()


def find_customer(account_number):
    bank_file = open("bank.bin", "rb")

    try:
        while True:
            customer = pickle.load(bank_file)

            if customer.account_number == account_number:
                return customer
    except EOFError:
        return None

    finally:
        bank_file.close()


def update_customer_data(account_number, update_function):

    customer_found = False

    bank_file = open("bank.bin", "rb")
    temporary_file = open("tmp.bin", "wb")

    try:
        while True:
            customer = pickle.load(bank_file)

            if customer.account_number == account_number:
                customer_found = True
                update_function(customer)

            pickle.dump(customer, temporary_file)

    except EOFError:
        pass

    finally:
        bank_file.close()
        temporary_file.close()

    os.remove("bank.bin")
    os.rename("tmp.bin", "bank.bin")

    if not customer_found:
        print("Account not found")


def deposit_money():

    account_number = get_integer("Enter Bank Account: ")

    def add_balance(customer):
        deposit_amount = get_integer("Enter Deposit Amount: ")
        customer.balance += deposit_amount

    update_customer_data(account_number, add_balance)

    print("Operation completed.")


def withdraw_balance(customer):

    withdraw_amount = get_integer("Enter Withdraw Amount: ")

    if customer.account_type == "s":

        while customer.balance - withdraw_amount < MIN_SAVING_BALANCE:
            print(f"Saving Account Balance can't be below {MIN_SAVING_BALANCE}")
            withdraw_amount = get_integer("Enter Withdraw Amount: ")

    elif customer.account_type == "c":

        while customer.balance - withdraw_amount < MIN_CURRENT_BALANCE:
            print(f"Current Account Balance can't be below {MIN_CURRENT_BALANCE}")
            withdraw_amount = get_integer("Enter Withdraw Amount: ")

    customer.balance -= withdraw_amount


def withdraw_money():

    account_number = get_integer("Enter Bank Account: ")

    update_customer_data(account_number, withdraw_balance)


def update_account():

    account_number = get_integer("Enter Bank Account: ")

    def change_name(customer):
        customer.name = input("Update Name: ")

    update_customer_data(account_number, change_name)


def search_account():
    account_number = get_integer("Enter Bank Account: ")

    customer = find_customer(account_number)

    if customer:
        print("\nName:", customer.name)
        print("Account Type:", customer.account_type)
        print("Amount:", customer.balance)
        print("Account No.:", customer.account_number)
    else:
        print("Account not found")


def exit_program():
    print("Thank you for using the system.")


def main_menu():

    while True:

        print()
        print("What Do You Wanna Do")
        print("1. Create Account")
        print("2. View all Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Update")
        print("6. Search")
        print("7. Exit")

        choice = get_integer("Enter your choice: ")

        if choice == 1:
            create_account()

        elif choice == 2:
            view_all_accounts()

        elif choice == 3:
            deposit_money()

        elif choice == 4:
            withdraw_money()

        elif choice == 5:
            update_account()

        elif choice == 6:
            search_account()

        elif choice == 7:
            exit_program()
            break

        else:
            print("Invalid option")
            print("Try again")


title = "BANKING MANAGEMENT SYSTEM"
print(title.center(45, "*"))

main_menu()
