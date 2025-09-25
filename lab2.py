import re

class UserRegistration:
    def __init__(self, name, age, reg_no, password):
        self.name = name
        self.age = age
        self.reg_no = reg_no
        self.password = password

    def validate(self):
        self._validate_name()
        self._validate_age()
        self._validate_reg_no()
        self._validate_password()
        return True

    def _validate_name(self):
        if not re.fullmatch(r"^[A-Za-z\s]+$", self.name):
            raise ValueError("Invalid name. Only letters and spaces are allowed.")

    def _validate_age(self):
        if not (18 <= self.age <= 60):
            raise ValueError("Invalid age. Age must be between 18 and 60.")

    def _validate_reg_no(self):
        if not re.fullmatch(r"\d{6}", self.reg_no):
            raise ValueError("Invalid registration number. It must be a 6-digit number.")

    def _validate_password(self):
        pw = self.password
        if not re.fullmatch(r"^[A-Za-z0-9@#$%^&+=]{8,}$", pw):
            raise ValueError("Invalid password. It must be at least 8 characters long and contain letters, numbers, and special characters.")
        if not re.search(r"[A-Za-z]", pw) or not re.search(r"\d", pw):
            raise ValueError("Invalid password. It must contain at least one letter and one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
            raise ValueError("Invalid password. It must contain at least one special character.")
        if not re.search(r"[A-Z]", pw):
            raise ValueError("Invalid password. It must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", pw):
            raise ValueError("Invalid password. It must contain at least one lowercase letter.")
        if not re.search(r"\d", pw):
            raise ValueError("Invalid password. It must contain at least one digit.")
