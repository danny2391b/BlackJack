import tkinter as tk
from tkinter import messagebox
import os
import json

# ------------------------------
# USER SYSTEM
# ------------------------------
class User:
    def __init__(self, username, password="", money=0):
        self.username = username
        self.password = password
        self.money = int(money)

    def to_dict(self):
        return {
            "user": self.username,
            "pass": self.password,
            "money": self.money
        }


class Users:
    def __init__(self):
        self.accounts = []
        self.is_logged_in = False
        self.logged_in_user = None
        self.load_accounts()

    def load_accounts(self):
        if os.path.exists("Accounts.json"):
            try:
                with open("Accounts.json", "r") as f:
                    data = json.load(f)
                self.accounts = [User(d["user"], d["pass"], d["money"]) for d in data]
            except:
                print("Accounts.json is empty or corrupted.")
                self.accounts = []

    def save_accounts(self):
        with open("Accounts.json", "w") as f:
            json.dump([user.to_dict() for user in self.accounts], f, indent=4)

    def add_account(self, username, password, money):
        self.accounts.append(User(username, password, money))
        self.save_accounts()
        return True

    def login(self, username_input, password_input):
        for user in self.accounts:
            if user.username == username_input and user.password == password_input:
                self.logged_in_user = user
                self.is_logged_in = True
                return True
        return False

    def send_money(self, target_username, amount):
        if not self.logged_in_user:
            return False, "You must log in first!"

        for user in self.accounts:
            if user.username == target_username:
                if self.logged_in_user.money >= amount:
                    self.logged_in_user.money -= amount
                    user.money += amount
                    self.save_accounts()
                    return True, "Transfer successful!"
                else:
                    return False, "Not enough money!"
        return False, "Target account not found."


# ------------------------------
# TKINTER UI
# ------------------------------

class BankApp:
    def __init__(self, root):
        self.user_system = Users()
        self.root = root
        self.root.title("Bank System")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.build_main_menu()

    # ---------- MAIN MENU ----------
    def build_main_menu(self):
        self.clear_frame()
        tk.Label(self.frame, text="Bank App", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.frame, text="Create Account", width=20,
                  command=self.create_account_ui).pack(pady=5)
        tk.Button(self.frame, text="Login", width=20,
                  command=self.login_ui).pack(pady=5)
        tk.Button(self.frame, text="Quit", width=20,
                  command=self.root.quit).pack(pady=5)

    # ---------- CREATE ACCOUNT ----------
    def create_account_ui(self):
        self.clear_frame()
        tk.Label(self.frame, text="Create Account", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.frame, text="Username:").pack()
        username_entry = tk.Entry(self.frame)
        username_entry.pack()

        tk.Label(self.frame, text="Password:").pack()
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.pack()

        tk.Label(self.frame, text="Starting Money:").pack()
        money_entry = tk.Entry(self.frame)
        money_entry.pack()

        def create_account():
            user = username_entry.get()
            pw = password_entry.get()
            money = money_entry.get()

            if not user or not pw or not money.isdigit():
                messagebox.showerror("Error", "Invalid input.")
                return

            self.user_system.add_account(user, pw, int(money))
            messagebox.showinfo("Success", "Account created!")
            self.build_main_menu()

        tk.Button(self.frame, text="Create", command=create_account).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.build_main_menu).pack()

    # ---------- LOGIN ----------
    def login_ui(self):
        self.clear_frame()
        tk.Label(self.frame, text="Login", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.frame, text="Username:").pack()
        user_entry = tk.Entry(self.frame)
        user_entry.pack()

        tk.Label(self.frame, text="Password:").pack()
        pass_entry = tk.Entry(self.frame, show="*")
        pass_entry.pack()

        def login():
            if self.user_system.login(user_entry.get(), pass_entry.get()):
                self.logged_menu()
            else:
                messagebox.showerror("Error", "Wrong username or password")

        tk.Button(self.frame, text="Login", command=login).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.build_main_menu).pack()

    # ---------- LOGGED IN MENU ----------
    def logged_menu(self):
        self.clear_frame()
        user = self.user_system.logged_in_user

        tk.Label(self.frame, text=f"Logged in as: {user.username}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.frame, text=f"Balance: £{user.money}", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.frame, text="Send Money", width=20, command=self.send_money_ui).pack(pady=5)
        tk.Button(self.frame, text="Log Out", width=20, command=self.logout).pack(pady=5)
        tk.Button(self.frame, text="Back to Menu", width=20, command=self.build_main_menu).pack(pady=5)

    def logout(self):
        self.user_system.logged_in_user = None
        self.user_system.is_logged_in = False
        self.build_main_menu()

    # ---------- SEND MONEY ----------
    def send_money_ui(self):
        self.clear_frame()
        tk.Label(self.frame, text="Send Money", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.frame, text="Target Username:").pack()
        target_entry = tk.Entry(self.frame)
        target_entry.pack()

        tk.Label(self.frame, text="Amount:").pack()
        amount_entry = tk.Entry(self.frame)
        amount_entry.pack()

        def send():
            if not amount_entry.get().isdigit():
                messagebox.showerror("Error", "Amount must be a number.")
                return

            success, msg = self.user_system.send_money(
                target_entry.get(), int(amount_entry.get())
            )

            messagebox.showinfo("Result", msg)
            self.logged_menu()

        tk.Button(self.frame, text="Send", command=send).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.logged_menu).pack()

    # ---------- UTILITY ----------
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()



