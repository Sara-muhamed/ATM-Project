from typing import List, Dict, Any
from datetime import datetime


class ATM_User:
    def __init__(self, accounts=None):
        self.accounts = accounts if accounts else []

    @classmethod
    def from_dict(cls, data):
        return cls(accounts=data["accounts"])

    def to_dict(self):
        return {"accounts": self.accounts}

    def get_account(self, account_number):
        """Get account by account number."""
        for account in self.accounts:
            if account["account_number"] == account_number:
                return account
        return None

    def add_account(self, account_number, pin):
        """Add a new account with initial balance."""
        if self.get_account(account_number):
            return False, "❌ Account already exists."
        self.accounts.append({
            "account_number": account_number,
            "pin": pin,
            "balance": 0.0,
            "statements": [],
            "attempts_left": 3   
        })
        return True, "✅ Account created successfully."

    def deposit(self, account_number, amount):
        """Deposit money into an account."""
        account = self.get_account(account_number)
        if amount <= 0:
            return False, "❌ Deposit amount must be greater than 0."
        account["balance"] += amount
        self.add_statement(account_number, f"Deposit: ${amount:.2f}")
        return True, "✅ Deposit successful"

    def withdraw(self, account_number, amount):
        """Withdraw money from an account if balance allows."""
        account = self.get_account(account_number)
        if amount <= 0:
            return False, "❌ Withdrawal amount must be greater than 0."
        if amount > account["balance"]:
            return False, "❌ Insufficient funds. Cannot withdraw more than balance."
        account["balance"] -= amount
        self.add_statement(account_number, f"Withdrawal: ${amount:.2f}")
        return True, "✅ Withdrawal successful"

    def change_pin(self, account_number, old_pin, new_pin, confirm_pin):
        """Change account PIN with confirmation."""
        account = self.get_account(account_number)
        if old_pin != account["pin"]:
            return False, "❌ Old PIN is incorrect."
        if new_pin != confirm_pin:
            return False, "❌ PINs do not match."
        account["pin"] = new_pin
        self.add_statement(account_number, "PIN changed")
        return True, "✅ PIN changed successfully."

    def reset_attempts(self, account_number):
        """Reset login attempts for an account."""
        account = self.get_account(account_number)
        if account:
            account["attempts_left"] = 3
            return True, "✅ Attempts reset."
        return False, "❌ Account not found."

    def login(self, account_number, entered_pin):
        """Login to an account with account number and PIN."""
        account = self.get_account(account_number)
        if not account:
            return False, "❌ Account not found."

        # Check if account is blocked
        if account["attempts_left"] <= 0:
            return False, "🚫 Account blocked due to too many failed attempts."

        if entered_pin == account["pin"]:
            account["attempts_left"] = 3  # ✅ Reset attempts on successful login
            return True, "✅ Login successful"
        else:
            account["attempts_left"] -= 1
            return False, f"❌ Incorrect PIN. Attempts left: {account['attempts_left']}"
    def add_statement(self, account_number, text: str):
        """Add transaction history with timestamp (keep only last 5)."""
        account = self.get_account(account_number)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account["statements"].append(f"{timestamp} - {text}")
        if len(account["statements"]) > 5:
            account["statements"].pop(0)
       