from typing import List, Dict, Any
from datetime import datetime

class ATM_clear:
    def __init__(self, pin="0000", balance=0.0, attempts_left=3, statements=None):
        self.pin = pin
        self.balance = balance
        self.attempts_left = attempts_left
        self.statements = statements or []  # Keep a history of transactions

    def login(self, entered_pin):
        """Check if entered PIN is correct and handle attempts."""
        if self.attempts_left <= 0:
            return False, "❌ Account locked. Too many failed attempts."
        
        if entered_pin == self.pin:
            self.reset_attempts()
            return True, "✅ Login successful"
        else:
            self.attempts_left -= 1
            if self.attempts_left <= 0:
                return False, "❌ Account locked. Too many failed attempts."
            return False, f"❌ Incorrect PIN. Attempts left: {self.attempts_left}"

    def reset_attempts(self):
        """Reset login attempts back to 3."""
        self.attempts_left = 3

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            return False, "❌ Deposit amount must be greater than 0."
        self.balance += amount
        self.add_statement(f"Deposit: ${amount:.2f}")
        return True, "✅ Deposit successful"

    def withdraw(self, amount):
        """Withdraw money if balance allows."""
        if amount <= 0:
            return False, "❌ Withdrawal amount must be greater than 0."
        if amount > self.balance:
            return False, "❌ Insufficient funds. Cannot withdraw more than balance."
        self.balance -= amount
        self.add_statement(f"Withdrawal: ${amount:.2f}")
        return True, "✅ Withdrawal successful"

    def add_statement(self, text: str):
        """Add transaction history with timestamp (keep only last 5)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.statements.append(f"{timestamp} - {text}")
        if len(self.statements) > 5:
            self.statements.pop(0)

    def reset(self):
        """Reset account data (used when pressing reset)."""
        self.pin = "0000"
        self.balance = 0.0
        self.statements = []
        self.attempts_left = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary (for session saving)."""
        return {
            "pin": self.pin,
            "balance": self.balance,
            "statements": self.statements,
            "attempts_left": self.attempts_left
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        """Create ATM object from dictionary (for session loading)."""
        return cls(
            pin=d.get("pin", "0000"),
            balance=d.get("balance", 0.0),
            statements=d.get("statements", []),
            attempts_left=d.get("attempts_left", 3)
        )

    def change_pin(self,old_pin:str, new_pin: str, confirm_pin: str):
        """Change account PIN with confirmation."""
        if old_pin!= self.pin:
            return False, "❌ Old PIN is incorrect."

        if new_pin != confirm_pin:
            return False, "❌ PINs do not match."
        self.pin = new_pin
        self.add_statement("PIN changed")
        return True, "✅ PIN changed successfully."
