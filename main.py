

import tkinter as tk
import random
import time

# ── Algorithms (exact pseudocode logic) ──────────────────

def brute_force(M, n):
    questions = 0
    for person in range(n):
        knows_someone = False
        for j in range(n):
            if j != person:
                questions += 1
                if M[person][j] == 1:
                    knows_someone = True
                    break
        known_by_all = True
        for i in range(n):
            if i != person:
                questions += 1
                if M[i][person] == 0:
                    known_by_all = False
                    break
        if not knows_someone and known_by_all:
            return person, questions
    return -1, questions


def dcc(M, n):
    candidate = 0
    questions = 0
    for i in range(1, n):              # Elimination phase
        questions += 1
        if M[candidate][i] == 1:
            candidate = i
    for i in range(n):                 # Verification phase
        if i != candidate:
            questions += 1
            if M[candidate][i] == 1:
                return -1, questions
            questions += 1
            if M[i][candidate] == 0:
                return -1, questions
    return candidate, questions


def make_matrix(n):
    M = [[0]*n for _ in range(n)]
    celeb = random.choice([-1] + list(range(n)))
    for i in range(n):
        for j in range(n):
            if i == j:
                M[i][j] = 0
            elif i == celeb:
                M[i][j] = 0           # celebrity knows nobody
            elif j == celeb:
                M[i][j] = 1           # everyone knows celebrity
            else:
                M[i][j] = random.randint(0, 1)
    return M, celeb


# ── Simple color palette ──────────────────────────────────
BG     = "#f0f7f4"   # soft mint white
CARD   = "#ffffff"   # white card
TEAL   = "#2e8b6e"   # main green-teal
LTEAL  = "#d4ede6"   # light teal (card highlight)
DTEAL  = "#1f6b52"   # dark teal (hover)
GRAY   = "#7a9e96"   # muted text
TEXT   = "#1a3530"   # dark text — pops on light bg
RED    = "#c0523a"
AMBER  = "#c47c1a"
AVATARS = ["🧑","👩","🧔","👱","🧕","👨","🧒","👴"]
MAX_HINTS = 3


# =========================================================
#                    MAIN APPLICATION
# =========================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Celebrity Finder")
        self.configure(bg=BG)
        self.state("zoomed")
        try: self.attributes("-zoomed", True)
        except: pass
        self.score = 0
        self.menu()
        
        
    # -----------------------------------------------------
    # Clear Screen
    # -----------------------------------------------------    

    def clear(self):
        for w in self.winfo_children(): w.destroy()

     # -----------------------------------------------------
    # Create Card Layout
    # -----------------------------------------------------
    def card(self):
        self.clear()
        self.configure(bg=BG)
        wrap = tk.Frame(self, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")
        box = tk.Frame(wrap, bg=CARD, padx=50, pady=35,
                       highlightthickness=2, highlightbackground=LTEAL)
        box.pack()
        return box


    # -----------------------------------------------------
    # Styled Label Creator
    # -----------------------------------------------------
    def lbl(self, p, text, size=11, color=TEXT, bold=False):
        w = "bold" if bold else "normal"
        return tk.Label(p, text=text, font=("Segoe UI", size, w),
                        bg=p["bg"], fg=color)
    
    # -----------------------------------------------------
    # Styled Button Creator
    # -----------------------------------------------------

    def btn(self, p, text, cmd, bg=TEAL, fg="white", size=11):
        return tk.Button(p, text=text, command=cmd, bg=bg, fg=fg,
                         font=("Segoe UI", size, "bold"), relief="flat",
                         padx=16, pady=7, cursor="hand2",
                         activebackground=DTEAL, activeforeground="white", bd=0)

    def line(self, p):
        tk.Frame(p, bg=LTEAL, height=2).pack(fill="x", pady=10)

    # =====================================================
    #                     MENU SCREEN
    # =====================================================
    def menu(self):
        box = self.card()
        self.lbl(box, "🌟  Celebrity Finder", 24, TEXT, True).pack(pady=(0,4))
        self.lbl(box, "Known by everyone  ·  Knows nobody", 12, GRAY).pack()
        self.line(box)
        self.lbl(box, "Pick a party size to start:", 12, TEXT, True).pack(pady=(0,8))
        row = tk.Frame(box, bg=CARD); row.pack()
        for label, n, col in [("4 People 🟢",4,TEAL),("6 People 🟡",6,AMBER),("8 People 🔴",8,RED)]:
            self.btn(row, label, lambda n=n: self.start(n), bg=col).pack(side="left", padx=7)
        self.line(box)
        self.lbl(box, f"🏆  Score: {self.score}", 13, TEAL, True).pack(pady=2)
        self.lbl(box, f"📋  How to Play", 13, TEAL, True).pack(pady=2)
        self.lbl(box, f"💡  A celebrity KNOWS nobody but is known by EVERYONE", 11, GRAY).pack()
        self.lbl(box, f"💡  Pick party size, Choose 4, 6, or 8 people to investigate", 11, GRAY).pack()
        self.lbl(box, f"💡  You get {MAX_HINTS} hints — but each one costs 15 points!", 11, GRAY).pack()
        self.lbl(box, f"💡  Make your guess ,Pick who you think the celebrity is!", 11, GRAY).pack()
        self.lbl(box, f"💡  See the result, Watch Brute Force vs DCC algorithm face off", 11, GRAY).pack()

    # =====================================================
    #                    GAME SCREEN
    # =====================================================
    def start(self, n):
        self.n = n
        self.M, self.celeb = make_matrix(n)
        self.hints_left = MAX_HINTS
        self.log = []
        self.t0 = time.time()
        self.game_screen()

    def game_screen(self):
        n = self.n
        box = self.card()

        self.lbl(box, f"👥  Party of {n} — Who is the Celebrity?", 18, TEXT, True).pack(pady=(0,4))
        
        self.lbl(box, "Celebrity: knows nobody  ·  known by everyone", 11, GRAY).pack()
        self.line(box)

        # person tiles
        row = tk.Frame(box, bg=CARD); row.pack(pady=4)
        for i in range(n):
            tile = tk.Frame(row, bg=LTEAL, padx=14, pady=8,
                            highlightthickness=1, highlightbackground="#a8ccc2")
            
            tile.pack(side="left", padx=6)
            tk.Label(tile, text=AVATARS[i], font=("Segoe UI",26), bg=LTEAL).pack()
            tk.Label(tile, text=f"P{i}", font=("Segoe UI",9,"bold"), bg=LTEAL, fg=TEAL).pack()

        self.line(box)

        # hint section
        self.hint_var = tk.StringVar(value=f"💡  Hints left: {self.hints_left}/{MAX_HINTS}")
        
        tk.Label(box, textvariable=self.hint_var, font=("Segoe UI",11,"bold"),
                 bg=CARD, fg=AMBER).pack()
        
        self.lbl(box, "Ask: Does Person ___ know Person ___?", 11, GRAY).pack(pady=(6,4))

        hrow = tk.Frame(box, bg=CARD); hrow.pack()
        
        tk.Label(hrow, text="Does P", font=("Segoe UI",11), bg=CARD, fg=TEXT).pack(side="left")
        self.fv = tk.StringVar(value="0")
        
        om1 = tk.OptionMenu(hrow, self.fv, *[str(i) for i in range(n)])
        
        om1.config(bg=LTEAL, fg=TEXT, font=("Segoe UI",10), relief="flat", bd=0, highlightthickness=0)
        
        om1["menu"].config(bg=LTEAL, fg=TEXT); om1.pack(side="left", padx=4)
        
        tk.Label(hrow, text="know P", font=("Segoe UI",11), bg=CARD, fg=TEXT).pack(side="left")
        
        self.tv = tk.StringVar(value="1")
        
        om2 = tk.OptionMenu(hrow, self.tv, *[str(i) for i in range(n)])
        
        om2.config(bg=LTEAL, fg=TEXT, font=("Segoe UI",10), relief="flat", bd=0, highlightthickness=0)
        
        om2["menu"].config(bg=LTEAL, fg=TEXT); om2.pack(side="left", padx=4)
        
        self.btn(hrow, "Ask 💬", self.hint, bg=AMBER, size=10).pack(side="left", padx=8)

        self.log_lbl = tk.Label(box, text="Hints will show here...",
                                font=("Segoe UI",10), bg=LTEAL, fg=GRAY,
                                padx=12, pady=8, justify="left", anchor="w", width=52)
        self.log_lbl.pack(pady=8, fill="x", padx=10)

        self.line(box)
        self.lbl(box, "Guess the Celebrity:", 13, TEXT, True).pack(pady=(0,8))
        grow = tk.Frame(box, bg=CARD); grow.pack()
        for i in range(n):
            self.btn(grow, f"{AVATARS[i]} P{i}", lambda i=i: self.guess(i), size=10).pack(side="left", padx=5)
        brow = tk.Frame(box, bg=CARD); brow.pack(pady=8)
        self.btn(brow, "🚫 No Celebrity", lambda: self.guess(-1), bg=RED, size=10).pack(side="left", padx=8)
        self.btn(brow, "🏠 Menu", self.menu, bg=LTEAL, fg=GRAY, size=10).pack(side="left", padx=8)
        
        # =====================================================
    #                     HINT SYSTEM
    # =====================================================

    def hint(self):
        if self.hints_left == 0:
            self.log_lbl.config(text="No hints left! Make your guess.", fg=RED); return
        i, j = int(self.fv.get()), int(self.tv.get())
        if i == j:
            self.log_lbl.config(text="⚠️  Choose two different people!", fg=AMBER); return
        self.hints_left -= 1
        self.hint_var.set(f"💡  Hints left: {self.hints_left}/{MAX_HINTS}")
        msg = f"✅ P{i} KNOWS P{j}" if self.M[i][j] == 1 else f"❌ P{i} does NOT know P{j}"
        self.log.append(msg)
        self.log_lbl.config(text="\n".join(self.log[-3:]), fg=DTEAL)

    # =====================================================
    #                    RESULT SCREEN
    # =====================================================
    def guess(self, g):
        elapsed = round(time.time() - self.t0, 1)
        correct = (g == self.celeb)
        used = MAX_HINTS - self.hints_left
        bf_ans, bf_q = brute_force(self.M, self.n)
        dcc_ans, dcc_q = dcc(self.M, self.n)
        if correct:
            self.score += max(0, 100 + max(0, 20-int(elapsed)) - used*15)

        box = self.card()
        if correct:
            self.lbl(box, "🎉  Correct!", 24, TEAL, True).pack(pady=(0,4))
            self.lbl(box, f"Hints used: {used}  ·  -{used*15} pts penalty", 11, GRAY).pack()
        else:
            self.lbl(box, "❌  Wrong!", 24, RED, True).pack(pady=(0,4))
            ans = "No celebrity!" if self.celeb==-1 else f"Person {self.celeb} {AVATARS[self.celeb]} was the celebrity"
            self.lbl(box, ans, 12, RED).pack()

        self.line(box)
        self.lbl(box, "⚡  Algorithm Comparison", 15, TEXT, True).pack(pady=(0,10))

        crow = tk.Frame(box, bg=CARD); crow.pack()
        for title, ans, q, col in [("🔍 Brute Force", bf_ans, bf_q, GRAY),
                                    ("⚡ Smart DCC",   dcc_ans, dcc_q, TEAL)]:
            c = tk.Frame(crow, bg=LTEAL, padx=24, pady=14,
                         highlightthickness=2, highlightbackground=col)
            c.pack(side="left", padx=10)
            tk.Label(c, text=title, font=("Segoe UI",12,"bold"), bg=LTEAL, fg=col).pack()
            tk.Label(c, text="No Celebrity" if ans==-1 else f"Person {ans}",
                     font=("Segoe UI",11), bg=LTEAL, fg=TEXT).pack(pady=4)
            tk.Label(c, text=f"❓ {q} questions", font=("Segoe UI",10), bg=LTEAL, fg=GRAY).pack()

        saved = bf_q - dcc_q
        verdict = (f"✅ DCC saved {saved} questions ({round(saved/bf_q*100)}% fewer)!" if saved>0
                   else "🔵 Brute Force used fewer questions this time!" if saved<0
                   else "🤝 Both used the same number of questions.")
        self.lbl(box, verdict, 11, TEAL if saved>=0 else RED, True).pack(pady=8)
        self.lbl(box, f"⏱ {elapsed}s  ·  💡 {used} hints  ·  🏆 Score: {self.score}", 11, GRAY).pack()

        self.line(box)
        row = tk.Frame(box, bg=CARD); row.pack()
        self.btn(row, "▶ Next Round", lambda: self.start(self.n)).pack(side="left", padx=8)
        self.btn(row, "🏠 Menu", self.menu, bg=LTEAL, fg=GRAY).pack(side="left", padx=8)


# =========================================================
#                    PROGRAM START
# =========================================================

if __name__ == "__main__":
    App().mainloop()