import tkinter as tk
from tkinter import messagebox
import random
import string

COMMON_PASSWORDS = ["kodikos", "password", "123456", "qwerty", "admin"]

# Έλεγχος αν ο κωδικός είναι ασφαλής
def is_strong(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in string.punctuation for c in password):
        return False
    if password.lower() in COMMON_PASSWORDS:
        return False
    return True

# Δημιουργία παρόμοιων κωδικών
def generate_suggestions(password: str, n: int = 3):
    suggestions = []
    for _ in range(n):
        new_pass = password
        if not any(c.isupper() for c in new_pass):
            new_pass += random.choice(string.ascii_uppercase)
        if not any(c.isdigit() for c in new_pass):
            new_pass += str(random.randint(0, 9))
        if not any(c in string.punctuation for c in new_pass):
            new_pass += random.choice("!@#$%&*")
        while len(new_pass) < 8:
            new_pass += random.choice(string.ascii_letters + string.digits)
        suggestions.append(new_pass)
    return suggestions

SECURITY_REQUIREMENTS = """
Απαιτήσεις για ασφαλή κωδικό:
- Τουλάχιστον 8 χαρακτήρες
- Τουλάχιστον 1 κεφαλαίο γράμμα
- Τουλάχιστον 1 αριθμό
- Τουλάχιστον 1 ειδικό χαρακτήρα (!, @, #, κ.λπ.)
- Να μην είναι συνηθισμένη λέξη (π.χ. "kodikos", "password")
"""

class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Έλεγχος Ασφαλείας Κωδικού")

        self.label = tk.Label(root, text="Δώσε έναν κωδικό:")
        self.label.pack(pady=5)

        # Frame για το entry και το κουμπί με το ματάκι
        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=5)

        self.entry = tk.Entry(entry_frame, show="*")
        self.entry.pack(side=tk.LEFT, padx=(0,5))

        self.show_password = False
        self.eye_btn = tk.Button(entry_frame, text="👁️", width=3, command=self.toggle_password)
        self.eye_btn.pack(side=tk.LEFT)

        self.check_btn = tk.Button(root, text="Έλεγχος", command=self.check_password)
        self.check_btn.pack(pady=5)

        self.suggestions_frame = tk.Frame(root)
        self.suggestions_frame.pack(pady=10)

        self.req_label = tk.Label(root, text=SECURITY_REQUIREMENTS, justify="left")
        self.req_label.pack(pady=10)

    def toggle_password(self):
        if self.show_password:
            self.entry.config(show="*")
            self.eye_btn.config(text="👁️")  # eye open
            self.show_password = False
        else:
            self.entry.config(show="")
            self.eye_btn.config(text="🙈")  # eye closed
            self.show_password = True

    def check_password(self):
        for widget in self.suggestions_frame.winfo_children():
            widget.destroy()

        password = self.entry.get()
        if is_strong(password):
            messagebox.showinfo("Ασφάλεια", "✅ Όλα καλά! Ο κωδικός είναι ασφαλής.")
        else:
            messagebox.showwarning("Ασφάλεια", "❌ Ο κωδικός δεν είναι ασφαλής.")
            suggestions = generate_suggestions(password)
            tk.Label(self.suggestions_frame, text="Προτάσεις:").pack()
            for sug in suggestions:
                btn = tk.Button(self.suggestions_frame, text=sug, command=lambda s=sug: self.choose_password(s))
                btn.pack(pady=2)
            tk.Button(self.suggestions_frame, text="Ξαναγράψε νέο κωδικό", command=self.reset_entry).pack(pady=5)

    def choose_password(self, password):
        if is_strong(password):
            messagebox.showinfo("Ασφάλεια", f"✅ Επέλεξες ασφαλή κωδικό: {password}")
        else:
            messagebox.showerror("Ασφάλεια", "Αυτός ο κωδικός δεν είναι αρκετά ασφαλής.")

    def reset_entry(self):
        self.entry.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
