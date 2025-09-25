import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import pandas as pd
import re
import os

class MentalWellnessLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("MindBloom – Nurture your thoughts daily")
        self.root.geometry("900x670")
        self.root.configure(bg="#f5f7fa")
        self.entries = []

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#364f6b", foreground="white", relief="flat")
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=27, background="#f5f7fa", fieldbackground="#f5f7fa")
        style.map("TButton", background=[("active", "#455d7a")])
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TCombobox", font=("Segoe UI", 11))

        header_frame = tk.Frame(root, bg="#364f6b", height=70)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(0)
        tk.Label(
            header_frame,
            text="MindBloom",
            font=("Segoe UI", 28, "bold"),
            fg="#f5f7fa",
            bg="#364f6b",
            anchor="w"
        ).pack(side="top", anchor="w", padx=30, pady=(10, 0))
        tk.Label(
            header_frame,
            text="Nurture your thoughts daily",
            font=("Segoe UI", 14),
            fg="#c7d3e0",
            bg="#364f6b",
            anchor="w"
        ).pack(side="top", anchor="w", padx=32, pady=(0, 10))

        input_frame = tk.Frame(root, bg="#f5f7fa", bd=0)
        input_frame.pack(pady=(18, 6), padx=36, fill="x")

        tk.Label(input_frame, text="Student Name:", font=("Segoe UI", 11, "bold"), bg="#f5f7fa").grid(row=0, column=0, sticky="w", pady=7)
        self.name_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=28, bd=1, relief="solid")
        self.name_entry.grid(row=0, column=1, sticky="w", pady=7, padx=(2,15))

        tk.Label(input_frame, text="Mental Wellness Activity:", font=("Segoe UI", 11, "bold"), bg="#f5f7fa").grid(row=1, column=0, sticky="w", pady=7)
        self.wellness_activities = [
            "Meditation", "Journaling", "Art Therapy", "Talking to Loved Ones", "Social Activities"
        ]
        self.wellness_combo = ttk.Combobox(input_frame, values=self.wellness_activities, font=("Segoe UI", 11), width=26)
        self.wellness_combo.grid(row=1, column=1, sticky="w", padx=(2,0), pady=7)
        self.wellness_combo['state'] = 'normal'
        add_wellness_btn = tk.Button(input_frame, text="Add", font=("Segoe UI", 10, "bold"), command=self.add_new_wellness,
                                     bg="#e3eafc", fg="#22223b", bd=0, relief="flat", width=6)
        add_wellness_btn.grid(row=1, column=2, sticky="w", padx=6)

        tk.Label(input_frame, text="Me-Time Activity:", font=("Segoe UI", 11, "bold"), bg="#f5f7fa").grid(row=2, column=0, sticky="w", pady=7)
        self.metime_activities = [
            "Sports", "Music", "Gardening", "Dance", "Research"
        ]
        self.metime_combo = ttk.Combobox(input_frame, values=self.metime_activities, font=("Segoe UI", 11), width=26)
        self.metime_combo.grid(row=2, column=1, sticky="w", padx=(2,0), pady=7)
        self.metime_combo['state'] = 'normal'
        add_metime_btn = tk.Button(input_frame, text="Add", font=("Segoe UI", 10, "bold"), command=self.add_new_metime,
                                   bg="#e3eafc", fg="#22223b", bd=0, relief="flat", width=6)
        add_metime_btn.grid(row=2, column=2, sticky="w", padx=6)

        tk.Label(input_frame, text="Screen-Free Time (minutes):", font=("Segoe UI", 11, "bold"), bg="#f5f7fa").grid(row=3, column=0, sticky="w", pady=7)
        self.screentime_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=28, bd=1, relief="solid")
        self.screentime_entry.grid(row=3, column=1, sticky="w", pady=7, padx=(2,15))

        tk.Label(input_frame, text="Notes (optional):", font=("Segoe UI", 11, "bold"), bg="#f5f7fa").grid(row=4, column=0, sticky="nw", pady=7)
        self.notes_text = tk.Text(input_frame, font=("Segoe UI", 10), height=3, width=40, wrap="word", bg="#f9fbfd", relief="solid", bd=1)
        self.notes_text.grid(row=4, column=1, columnspan=2, pady=7, padx=(2,0), sticky="w")

        tk.Label(input_frame, text="Wellness Status:", font=("Segoe UI", 11, "bold"), bg="#f5f7fa").grid(row=5, column=0, sticky="w", pady=(14,0))
        self.status_label = tk.Label(input_frame, text="Enter details to see status",
                                    font=("Segoe UI", 11), bg="#f5f7fa", fg="#7b8794")
        self.status_label.grid(row=5, column=1, sticky="w", pady=(14,0))

        self.name_entry.bind("<KeyRelease>", self.update_status)
        self.wellness_combo.bind("<<ComboboxSelected>>", self.update_status)
        self.metime_combo.bind("<<ComboboxSelected>>", self.update_status)
        self.screentime_entry.bind("<KeyRelease>", self.update_status)
        self.notes_text.bind("<KeyRelease>", self.update_status)

        btnf = tk.Frame(root, bg="#f5f7fa")
        btnf.pack(pady=8)
        self.create_btn(btnf, "Add Entry", self.add_entry, "#364f6b").pack(side="left", padx=10)
        self.create_btn(btnf, "Delete Selected", self.delete_entry, "#b23b3b").pack(side="left", padx=10)
        self.create_btn(btnf, "Clear All", self.clear_all, "#6d7c93").pack(side="left", padx=10)
        self.create_btn(btnf, "Save to Excel", self.save_to_excel, "#20639b").pack(side="left", padx=10)

        table_frame = tk.Frame(root, bg="#f5f7fa")
        table_frame.pack(padx=30, pady=(12, 0), fill="both", expand=True)
        columns = ("Name", "Wellness", "Me-Time", "Screen-Free Time", "Status", "Notes", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col, w in zip(columns, (110, 120, 110, 120, 95, 205, 120)):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=w, anchor="center")
        self.tree.tag_configure('oddrow', background='#e8ecf3')
        self.tree.tag_configure('evenrow', background='#f5f7fa')
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def create_btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd, font=("Segoe UI", 11, "bold"),
                         bg=color, fg="white", bd=0, padx=20, pady=6,
                         activebackground="#455d7a", cursor="hand2", relief="flat")

    def add_new_wellness(self):
        new_activity = simpledialog.askstring("Add Wellness Activity", "Enter new wellness activity:")
        if new_activity and re.fullmatch(r"[A-Za-z ]+", new_activity.strip()):
            activity = new_activity.strip().title()
            if activity not in self.wellness_activities:
                self.wellness_activities.append(activity)
                self.wellness_combo['values'] = self.wellness_activities
                self.wellness_combo.set(activity)
        elif new_activity is not None:
            messagebox.showerror("Input Error", "Activity must only contain alphabets and spaces.")

    def add_new_metime(self):
        new_activity = simpledialog.askstring("Add Me-Time Activity", "Enter new me-time activity:")
        if new_activity and re.fullmatch(r"[A-Za-z ]+", new_activity.strip()):
            activity = new_activity.strip().title()
            if activity not in self.metime_activities:
                self.metime_activities.append(activity)
                self.metime_combo['values'] = self.metime_activities
                self.metime_combo.set(activity)
        elif new_activity is not None:
            messagebox.showerror("Input Error", "Activity must only contain alphabets and spaces.")

    def update_status(self, event=None):
        name = self.name_entry.get().strip()
        wellness = self.wellness_combo.get().strip()
        metime = self.metime_combo.get().strip()
        screentime = self.screentime_entry.get().strip()
        try:
            if not (name and wellness and metime and screentime):
                self.status_label.config(text="Enter details to see status", fg="#7b8794")
                return
            val = float(screentime)
            if val < 0:
                self.status_label.config(text="Invalid screen-free time", fg="#b23b3b")
                return
        except ValueError:
            self.status_label.config(text="Invalid screen-free time", fg="#b23b3b")
            return
        healthy = val >= 60 and bool(metime)
        self.status_label.config(
            text="Healthy" if healthy else "Needs More Me-Time",
            fg="#09816a" if healthy else "#d35400", font=("Segoe UI", 11, "bold")
        )

    def validate(self):
        name = self.name_entry.get().strip()
        wellness = self.wellness_combo.get().strip()
        metime = self.metime_combo.get().strip()
        screentime = self.screentime_entry.get().strip()
        notes = self.notes_text.get("1.0", "end").strip()

        if not name:
            messagebox.showerror("Input Error", "Student name cannot be empty!")
            return None
        if not wellness:
            messagebox.showerror("Input Error", "Mental wellness activity cannot be empty!")
            return None
        if not metime:
            messagebox.showerror("Input Error", "Me-time activity cannot be empty!")
            return None
        if not screentime:
            messagebox.showerror("Input Error", "Screen-free time cannot be empty!")
            return None

        if not re.fullmatch(r"[A-Za-z ]+", name):
            messagebox.showerror("Input Error", "Student name must only contain alphabets and spaces!")
            return None
        if not re.fullmatch(r"[A-Za-z ]+", wellness):
            messagebox.showerror("Input Error", "Wellness activity must only contain alphabets and spaces!")
            return None
        if not re.fullmatch(r"[A-Za-z ]+", metime):
            messagebox.showerror("Input Error", "Me-time activity must only contain alphabets and spaces!")
            return None

        try:
            screentime_val = float(screentime)
            if screentime_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Screen-free time must be a positive number (in minutes)!")
            return None

        return {
            "student_name": name,
            "mental_wellness_activity": wellness,
            "me-time_activity": metime,
            "screen-free_time_(minutes)": screentime_val,
            "notes": notes
        }, screentime_val, notes

    def add_entry(self):
        res = self.validate()
        if not res:
            return
        values, screentime, notes = res
        status = "Healthy" if screentime >= 60 and values["me-time_activity"] else "Needs More Me-Time"
        entry = {
            "Student Name": values["student_name"],
            "Wellness Activity": values["mental_wellness_activity"],
            "Me-Time Activity": values["me-time_activity"],
            "Screen-Free Time (minutes)": screentime,
            "Status": status,
            "Notes": notes,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.entries.append(entry)
        tag = 'evenrow' if len(self.entries) % 2 == 0 else 'oddrow'
        self.tree.insert("", "end", values=(
            entry["Student Name"], entry["Wellness Activity"], entry["Me-Time Activity"],
            f"{entry['Screen-Free Time (minutes)']} min", entry["Status"], entry["Notes"], entry["Date"]
        ), tags=(tag,))
        self.clear_inputs()
        messagebox.showinfo("Success", "Record added successfully!")

    def delete_entry(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selection Error", "Please select an entry to delete!")
            return
        idx = self.tree.index(sel[0])
        self.tree.delete(sel[0])
        del self.entries[idx]
        messagebox.showinfo("Success", "Record deleted successfully!")

    def clear_all(self):
        if not self.entries:
            messagebox.showinfo("Info", "No entries to clear!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all entries?"):
            self.entries.clear()
            for i in self.tree.get_children():
                self.tree.delete(i)
            self.clear_inputs()
            messagebox.showinfo("Success", "All entries cleared successfully!")

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.wellness_combo.set("")
        self.metime_combo.set("")
        self.screentime_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)
        self.status_label.config(text="Enter details to see status", fg="#7b8794", font=("Segoe UI", 11))

    def save_to_excel(self):
        if not self.entries:
            messagebox.showinfo("Info", "No entries to save!")
            return
        try:
            filename = "Mental_Wellness_Logger.xlsx"
            df_new = pd.DataFrame(self.entries)
            if os.path.exists(filename):
                df_existing = pd.read_excel(filename)
                df_final = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_final = df_new
            df_final.to_excel(filename, index=False)
            messagebox.showinfo("Success", f"Data saved to {filename} successfully!")
            self.entries.clear()
            for i in self.tree.get_children():
                self.tree.delete(i)
        except PermissionError:
            messagebox.showerror("Error", f"Cannot write to '{filename}'.\nPlease close the file in Excel and try again.")
        except ImportError:
            messagebox.showerror("Error", "pandas is required for Excel export. Install with: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving to Excel: {str(e)}")

def main():
    root = tk.Tk()
    MentalWellnessLogger(root)
    root.mainloop()

if __name__ == "__main__":
    main()