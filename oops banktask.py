class BankAccount:
    def __init__(self, account_holder, initial_balance):
        self._account_holder = account_holder
        self.__balance = initial_balance
        self._active = True
        self._cheque_book_requested = False
    
    def check_balance(self):
        if not self._active:
            return "Account is frozen"
        return f"Balance: ${self.__balance}"
    
    def deposit(self, amount):
        if not self._active:
            return "Account is frozen. Cannot deposit."
        if amount <= 0:
            return "Deposit amount must be positive"
        self.__balance += amount
        return f"Deposited ${amount}. New balance: ${self.__balance}"
    
    def request_cheque_book(self):
        if not self._active:
            return "Account is frozen"
        if self._cheque_book_requested:
            return "Cheque book already requested"
        self._cheque_book_requested = True
        return "Cheque book request approved"
    
    def freeze_account(self):
        if not self._active:
            return "Account already frozen"
        self._active = False
        return "Account frozen successfully"
    
    def unfreeze_account(self):
        if self._active:
            return "Account already active"
        self._active = True
        return "Account unfrozen successfully"
    
    def __update_balance(self, amount):
        self.__balance += amount
    
    def get_balance(self):
        return self.__balance
    
    def is_active(self):
        return self._active


class SavingsAccount(BankAccount):
    def __init__(self, account_holder, initial_balance, pin):
        super().__init__(account_holder, initial_balance)
        self.__pin = pin
        self.__atm_card_requested = False
        self.__daily_withdrawal_limit = 1000
        self.__daily_withdrawn = 0
    
    def __verify_pin(self, entered_pin):
        return self.__pin == entered_pin
    
    def check_balance(self, pin):
        if not self._active:
            return "Account is frozen"
        if not self.__verify_pin(pin):
            return "Invalid PIN"
        return f"Balance: ${self.get_balance()}"
    
    def withdraw(self, amount, pin):
        if not self._active:
            return "Account is frozen"
        if not self.__verify_pin(pin):
            return "Invalid PIN"
        if amount <= 0:
            return "Withdrawal amount must be positive"
        if amount > self.get_balance():
            return "Insufficient funds"
        if amount + self.__daily_withdrawn > self.__daily_withdrawal_limit:
            return "Daily withdrawal limit exceeded"
        
        self._BankAccount__update_balance(-amount)
        self.__daily_withdrawn += amount
        return f"Withdrew ${amount}. New balance: ${self.get_balance()}"
    
    def deposit(self, amount, pin):
        if not self._active:
            return "Account is frozen. Cannot deposit."
        if not self.__verify_pin(pin):
            return "Invalid PIN"
        if amount <= 0:
            return "Deposit amount must be positive"
        
        self._BankAccount__update_balance(amount)
        return f"Deposited ${amount}. New balance: ${self.get_balance()}"
    
    def request_atm_card(self):
        if not self._active:
            return "Account is frozen"
        if self.__atm_card_requested:
            return "ATM card already requested"
        self.__atm_card_requested = True
        return "ATM card request approved"
    
    def reset_daily_withdrawal(self):
        self.__daily_withdrawn = 0


class BusinessAccount(BankAccount):
    def __init__(self, business_name, initial_balance):
        super().__init__(business_name, initial_balance)
        self.__overdraft_limit = 5000
        self.__loan_limit = 10000
        self.__current_loan = 0
    
    def check_balance(self):
        return super().check_balance()
    
    def withdraw(self, amount):
        if not self._active:
            return "Account is frozen"
        if amount <= 0:
            return "Withdrawal amount must be positive"
        
        available_funds = self.get_balance() + self.__overdraft_limit
        if amount > available_funds:
            return "Insufficient funds (exceeds overdraft limit)"
        
        self._BankAccount__update_balance(-amount)
        return f"Withdrew ${amount}. New balance: ${self.get_balance()}"
    
    def request_loan(self, amount):
        if not self._active:
            return "Account is frozen"
        if amount <= 0:
            return "Loan amount must be positive"
        if amount > self.__loan_limit:
            return "Loan amount exceeds limit"
        if self.__current_loan > 0:
            return "Existing loan must be paid first"
        
        self.__current_loan = amount
        self._BankAccount__update_balance(amount)
        return f"Loan of ${amount} approved. New balance: ${self.get_balance()}"


def run_complete_test_flow():
    print("=== BANK CUSTOMERWISE COMPLETE TEST FLOW ===\n")
    
    print("1. Creating Savings Account...")
    savings = SavingsAccount("Narendra", 1000, 1234)
    print("   Savings account created for Narendra with initial balance $1000\n")

    print("2. Check balance with correct PIN (1234):")
    print(f"   {savings.check_balance(1234)}\n")
    
    print("3. Check balance with wrong PIN (9999):")
    print(f"   {savings.check_balance(9999)}\n")
    
    print("4. Withdraw $200 with correct PIN:")
    print(f"   {savings.withdraw(200, 1234)}\n")
    
    print("5. Withdraw $900 (exceeds daily limit):")
    print(f"   {savings.withdraw(900, 1234)}\n")
    
    print("6. Withdraw $100 with wrong PIN:")
    print(f"   {savings.withdraw(100, 9999)}\n")
    
    print("7. Deposit $500 with correct PIN:")
    print(f"   {savings.deposit(500, 1234)}\n")
    
    print("8. Deposit $100 with wrong PIN:")
    print(f"   {savings.deposit(100, 9999)}\n")
    
    print("9. Request ATM card:")
    print(f"   {savings.request_atm_card()}\n")
    
    print("10. Request ATM card again:")
    print(f"    {savings.request_atm_card()}\n")
    
    print("11. Request cheque book:")
    print(f"    {savings.request_cheque_book()}\n")
    
    print("12. Request cheque book again:")
    print(f"    {savings.request_cheque_book()}\n")
    
    print("13. Freeze account:")
    print(f"    {savings.freeze_account()}\n")
    
    print("14. Withdraw after freeze:")
    print(f"    {savings.withdraw(100, 1234)}\n")
    
    print("15. Unfreeze account:")
    print(f"    {savings.unfreeze_account()}\n")
    
    print("16. Create Business Account object:")
    business = BusinessAccount("Tech Corp", 5000)
    print("   Business account created for Tech Corp with initial balance $5000\n")
    
    print("17. Check balance:")
    print(f"    {business.check_balance()}\n")
    
    print("18. Withdraw money within overdraft limit:")
    print(f"    {business.withdraw(7000)}\n")
    
    print("19. Withdraw money above overdraft limit:")
    print(f"    {business.withdraw(4000)}\n")
    
    print("20. Request loan within limit:")
    print(f"    {business.request_loan(5000)}\n")
    
    print("21. Request loan above limit:")
    print(f"    {business.request_loan(15000)}\n")
    
    print("22. Request cheque book:")
    print(f"    {business.request_cheque_book()}\n")
    
    print("=== TEST FLOW COMPLETED ===")


if __name__ == "__main__":
    run_complete_test_flow()
    
