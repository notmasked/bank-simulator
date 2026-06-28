import hashlib
accounts = []
account_file = "Bank Simulator/account data/accounts.txt"
class Account:
    def __init__(self, number, name, pin, balance):
        self.num = int(number)
        self.name = name
        self.pin = pin
        self.bal = int(balance)

    def deposit(self, amount):
        if amount <= 0:
            print("Please enter a valid amount.")
        else:
            self.bal += amount
            print(f"${amount} has been successfully deposited to your account {self.num}.")
            updatedata()

    def withdraw(self, amount):
        if amount <= 0:
            print("Please enter a valid amount.")
        else:
            if amount <= self.bal:
                self.bal -= amount
                print(f"${amount} has been successfully withdrawn from your account {self.num}")
                updatedata()
            else:
                print("Insufficient funds.")

    def checkbal(self):
        print(f"Your current balance is ${self.bal}.")

    def transfer(self, accnum, amount):
        if amount <= 0:
            print("Please enter a valid amount.")
        else:
            if amount > self.bal:
                print("Insufficient funds. Please try a lower amount.")
            elif accnum == self.num:
                print("You cannot transfer money to yourself.")
            else:
                for acc in accounts:
                    if acc.num == accnum:
                        acc.bal += amount
                        self.bal -= amount
                        print(f"${amount} has been successfully sent to {acc.name}.")
                        updatedata()
                        break
                else:
                    print("Account number is invalid. Please try again")
            
def updatedata():
    with open(account_file, "w") as f:
        for acc in accounts:
            f.write(f"{acc.num},{acc.name},{acc.pin},{acc.bal}\n")

def hashpin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def main():
    print("■■■■■■■■■■■■■■■■■■■■")
    print("■-Welcome to bank!-■")
    print("■■■■■■■■■■■■■■■■■■■■")
    print("1. Login\n2. Register\n3. Exit")
    try:
        choice = int(input("Enter: "))
    except ValueError:
        print("Please enter a number.")
        return
    if choice == 1:
        login()
    elif choice == 2:
        register()
    elif choice == 3:
        exit()
    else:
        print("Please enter a valid input.")
        return

def login():
    print('-----------------------------')
    print("Please enter your account number below to login.")
    try:
        number = int(input("Enter: "))
    except ValueError:
        print("Please enter a number.")
        return
    found = False
    for acc in accounts:
        if number == acc.num:
            found = True
            print('-----------------------------')
            print(f"Welcome {acc.name}!, please enter your PIN below.")
            pin = input("Enter: ")
            hashedpin = hashpin(pin)
            if hashedpin == acc.pin:
                print('-----------------------------')
                print(f"Successfully logged in as {acc.name}.")
                mainmenu(acc)
                break
            else:
                print("Wrong PIN. Please try again.")
                return
    if not found:
        print("User not found. Please enter a valid account number.")
        return       
    
def register():
    while True:
        print('-----------------------------')
        print("Welcome to our bank where we provide the best user experience.")
        print('-----------------------------')
        name = input("Please enter your first name: ")
        if len(accounts) == 0:
            newnum = 1001
        else:
            newnum = (accounts[-1]).num + 1
        temppin = input("Set a 4 digit pin: ")
        if not (temppin.isdigit() and len(temppin) == 4):
            print("Your pin is invalid, please try again with a 4 digit pin.")
            break
        confirmedpin = input("Confirm your pin: ")
        if temppin == confirmedpin:
            newhashedpin = hashpin(confirmedpin)
            with open(account_file, "a") as f:
                f.write(f"{newnum},{name},{newhashedpin},0\n")
            accounts.append(Account(newnum,name,newhashedpin,0))
            print(f"Welcome {name} to our bank!, your account has been successfully created.")
            print(f"Your account number is {newnum}.")
            print("You may login now.")
            break
        else:
            print("Both pins do not match. Please try again.")
            return

def mainmenu(acc):
    while True:
        print("■■■■■■■■■■■■■")
        print("■-Main Menu-■")
        print("■■■■■■■■■■■■■")
        print("1. Check balance\n2. Deposit money\n3. Withdraw money\n4. Transfer money\n5. Logout")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            print("Please enter a number.")
            return
        if choice == 1:
            print('-----------------------------')
            acc.checkbal()
            print('-----------------------------')
        elif choice == 2:
            print('-----------------------------')
            try:
                amount = int(input("Enter amount you wish to deposit (in $): "))
            except ValueError:
                print("Please enter a number.")
                return
            print('-----------------------------')
            acc.deposit(amount)
            print('-----------------------------')
        elif choice == 3:
            print('-----------------------------')
            try:
                amount = int(input("Enter amount you wish to withdraw (in $): "))
            except ValueError:
                print("Please enter a number.")
                return
            print('-----------------------------')
            acc.withdraw(amount)
            print('-----------------------------')
        elif choice == 4:
            print('-----------------------------')
            try:
                accnum = int(input("Enter account number of receiver: "))
            except ValueError:
                print("Please enter a number.")
                return
            try:
                amount = int(input("Enter the amount you want to transfer: "))
            except ValueError:
                print("Please enter a number.")
                return
            print('-----------------------------')
            acc.transfer(accnum, amount)
            print('-----------------------------')
        elif choice == 5:
            print("Logging out...")
            return
        else:
            print("Invalid input. Please try again.")

with open(account_file) as f:
    for line in f:
        line = line.strip()
        data = line.split(",")
        acc = Account(data[0], data[1], data[2], data[3])
        accounts.append(acc)

while True:
    main()