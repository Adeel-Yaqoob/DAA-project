import tkinter as tk
from tkinter import ttk, messagebox
import random

# -------------------- Game Data --------------------
people = ["Person 1", "Person 2", "Person 3", "Person 4", "Person 5"]
n = len(people)
celebrity = 0
knows = []
questions = 0
score = 100

# -------------------- Game Logic --------------------
def create_game():
    global celebrity, knows, questions, score

    celebrity = random.randint(0, n - 1)
    questions = 0
    score = 100

    # Create n x n matrix
    knows = [[False for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                knows[i][j] = False
            elif j == celebrity:
                knows[i][j] = True       # everyone knows celebrity
            elif i == celebrity:
                knows[i][j] = False      # celebrity knows nobody
            else:
                knows[i][j] = random.choice([True, False])

    answer_label.config(text="Answer will appear here", fg="black")
    info_box.delete("1.0", tk.END)
    info_box.insert(tk.END, "New game started. Ask questions and find the celebrity.\n")
    update_stats()


def ask_question():
    global questions, score

    a = box_a.current()
    b = box_b.current()

    if a == b:
        messagebox.showwarning("Invalid", "A person cannot ask about himself.")
        return

    questions += 1
    score = max(0, score - 5)

    if knows[a][b]:
        result = f"YES, {people[a]} knows {people[b]}."
        answer_label.config(text=result, fg="green")
    else:
        result = f"NO, {people[a]} does not know {people[b]}."
        answer_label.config(text=result, fg="red")

    info_box.insert(tk.END, result + "\n")
    update_stats()


def guess_celebrity():
    guess = guess_box.current()

    if guess == celebrity:
        messagebox.showinfo("Correct", f"Correct! {people[guess]} is the celebrity.\nScore: {score}")
        info_box.insert(tk.END, f"Correct guess! Celebrity is {people[guess]}.\n")
    else:
        messagebox.showerror("Wrong", f"Wrong guess! Correct celebrity was {people[celebrity]}.")
        info_box.insert(tk.END, f"Wrong guess. Correct celebrity was {people[celebrity]}.\n")


def brute_force():
    checks = 0

    for i in range(n):
        possible = True

        # celebrity should know nobody
        for j in range(n):
            if i != j:
                checks += 1
                if knows[i][j]:
                    possible = False
                    break

        # everyone should know celebrity
        if possible:
            for j in range(n):
                if i != j:
                    checks += 1
                    if not knows[j][i]:
                        possible = False
                        break

        if possible:
            info_box.insert(tk.END, f"Brute Force found: {people[i]} | Checks: {checks}\n")
            return

    info_box.insert(tk.END, f"Brute Force: No celebrity | Checks: {checks}\n")


def efficient_algo():
    checks = 0
    candidate = 0

    # Step 1: eliminate non-celebrities
    for i in range(1, n):
        checks += 1
        if knows[candidate][i]:
            candidate = i

    # Step 2: verify candidate
    for j in range(n):
        if j != candidate:
            checks += 1
            if knows[candidate][j] or not knows[j][candidate]:
                info_box.insert(tk.END, f"Efficient Algo: No celebrity | Checks: {checks}\n")
                return

    info_box.insert(tk.END, f"Efficient Algo found: {people[candidate]} | Checks: {checks}\n")


def show_matrix():
    win = tk.Toplevel(root)
    win.title("Hidden Matrix")
    win.geometry("420x300")

    text = tk.Text(win, font=("Courier", 10))
    text.pack(padx=10, pady=10)

    text.insert(tk.END, "Hidden Knows Matrix\n\n")
    text.insert(tk.END, "      P1 P2 P3 P4 P5\n")

    for i in range(n):
        row = f"P{i+1}   "
        for j in range(n):
            row += "1  " if knows[i][j] else "0  "
        text.insert(tk.END, row + "\n")

    text.insert(tk.END, f"\nCelebrity: {people[celebrity]}\n")
    text.insert(tk.END, "1 = knows, 0 = does not know")


def update_stats():
    stats_label.config(text=f"Questions: {questions} | Score: {score}")

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Celebrity Puzzle Game")
root.geometry("950x720")
root.resizable(False, False)
root.configure(bg="#eef3f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 11, "bold"), padding=8)

# Title
label_title = tk.Label(root, text="Celebrity Puzzle Game", font=("Arial", 26, "bold"), bg="#eef3f8", fg="#1f3c88")
label_title.pack(pady=15)

label_subtitle = tk.Label(root, text="Find the person who knows nobody but is known by everyone.", font=("Arial", 13), bg="#eef3f8")
label_subtitle.pack()

main_frame = tk.Frame(root, bg="#eef3f8")
main_frame.pack(pady=20)

left_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge", width=390, height=520)
left_frame.grid(row=0, column=0, padx=15)
left_frame.pack_propagate(False)

right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge", width=460, height=520)
right_frame.grid(row=0, column=1, padx=15)
right_frame.pack_propagate(False)

# Left side
tk.Label(left_frame, text="Ask a Question", font=("Arial", 18, "bold"), bg="white", fg="#1f3c88").pack(pady=20)
tk.Label(left_frame, text="Does Person A know Person B?", font=("Arial", 12), bg="white").pack(pady=5)

box_a = ttk.Combobox(left_frame, values=people, state="readonly", width=25)
box_a.pack(pady=8)
box_a.current(0)

box_b = ttk.Combobox(left_frame, values=people, state="readonly", width=25)
box_b.pack(pady=8)
box_b.current(1)

ttk.Button(left_frame, text="Ask Question", command=ask_question).pack(pady=12)

answer_label = tk.Label(left_frame, text="Answer will appear here", font=("Arial", 13, "bold"), bg="white")
answer_label.pack(pady=10)

tk.Label(left_frame, text="Make Your Guess", font=("Arial", 18, "bold"), bg="white", fg="#1f3c88").pack(pady=20)

guess_box = ttk.Combobox(left_frame, values=people, state="readonly", width=25)
guess_box.pack(pady=8)
guess_box.current(0)

ttk.Button(left_frame, text="Guess Celebrity", command=guess_celebrity).pack(pady=12)

# Right side
tk.Label(right_frame, text="Game Information", font=("Arial", 18, "bold"), bg="white", fg="#1f3c88").pack(pady=20)

rules = "Rules:\n1. A celebrity knows nobody.\n2. Everyone else knows the celebrity.\n3. Ask questions to find the celebrity.\n4. Fewer questions give a better score."
tk.Label(right_frame, text=rules, font=("Arial", 12), bg="white", justify="left").pack(pady=5)

info_box = tk.Text(right_frame, height=10, width=50, font=("Arial", 10), bg="#f7f9fc")
info_box.pack(pady=12)

stats_label = tk.Label(right_frame, text="Questions: 0 | Score: 100", font=("Arial", 13, "bold"), bg="white")
stats_label.pack(pady=10)

# Bottom buttons
bottom_frame = tk.Frame(root, bg="#eef3f8")
bottom_frame.pack(pady=10)

ttk.Button(bottom_frame, text="Run Brute Force", command=brute_force).grid(row=0, column=0, padx=7)
ttk.Button(bottom_frame, text="Run Efficient Algo", command=efficient_algo).grid(row=0, column=1, padx=7)
ttk.Button(bottom_frame, text="New Game", command=create_game).grid(row=0, column=2, padx=7)
ttk.Button(bottom_frame, text="Show Hidden Matrix", command=show_matrix).grid(row=0, column=3, padx=7)
ttk.Button(bottom_frame, text="Exit", command=root.quit).grid(row=0, column=4, padx=7)

create_game()
root.mainloop()
