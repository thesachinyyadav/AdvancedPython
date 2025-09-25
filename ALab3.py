import tkinter as tk

from tkinter import messagebox, ttk

import pandas as pd


class WellnessLoggerApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Mental Wellness Entry Logger")

        self.entries = []


        tk.Label(root, text="Mental Wellness Entry Logger", font=("Arial", 16, "bold")).pack(pady=10)


        input_frame = tk.Frame(root, padx=10, pady=10)

        input_frame.pack()


        tk.Label(input_frame, text="Student Name:").grid(row=0, column=0, sticky="e")

        self.name_entry = tk.Entry(input_frame, width=30)

        self.name_entry.grid(row=0, column=1)


        tk.Label(input_frame, text="Wellness Activity:").grid(row=1, column=0, sticky="e")

        self.wellness_entry = tk.Entry(input_frame, width=30)

        self.wellness_entry.grid(row=1, column=1)


        tk.Label(input_frame, text="Me-Time Activity:").grid(row=2, column=0, sticky="e")

        self.me_time_entry = tk.Entry(input_frame, width=30)

        self.me_time_entry.grid(row=2, column=1)


        tk.Label(input_frame, text="Screen-Free Time (min):").grid(row=3, column=0, sticky="e")

        self.screen_time_entry = tk.Entry(input_frame, width=30)

        self.screen_time_entry.grid(row=3, column=1)


        self.status_label = tk.Label(input_frame, text="Status: ", fg="blue", font=("Arial", 10, "italic"))

        self.status_label.grid(row=4, column=1, sticky="w", pady=(5, 0))


        button_frame = tk.Frame(root, pady=10)

        button_frame.pack()


        tk.Button(button_frame, text="Add Entry", command=self.add_entry).grid(row=0, column=0, padx=5)

        tk.Button(button_frame, text="Delete Selected Entry", command=self.delete_entry).grid(row=0, column=1, padx=5)

        tk.Button(button_frame, text="Clear All", command=self.clear_all).grid(row=0, column=2, padx=5)

        tk.Button(button_frame, text="Save to Excel", command=self.save_to_excel).grid(row=0, column=3, padx=5)


        self.tree = ttk.Treeview(root, columns=("Name", "Wellness", "MeTime", "ScreenTime", "Status"), show='headings', height=8)

        for col in self.tree["columns"]:

            self.tree.heading(col, text=col)

            self.tree.column(col, width=120)

        self.tree.pack(pady=10)


        self.screen_time_entry.bind("<FocusOut>", lambda e: self.update_status())


    def update_status(self):

        try:

            screen_time = int(self.screen_time_entry.get())

            if screen_time >= 120 and self.wellness_entry.get().strip() and self.me_time_entry.get().strip():

                status = "Healthy"

            else:

                status = "Needs More Me-Time"

        except:

            status = "Needs More Me-Time"

        self.status_label.config(text=f"Status: {status}")

        return status


    def add_entry(self):

        name = self.name_entry.get().strip()

        wellness = self.wellness_entry.get().strip()

        me_time = self.me_time_entry.get().strip()

        screen_time_str = self.screen_time_entry.get().strip()


        if not name or not wellness or not me_time or not screen_time_str:

            messagebox.showerror("Error", "All fields must be filled.")

            return


        try:

            screen_time = int(screen_time_str)

            if screen_time <= 0:

                raise ValueError

        except:

            messagebox.showerror("Error", "Screen-Free Time must be a positive number.")

            return


        status = self.update_status()


        self.tree.insert("", "end", values=(name, wellness, me_time, screen_time, status))

        messagebox.showinfo("Success", "Entry added successfully.")

        self.clear_inputs()


    def delete_entry(self):

        selected_item = self.tree.selection()

        if not selected_item:

            messagebox.showerror("Error", "No entry selected.")

            return

        self.tree.delete(selected_item)

        messagebox.showinfo("Deleted", "Selected entry deleted.")


    def clear_all(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        messagebox.showinfo("Cleared", "All entries cleared.")


    def clear_inputs(self):

        self.name_entry.delete(0, tk.END)

        self.wellness_entry.delete(0, tk.END)

        self.me_time_entry.delete(0, tk.END)

        self.screen_time_entry.delete(0, tk.END)

        self.status_label.config(text="Status: ")


    def save_to_excel(self):

        data = []

        for row_id in self.tree.get_children():

            data.append(self.tree.item(row_id)["values"])

        if not data:

            messagebox.showwarning("Warning", "No data to save.")

            return

        df = pd.DataFrame(data, columns=["Name", "Wellness", "MeTime", "ScreenTime", "Status"])

        try:

            df.to_excel("Mental_Wellness_Log.xlsx", index=False)

            messagebox.showinfo("Saved", "Data saved to Mental_Wellness_Log.xlsx")

        except Exception as e:

            messagebox.showerror("Error", f"Failed to save Excel: {e}")


if __name__ == "__main__":

    root = tk.Tk()

    app = WellnessLoggerApp(root)

    root.mainloop()