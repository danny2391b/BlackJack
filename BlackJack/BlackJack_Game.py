import random
import tkinter as tk
from tkinter import messagebox
import Bank_App as Bank   # Your Bank system


class BlackJackUI:
    def __init__(self, root: tk.Tk, CARDS: dict, bankobj: Bank.BankApp):
        self.root = root
        self.CARDS = CARDS
        self.bankobj = bankobj  # <- connection to bank system

        self.player_cards = []
        self.dealer_cards = []
        self.bet_amount = 0

        root.title("Blackjack")

        # UI -------------------------
        self.info = tk.Label(root, text="Login and place a bet to start!", font=("Arial", 14))
        self.info.pack(pady=10)

        self.player_label = tk.Label(root, text="Player: ", font=("Arial", 12))
        self.player_label.pack()

        self.dealer_label = tk.Label(root, text="Dealer: ", font=("Arial", 12))
        self.dealer_label.pack()

        self.result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=10)

        # BET AREA ----------------------
        bet_frame = tk.Frame(root)
        bet_frame.pack(pady=5)

        tk.Label(bet_frame, text="Bet Amount:").grid(row=0, column=0)
        self.bet_entry = tk.Entry(bet_frame)
        self.bet_entry.grid(row=0, column=1)

        self.place_bet_btn = tk.Button(bet_frame, text="Place Bet", command=self.place_bet)
        self.place_bet_btn.grid(row=0, column=2, padx=5)

        # GAME BUTTONS -------------------
        frame = tk.Frame(root)
        frame.pack(pady=10)

        self.hit_btn = tk.Button(frame, text="Hit", state="disabled", command=self.hit)
        self.hit_btn.grid(row=0, column=0, padx=5)

        self.stand_btn = tk.Button(frame, text="Stand", state="disabled", command=self.stand)
        self.stand_btn.grid(row=0, column=1, padx=5)

        self.start_btn = tk.Button(root, text="Start Game", state="disabled", command=self.start_game)
        self.start_btn.pack(pady=5)

    # -----------------------------------
    # BET CHECK
    # -----------------------------------
    def place_bet(self):
        if not self.bankobj.user_system.is_logged_in:
            messagebox.showerror("Error", "You must log in first!")
            return

        try:
            bet = int(self.bet_entry.get())
        except:
            messagebox.showerror("Error", "Invalid bet.")
            return

        user = self.bankobj.user_system.logged_in_user
        if bet <= 0 or bet > user.money:
            messagebox.showerror("Error", "Not enough money!")
            return

        self.bet_amount = bet
        self.start_btn.config(state="normal")
        messagebox.showinfo("Bet", f"Bet of £{bet} placed!")

    # -----------------------------------
    def dealCard(self):
        return random.choice(list(self.CARDS.keys()))

    def countCards(self, cards):
        total, aces = 0, 0
        for c in cards:
            if c in "JQK" or c == "10":
                total += 10
            elif c == "A":
                total += 11
                aces += 1
            else:
                total += int(c)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    # -----------------------------------
    def start_game(self):
        self.result_label.config(text="")

        self.player_cards = [self.dealCard(), self.dealCard()]
        self.dealer_cards = [self.dealCard(), self.dealCard()]

        self.update_labels()
        self.hit_btn.config(state="normal")
        self.stand_btn.config(state="normal")
        self.start_btn.config(state="disabled")

        if self.countCards(self.player_cards) == 21:
            self.result_label.config(text="Blackjack! Player Wins!")
            self.end_game(win=True)

    # -----------------------------------
    def hit(self):
        self.player_cards.append(self.dealCard())
        self.update_labels()
        if self.countCards(self.player_cards) > 21:
            self.result_label.config(text="Bust! Dealer Wins!")
            self.end_game(win=False)

    # -----------------------------------
    def stand(self):
        while self.countCards(self.dealer_cards) < 17:
            self.dealer_cards.append(self.dealCard())
            self.update_labels()
        self.check_win()

    # -----------------------------------
    def check_win(self):
        p, d = self.countCards(self.player_cards), self.countCards(self.dealer_cards)

        if d > 21:
            self.result_label.config(text=f"Dealer Busts! Player wins.")
            self.end_game(win=True)
        elif p > d:
            self.result_label.config(text=f"Player Wins! {p} vs {d}")
            self.end_game(win=True)
        elif p == d:
            self.result_label.config(text=f"Draw! {p} vs {d}")
            self.end_game(draw=True)
        else:
            self.result_label.config(text=f"Dealer Wins! {d} vs {p}")
            self.end_game(win=False)

    # -----------------------------------
    def update_labels(self):
        self.player_label.config(text=f"Player: {', '.join(self.player_cards)} (Total: {self.countCards(self.player_cards)})")
        self.dealer_label.config(text=f"Dealer: {self.dealer_cards[0]}, ?")

    # -----------------------------------
    def end_game(self, win=False, draw=False):
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")

        # Show full dealer cards
        self.dealer_label.config(
            text=f"Dealer: {', '.join(self.dealer_cards)} (Total: {self.countCards(self.dealer_cards)})"
        )

        user = self.bankobj.user_system.logged_in_user
        if draw:
            return   # No money change

        if win:
            user.money += self.bet_amount 
        else:
            user.money -= self.bet_amount

        self.bankobj.user_system.save_accounts()  # save
        self.bankobj.logged_menu()  # update bank menu


# ------------------------------------------
# RUN PROGRAM
# ------------------------------------------
CARDS = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,
         "9":9,"10":10,"J":10,"Q":10,"K":10,"A":11}

root = tk.Tk()
root2 = tk.Tk()              #Seperate Root for the bank
bank = Bank.BankApp(root2)   #Seperate Root for the bank
game = BlackJackUI(root, CARDS, bank)
root.mainloop()

