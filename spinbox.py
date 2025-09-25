import tkinter as tk
from tkinter import ttk

def show_value():
    value = spinbox.get()
    label.config(text=f"Selected Value: {value}")

root = tk.Tk()
root.title("Spinbox Example")

# Create a Spinbox
spinbox = tk.Spinbox(root, from_=0, to=20, width=5)
spinbox.pack(pady=10)

# Button to show selected value
button = ttk.Button(root, text="Show Value", command=show_value)
button.pack(pady=5)

# Label to display selected value
label = ttk.Label(root, text="Selected Value: ")
label.pack(pady=5)

root.mainloop()