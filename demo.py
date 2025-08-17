# run_core_demo.py
from Login import ATM_clear
atm = ATM_clear()
print("initial:", atm.to_dict())

ok, msg = atm.deposit(200)
print(ok, msg, "balance:", atm.balance)

ok, msg = atm.withdraw(50)
print(ok, msg, "balance:", atm.balance)

ok, msg = atm.change_pin("1234", "1234")
print(ok, msg, "pin:", atm.pin)

ok, msg = atm.login("1234")
print(ok, msg)
