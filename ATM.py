import streamlit as st
st.set_page_config(page_title="ATM Machine", layout="centered")
class ATM:
  def __init__(self):
    self.defaults = {
            "screen": "welcome",
            "attempts_left": 3,
            "pin": "0000",
            "balance": 0.0,
            "statements": [],
        }
    for k, v in self.defaults.items():
         st.session_state.setdefault(k, v)

  def go(self, screen: str):
        st.session_state["screen"] = screen
        st.rerun()
  

  def welcome(self):
        st.title("🏦 Welcome to the ATM")
        if st.button("press to Login"):
            self.go("login")
    

  def login(self):
      
      if st.session_state.attempts_left <= 0:
            
            st.error("❌ You have reached the maximum number of attempts.")
            if st.button("Reset ATM"):
                self.logout()  
            return  
      st.subheader("Enter your PIN")
      st.info(f"Attempts left: {st.session_state.attempts_left}")
      entered_pin = st.text_input("Please enter your PIN:", max_chars=4,type="password",key="pin_input")
     
      if st.button("submit pin"):
        if entered_pin == st.session_state.pin:
            st.success("Login successful")
            st.session_state.attempts_left = 3
            self.go("menu")
            
        else:
            st.session_state.attempts_left -= 1
            self.go("login")
            
            
  def logout(self):
      st.session_state.screen = "welcome"
      st.session_state.attempts_left = 3    
      st.session_state.pin = "0000"
      st.session_state.balance = 0.0
      st.session_state.statements = []
      st.rerun()


  def display_menu(self):
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Withdraw"):
            self.go("withdraw")
        if st.button("Display Balance"):
            self.go("display_balance")
        if st.button("Deposit"):
            self.go("deposit")

    with col2:
        if st.button("Change PIN"):
            self.go("change_pin")
        if st.button("Mini Statement"):
            self.go("mini_statement")
        if st.button("Exit"):
           self.logout()

  def change_pin(self):  
    new_pin = st.text_input("Please enter your new PIN:", max_chars=4, type="password",key="new_pin_input")
    confirm_pin = st.text_input("Please confirm your new PIN:", max_chars=4, type="password",key="confirm_new_pin_input")
    if st.button("Change PIN"):
        if new_pin != confirm_pin:
            st.error("PINs do not match.")
        else:
            st.session_state.pin = new_pin
            self.add_statement("PIN changed")
            st.success("Your PIN has been changed successfully")
    if st.button("Back to Menu"):
                self.go("menu")
    elif st.button("Exit"):
                self.logout()
    

  def withdraw(self):
    st.subheader("Withdraw Money")
    if st.session_state.balance == 0:
      st.write("Your balance is zero. Please deposit money first.")
      if st.button("Back to Menu"):
            self.go("menu")
      elif st.button("Exit"):
        self.logout()
    return
    
    amount = st.number_input("Enter the amount to withdraw:")
    if amount < st.session_state.balance:
      st.session_state.balance -= amount
      self. add_statement(f"Withdraw: {amount}")
      st.write("Withdrawal successful")
    else:
      st.write("Insufficient balance")
    self.display_menu()

  def display_balance(self):
    st.metric(label="Your balance ",value=f"${st.session_state.balance:,.2f}")
    if st.button("Back to Menu"):
        self.go("menu")
    elif st.button("Exit"):
        self.logout()

  def deposit(self):
    amount = st.number_input("Enter the amount to deposit:")
    st.session_state.balance += amount
    self. add_statement(f"Deposit: {amount}")
    st.write("Deposit successful")
    if st.button("Back to Menu"):
        self.go("menu")
    elif st.button("Exit"):
        self.logout()

  def mini_statement(self):
    if len(st.session_state.statements) == 0:
      st.write("You haven't done anything yet.")


    else:
      st.write("Last 5 statements are:")
      for entry in st.session_state.statements:
        st.write(entry)
    if st.button("Back to Menu"):
        self.go("menu")
    elif st.button("Exit"):
        self.logout()

  
  def add_statement(self, text):
    st.session_state.statements.append(text)
    if len(st.session_state.statements) > 5:
      st.session_state.statements.pop(0)


def main():
  user = ATM()
  if st.session_state.screen == "welcome":
        user.welcome()
  elif st.session_state.screen == "login":
        user.login()
  elif st.session_state.screen == "menu":
         user.display_menu()  
  elif st.session_state.screen == "withdraw":
        user.withdraw()
  elif st.session_state.screen == "display_balance":
        user.display_balance()              
  elif st.session_state.screen == "deposit":
        user.deposit()
  elif st.session_state.screen == "change_pin":
        user.change_pin() 
  elif st.session_state.screen == "mini_statement":
        user.mini_statement() 

if __name__ == '__main__':
  main()
