import tkinter as tk
from tkinter import ttk, messagebox
import re
import csv

class Validator:
    @staticmethod
    def validate_name(name):
        return re.fullmatch(r"[A-Za-z ]{2,}", name) is not None

    @staticmethod
    def validate_email(email):
        return re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[a-zA-Z]{2,}", email) is not None

    @staticmethod
    def validate_phone(phone):
        return re.fullmatch(r"(0|\+91)?[6-9]\d{9}", phone) is not None

    @staticmethod
    def validate_password(password):
        return re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}", password) is not None

    @staticmethod
    def password_strength(password):
        score = sum([
            len(password) >= 8,
            bool(re.search(r"[a-z]", password)),
            bool(re.search(r"[A-Z]", password)),
            bool(re.search(r"\d", password)),
            bool(re.search(r"[@$!%*?&]", password)),
        ])
        if score == 5:
            return "Strong", "#2e7d32"
        elif score >= 3:
            return "Medium", "#f9a825"
        return "Weak", "#c62828"

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form")
        self.root.geometry("520x700")
        self.root.resizable(False, False)
        self.theme_dark = False

        self.show_password = tk.BooleanVar()
        self.agree_terms = tk.BooleanVar()

        self.valid_icons = {}
        self.entries = {}
        self.dark_mode_button = None

        self.build_ui()

    def build_ui(self):
        self.set_theme()

        container = tk.Frame(self.root, bg=self.bg_color)
        container.place(relx=0.5, rely=0.5, anchor='center')

        top_bar = tk.Frame(container, bg=self.bg_color)
        top_bar.pack(fill="x")
        self.dark_mode_button = tk.Button(top_bar, text="🌙 Dark Mode" if not self.theme_dark else "☀ Light Mode", 
                                          command=self.toggle_theme, bg="#444", fg="white", font=("Segoe UI", 9))
        self.dark_mode_button.pack(side="right", padx=5, pady=5)

        self.title_label = tk.Label(container, text="User Registration", font=("Segoe UI", 24, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.title_label.pack(pady=(5, 0))

        subtitle = tk.Label(container, text="Create your account. It's free and only takes a minute.", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color)
        subtitle.pack(pady=(0, 10))

        self.card = tk.Frame(container, bg=self.card_color, bd=2, relief="groove")
        self.card.pack(padx=25, pady=5, fill="both", expand=True)

        self.add_field("Name")
        self.add_field("Email")
        self.add_field("Phone")
        self.add_field("Password", show="*")
        self.add_field("Confirm Password", show="*")

        ttk.Checkbutton(self.card, text="Show Password", variable=self.show_password, command=self.toggle_password).pack(anchor='w', padx=10, pady=5)

        self.strength_label = tk.Label(self.card, text="Strength: ", font=("Segoe UI", 9), bg=self.card_color, fg=self.fg_color)
        self.strength_label.pack(anchor='w', padx=10, pady=3)

        ttk.Checkbutton(container, text="I accept the Terms of Use & Privacy Policy", variable=self.agree_terms, command=self.validate_form).pack(pady=8)

        btn_frame = tk.Frame(container, bg=self.bg_color)
        btn_frame.pack(pady=10)
        self.submit_btn = tk.Button(btn_frame, text="Register Now", command=self.submit, bg="#43a047", fg="white", width=20, font=("Segoe UI", 10, "bold"), state="disabled")
        self.submit_btn.grid(row=0, column=0, padx=10)
        self.clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_form, bg="#bdbdbd", fg="black", width=10, font=("Segoe UI", 10, "bold"))
        self.clear_btn.grid(row=0, column=1, padx=10)

        signin_frame = tk.Frame(container, bg=self.bg_color)
        signin_frame.pack(pady=(0, 10))
        signin_label = tk.Label(signin_frame, text="Already have an account? ", bg=self.bg_color, fg=self.fg_color)
        signin_label.pack(side="left")
        signin_link = tk.Label(signin_frame, text="Sign in", fg="blue", bg=self.bg_color, cursor="hand2")
        signin_link.pack(side="left")

        for field in self.entries:
            self.entries[field].bind("<KeyRelease>", self.validate_form)

    def set_theme(self):
        if self.theme_dark:
            self.bg_color = "#121212"
            self.fg_color = "#eeeeee"
            self.card_color = "#1e1e1e"
        else:
            self.bg_color = "#e5e9f2"
            self.fg_color = "#000000"
            self.card_color = "#ffffff"
        self.root.configure(bg=self.bg_color)

    def toggle_theme(self):
        self.theme_dark = not self.theme_dark
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_ui()

    def add_field(self, label, show=None):
        container = tk.Frame(self.card, bg=self.card_color)
        container.pack(fill="x", pady=5, padx=10)
        tk.Label(container, text=label + ":", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.fg_color).pack(anchor='w')
        inner = tk.Frame(container, bg=self.card_color)
        inner.pack(fill="x")
        entry = ttk.Entry(inner, width=32, show=show, font=("Segoe UI", 10))
        entry.pack(side="left", padx=(0, 5), pady=2)
        tick = tk.Label(inner, text="", bg=self.card_color, fg="green", font=("Segoe UI", 12, "bold"))
        tick.pack(side="left")
        self.entries[label] = entry
        self.valid_icons[label] = tick

    def toggle_password(self):
        show = "" if self.show_password.get() else "*"
        self.entries["Password"].config(show=show)
        self.entries["Confirm Password"].config(show=show)

    def validate_form(self, event=None):
        name = self.entries["Name"].get()
        email = self.entries["Email"].get()
        phone = self.entries["Phone"].get()
        password = self.entries["Password"].get()
        confirm = self.entries["Confirm Password"].get()
        terms = self.agree_terms.get()

        valid_name = Validator.validate_name(name)
        valid_email = Validator.validate_email(email)
        valid_phone = Validator.validate_phone(phone)
        valid_password = Validator.validate_password(password)
        passwords_match = password == confirm and confirm != ""

        strength, color = Validator.password_strength(password)
        self.strength_label.config(text="Strength: " + strength, fg=color)

        self.valid_icons["Name"].config(text="✔" if valid_name else "")
        self.valid_icons["Email"].config(text="✔" if valid_email else "")
        self.valid_icons["Phone"].config(text="✔" if valid_phone else "")
        self.valid_icons["Password"].config(text="✔" if valid_password else "")
        self.valid_icons["Confirm Password"].config(text="✔" if passwords_match else "")

        if all([valid_name, valid_email, valid_phone, valid_password, passwords_match, terms]):
            self.submit_btn.config(state="normal")
        else:
            self.submit_btn.config(state="disabled")

    def submit(self):
        name = self.entries["Name"].get()
        email = self.entries["Email"].get()
        phone = self.entries["Phone"].get()
        password = self.entries["Password"].get()
        confirm = self.entries["Confirm Password"].get()

        errors = []
        if not Validator.validate_name(name):
            errors.append("Enter a valid name (only letters, min 2 chars).")
        if not Validator.validate_email(email):
            errors.append("Enter a valid email address.")
        if not Validator.validate_phone(phone):
            errors.append("Enter a valid Indian phone number (10 digits).")
        if not Validator.validate_password(password):
            errors.append("Password must have 8+ chars, 1 upper, 1 lower, 1 digit, 1 special.")
        if password != confirm or confirm == "":
            errors.append("Password and Confirm Password do not match.")
        if not self.agree_terms.get():
            errors.append("You must agree to the Terms & Conditions.")

        if errors:
            messagebox.showerror("Invalid Input", "\n".join(errors))
            return

        with open("registrations.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, email, phone, password])

        messagebox.showinfo("Success", "\U0001F389 Registration Successful!")
        self.clear_form()

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        for tick in self.valid_icons.values():
            tick.config(text="")
        self.show_password.set(False)
        self.toggle_password()
        self.agree_terms.set(False)
        self.strength_label.config(text="Strength: ", fg=self.fg_color)
        self.submit_btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationForm(root)
    root.mainloop()
