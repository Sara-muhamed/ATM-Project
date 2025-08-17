import streamlit as st
from Login import ATM_User
import data


st.set_page_config(page_title="ATM Machine", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .stButton>button {
        font-size:18px;
        padding:12px 20px;
        border-radius:12px;
        width:100%;
        margin-bottom:10px;
        background-color:#2b5876;
        color:white;
        border:none;
        transition:all 0.3s ease-in-out;
        font-weight:600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color:#4e4376;
        transform:scale(1.03);
        box-shadow: 0 6px 8px rgba(0,0,0,0.3);
    }
    input {
        font-size:18px !important;
        text-align:center;
        border-radius:12px;
        padding:12px;
        border:2px solid #ccc;
        margin-bottom:12px;
        transition:all 0.3s ease-in-out;
    }
    input:focus {
        border:2px solid #2b5876;
        outline:none;
        box-shadow:0 0 8px #2b5876;
        background-color:#f9f9ff;
    }
    input[type="number"] {
        font-size:20px !important;
        font-weight:600;
        color:#2b5876;
        background-color:#eef2f7;
    }
    input[type="password"] {
        font-size:22px !important;
        letter-spacing:6px;
        color:#000000 !important;   
        background-color:#ffffff !important; 
    }
            input[type="text"] {
    font-size: 20px !important;
    font-weight: 600;
    color: #2b5876 !important;  
    background-color: #eef2f7 !important;  
}

         
    .stMarkdown h2, .stMarkdown h3 {
        color:#2b5876;
        font-weight:700;
    }
    </style>
""", unsafe_allow_html=True)


# ---------- ATM Session Handling ----------
def load_atm():
    if "atm_data" not in st.session_state:
        st.session_state["atm_data"] = data.load_atm_data()
    return ATM_User.from_dict(st.session_state["atm_data"]) 

def save_atm(atm: ATM_User):
    st.session_state["atm_data"] = atm.to_dict()
    data.save_atm_data(st.session_state["atm_data"])


# ---------- Main ----------
def main():
    st.title("🏧 ATM Machine Simulator")

    atm = load_atm()
    screen = st.session_state.get("screen", "welcome")

    # ---------- Welcome Screen ----------
    if screen == "welcome":
        st.header("👋 Welcome to the ATM")
        if st.button("➡️ Proceed to Login"):
            st.session_state.screen = "login"
            st.rerun()

    # ---------- Login ----------
    elif screen == "login":
        st.subheader("🔑 Login")
        
        account_number = st.text_input("Enter Account Number:", max_chars=6, key="account_number_input")
        pin = st.text_input("Enter PIN:", type="password", max_chars=4, key="pin_input")

        if st.button("Login"):
            ok, msg = atm.login(account_number, pin)
            save_atm(atm)
            if ok:
                st.session_state.account_number = account_number
                st.session_state.screen = "menu"
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error(msg)
                account = atm.get_account(account_number)
                if account and account["attempts_left"] <= 0:
                    st.session_state.screen = "block"
                    st.rerun()
                    
    # ---------- Blocked ----------
    elif screen == "block":
        st.subheader("❌ Account Locked")
        st.error("Too many failed attempts. Please contact support.")
        if st.button("⬅️ Back to Welcome"):
            st.session_state.screen = "welcome"
            st.rerun()

    # ---------- Menu ----------
    elif screen == "menu":
        st.subheader("📋 Main Menu")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("💵 Withdraw"):
                st.session_state.screen = "withdraw"
                st.rerun()
            if st.button("💰 Deposit"):
                st.session_state.screen = "deposit"
                st.rerun()
            if st.button("📊 Balance"):
                st.session_state.screen = "balance"
                st.rerun()

        with col2:
            if st.button("🔐 Change PIN"):
                st.session_state.screen = "change_pin"
                st.rerun()
            if st.button("🧾 Mini Statement"):
                st.session_state.screen = "mini_statement"
                st.rerun()
            if st.button("🚪 Logout"):
                st.success("✅ Logged out successfully.")
                st.session_state.screen = "welcome"
                st.rerun()

    # ---------- Withdraw ----------
    elif screen == "withdraw":
        st.subheader("💵 Withdraw Money")
        account = atm.get_account(st.session_state.account_number)
        
        if account["balance"] <= 0:
            st.error("Your balance is zero. Please deposit money first.")
        else:    
            amount = st.number_input("Enter amount:")
            if st.button("Confirm Withdrawal"):
                ok, msg = atm.withdraw(account["account_number"], amount)
                save_atm(atm)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
        if st.button("⬅️ Back to Menu"):
            st.session_state.screen = "menu"
            st.rerun()

    # ---------- Deposit ----------
    elif screen == "deposit":
        st.subheader("💰 Deposit Money")
        account = atm.get_account(st.session_state.account_number)
        amount = st.number_input("Enter amount:", key="deposit_amount", min_value=1)
        if st.button("Confirm Deposit"):
            ok, msg = atm.deposit(account["account_number"], amount)
            save_atm(atm)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
        if st.button("⬅️ Back to Menu"):
            st.session_state.screen = "menu"
            st.rerun()

    # ---------- Balance ----------
    elif screen == "balance":
        st.subheader("📊 Your Balance")
        account = atm.get_account(st.session_state.account_number)
        st.info(f"💲 Current Balance: {account['balance']}")
        if st.button("⬅️ Back to Menu"):
            st.session_state.screen = "menu"
            st.rerun()

    # ---------- Change PIN ----------
    elif screen == "change_pin":
        st.subheader("🔐 Change PIN")
        old_pin = st.text_input("Enter Old PIN:", type="password")
        new_pin = st.text_input("Enter New PIN (4 digits):", max_chars=4, type="password").strip()
        confirm_pin = st.text_input("Confirm New PIN:", max_chars=4, type="password").strip()

        if st.button("Confirm Change"):
            account = atm.get_account(st.session_state.account_number)
            ok, msg = atm.change_pin(account["account_number"], old_pin, new_pin, confirm_pin)
            save_atm(atm)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
        if st.button("⬅️ Back to Menu"):
            st.session_state.screen = "menu"
            st.rerun()

    # ---------- Mini Statement ----------
    elif screen == "mini_statement":
        st.subheader("🧾 Mini Statement")
        account = atm.get_account(st.session_state.account_number)
        if account["statements"]:
            for s in account["statements"]:
                st.write(f"- {s}")
        else:
            st.info("No transactions yet.")
        if st.button("⬅️ Back to Menu"):
            st.session_state.screen = "menu"
            st.rerun()


# Run App
if __name__ == "__main__":
    main()
