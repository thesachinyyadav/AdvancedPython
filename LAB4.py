import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import re, os
import matplotlib
matplotlib.use("Agg")


class MentalWellnessLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("MindBloom – Nurture your thoughts daily")
        self.root.geometry("1000x720")
        self.root.configure(bg="#f8fafc")
        self.entries = []
        self.dark_mode = False
        self.colors = {'primary': '#3b82f6', 'success': '#10b981', 'warning': '#f59e0b', 'danger': '#ef4444', 'light': '#f8fafc', 'card': '#fff'}
        self.setup_styles()
        self.layout_main()


    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Modern.TButton", font=("Segoe UI", 10, "bold"), padding=(15, 8), borderwidth=0)
        style.configure("Card.TFrame", background="#fff", relief="flat", borderwidth=1)


    def layout_main(self):
        self.header(tk.Frame(self.root, bg=self.colors['primary'], height=80).pack(fill="x"))
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.quick_actions(main_frame)
        self.stats_cards(main_frame)
        self.recent_entries(main_frame)
        self.update_summary()


    def header(self, header_frame):
        header_frame = self.root.winfo_children()[0]
        tk.Label(header_frame, text="MindBloom", font=("Segoe UI", 24, "bold"), bg=self.colors['primary'], fg="white").pack(side="left", padx=30, pady=20)
        tk.Label(header_frame, text="Nurture your thoughts daily", font=("Segoe UI", 12), bg=self.colors['primary'], fg="#bfdbfe").pack(side="left", padx=30)
        tk.Button(header_frame, text="🌙", font=("Segoe UI", 16), bg=self.colors['primary'], fg="white", bd=0, command=self.toggle_theme, cursor="hand2").pack(side="right", padx=30)


    def quick_actions(self, parent):
        actions = [("➕ Add Entry", self.open_entry_window, self.colors['success']),
                   ("📊 Dashboard", self.open_dashboard_window, self.colors['primary']),
                   ("📋 View Data", self.open_data_table_window, "#8b5cf6"),
                   ("🧮 Calculator", self.open_calc_window, self.colors['warning'])]
        frame = tk.Frame(parent, bg=self.colors['light'])
        frame.pack(fill="x", pady=(0, 20))
        tk.Label(frame, text="Quick Actions", font=("Segoe UI", 16, "bold"), bg=self.colors['light'], fg="#1e293b").pack(anchor="w")
        btns = tk.Frame(frame, bg=self.colors['light'])
        btns.pack(fill="x")
        for text, cmd, color in actions:
            tk.Button(btns, text=text, command=cmd, font=("Segoe UI", 11, "bold"), bg=color, fg="white", bd=0, padx=20, pady=12, cursor="hand2").pack(side="left", padx=8, pady=8)


    def stats_cards(self, parent):
        frame = tk.Frame(parent, bg=self.colors['light'])
        frame.pack(fill="x", pady=(0, 20))
        tk.Label(frame, text="Overview", font=("Segoe UI", 16, "bold"), bg=self.colors['light'], fg="#1e293b").pack(anchor="w")
        cards = tk.Frame(frame, bg=self.colors['light'])
        cards.pack(fill="x")
        self.total_card = self.stat_card(cards, "Total Entries", "0", self.colors['primary'])
        self.healthy_card = self.stat_card(cards, "Healthy Days", "0", self.colors['success'])
        self.avg_card = self.stat_card(cards, "Avg Screen-Free", "0 min", self.colors['warning'])


    def stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="#fff", relief="solid", bd=1, padx=20, pady=15)
        card.pack(side="left", padx=10)
        tk.Label(card, text=title, font=("Segoe UI", 10), bg="#fff", fg="#64748b").pack(anchor="w")
        val_lbl = tk.Label(card, text=value, font=("Segoe UI", 20, "bold"), bg="#fff", fg=color)
        val_lbl.pack(anchor="w")
        return val_lbl


    def recent_entries(self, parent):
        frame = tk.Frame(parent, bg=self.colors['light'])
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Recent Activity", font=("Segoe UI", 16, "bold"), bg=self.colors['light'], fg="#1e293b").pack(anchor="w")
        canvas = tk.Canvas(frame, bg=self.colors['light'], height=200)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.recent_entries_frame = tk.Frame(canvas, bg=self.colors['light'])
        canvas.create_window((0, 0), window=self.recent_entries_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.recent_entries_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    def create_entry_card(self, parent, entry):
        card = tk.Frame(parent, bg="#fff", relief="solid", bd=1, padx=15, pady=10)
        card.pack(fill="x", pady=(0, 10))
        tk.Label(card, text=entry["Student Name"], font=("Segoe UI", 12, "bold"), bg="#fff", fg="#1e293b").pack(side="left")
        status_color = self.colors['success'] if entry["Status"] == "Healthy" else self.colors['warning']
        tk.Label(card, text=entry["Status"], font=("Segoe UI", 10, "bold"), bg=status_color, fg="white", padx=8, pady=2).pack(side="right")
        details = f"🧘 {entry['Wellness Activity']} | 🎯 {entry['Me-Time Activity']} | ⏰ {entry['Screen-Free Time (minutes)']} min"
        tk.Label(card, text=details, font=("Segoe UI", 10), bg="#fff", fg="#64748b").pack(anchor="w", pady=(5, 0))
        tk.Label(card, text=entry["Date"], font=("Segoe UI", 9), bg="#fff", fg="#94a3b8").pack(anchor="w")


    def open_entry_window(self, edit_idx=None):
        win = tk.Toplevel(self.root)
        win.title("Add Mental Wellness Entry")
        win.geometry("400x400")
        win.configure(bg="#f8fafc")
        win.transient(self.root)
        win.grab_set()
        tk.Label(win, text="✨ New Wellness Entry", font=("Segoe UI", 14, "bold"), bg=self.colors['primary'], fg="white").pack(fill="x")
        form = tk.Frame(win, bg="#fff", padx=20, pady=20)
        form.pack(fill="both", expand=True, padx=18, pady=18)
        fields = {}
        combos = {
            'wellness': ["Meditation", "Journaling", "Art Therapy", "Talking to Loved Ones", "Social Activities"],
            'metime': ["Sports", "Music", "Gardening", "Dance", "Research"]
        }
        labels = {'name': "Student Name", 'wellness': "Wellness Activity", 'metime': "Me-Time Activity", 'screentime': "Screen-Free Time (minutes)", 'notes': "Notes (optional)"}
        for i, key in enumerate(['name', 'wellness', 'metime', 'screentime', 'notes']):
            tk.Label(form, text=labels[key], font=("Segoe UI", 11, "bold"), bg="#fff", fg="#1e293b").grid(row=i*2, column=0, sticky="w", pady=(0, 5))
            if key in combos:
                fields[key] = ttk.Combobox(form, font=("Segoe UI", 11), width=28, values=combos[key])
            elif key == 'notes':
                fields[key] = tk.Text(form, font=("Segoe UI", 10), height=2, width=28, bg="#f8fafc")
            else:
                fields[key] = tk.Entry(form, font=("Segoe UI", 11), width=30, bg="#f8fafc")
            fields[key].grid(row=i*2+1, column=0, sticky="ew", pady=(0, 10))
        status_label = tk.Label(form, text="", font=("Segoe UI", 11, "bold"), bg="#fff", fg="#64748b")
        status_label.grid(row=10, column=0, pady=(0, 10))
        def update_status(*_):
            try:
                name = fields['name'].get().strip()
                wellness = fields['wellness'].get().strip()
                metime = fields['metime'].get().strip()
                screentime = fields['screentime'].get().strip()
                if not all([name, wellness, metime, screentime]):
                    status_label.config(text="Fill all fields to see status", fg="#64748b")
                    return
                val = float(screentime)
                if val < 0: raise ValueError
                healthy = val >= 60 and bool(metime)
                status_label.config(text=f"Status: {'✅ Healthy' if healthy else '⚠️ Needs More Me-Time'}", fg=self.colors['success'] if healthy else self.colors['warning'])
            except:
                status_label.config(text="Invalid screen-free time", fg=self.colors['danger'])
        for key in ['name', 'screentime']:
            fields[key].bind("<KeyRelease>", update_status)
        for key in ['wellness', 'metime']:
            fields[key].bind("<<ComboboxSelected>>", update_status)
        if edit_idx is not None:
            entry = self.entries[edit_idx]
            fields['name'].insert(0, entry["Student Name"])
            fields['wellness'].set(entry["Wellness Activity"])
            fields['metime'].set(entry["Me-Time Activity"])
            fields['screentime'].insert(0, str(entry["Screen-Free Time (minutes)"]))
            fields['notes'].insert("1.0", entry["Notes"])
            update_status()
        def save_entry():
            try:
                name = fields['name'].get().strip()
                wellness = fields['wellness'].get().strip()
                metime = fields['metime'].get().strip()
                screentime = fields['screentime'].get().strip()
                notes = fields['notes'].get("1.0", "end").strip()
                if not all([name, wellness, metime, screentime]):
                    messagebox.showerror("Error", "All fields except notes are required!")
                    return
                if not re.fullmatch(r"[A-Za-z ]+", name): messagebox.showerror("Error", "Name must only contain letters and spaces!"); return
                screentime_val = float(screentime)
                if screentime_val <= 0: raise ValueError
                status = "Healthy" if screentime_val >= 60 and metime else "Needs More Me-Time"
                entry = {"Student Name": name, "Wellness Activity": wellness, "Me-Time Activity": metime, "Screen-Free Time (minutes)": screentime_val, "Status": status, "Notes": notes, "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}
                if edit_idx is not None:
                    self.entries[edit_idx] = entry
                    messagebox.showinfo("Success", "Entry updated successfully!")
                else:
                    self.entries.append(entry)
                    messagebox.showinfo("Success", "Entry added successfully!")
                self.update_summary()
                win.destroy()
            except: messagebox.showerror("Error", "Screen-free time must be a positive number!")
        btn_frame = tk.Frame(form, bg="#fff")
        btn_frame.grid(row=11, column=0, pady=10)
        tk.Button(btn_frame, text="💾 Save Entry", command=save_entry, font=("Segoe UI", 12, "bold"), bg=self.colors['success'], fg="white", bd=0, padx=18, pady=10, cursor="hand2").pack(side="left", padx=6)
        tk.Button(btn_frame, text="❌ Cancel", command=win.destroy, font=("Segoe UI", 12, "bold"), bg=self.colors['danger'], fg="white", bd=0, padx=18, pady=10, cursor="hand2").pack(side="left", padx=6)


    def open_data_table_window(self):
        win = tk.Toplevel(self.root)
        win.title("Wellness Data Table")
        win.geometry("800x400")
        win.configure(bg=self.colors['light'])
        tk.Label(win, text="📋 Wellness Data", font=("Segoe UI", 15, "bold"), bg="#8b5cf6", fg="white").pack(fill="x")
        search_var = tk.StringVar()
        search_frame = tk.Frame(win, bg=self.colors['light'])
        search_frame.pack(fill="x")
        tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 11), bg=self.colors['light'], fg="#1e293b").pack(side="left")
        tk.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 11), width=28, bd=1, relief="solid").pack(side="left", padx=8)
        table_frame = tk.Frame(win, bg="#fff")
        table_frame.pack(fill="both", expand=True)
        cols = ("Name", "Wellness", "Me-Time", "Screen-Free", "Status", "Date")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)
        for col in cols: tree.heading(col, text=col, anchor="center"); tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        def update_table():
            tree.delete(*tree.get_children())
            ftxt = search_var.get().lower()
            for entry in self.entries:
                if not ftxt or ftxt in entry["Student Name"].lower() or ftxt in entry["Status"].lower():
                    tree.insert("", "end", values=(entry["Student Name"], entry["Wellness Activity"], entry["Me-Time Activity"], f"{entry['Screen-Free Time (minutes)']} min", entry["Status"], entry["Date"]))
        search_var.trace('w', lambda *args: update_table())
        update_table()
        tk.Button(win, text="✏️ Edit Selected", command=lambda: self.edit_selected_entry(tree, win), font=("Segoe UI", 10, "bold"), bg=self.colors['primary'], fg="white", bd=0, padx=15, pady=8, cursor="hand2").pack(pady=8)


    def edit_selected_entry(self, tree, win):
        sel = tree.selection()
        if not sel: messagebox.showwarning("No Selection", "Please select an entry to edit."); return
        idx = tree.index(sel[0])
        win.destroy()
        self.open_entry_window(edit_idx=idx)


    def open_dashboard_window(self):
        win = tk.Toplevel(self.root)
        win.title("Wellness Dashboard")
        win.geometry("800x420")
        win.configure(bg=self.colors['light'])
        tk.Label(win, text="📊 Wellness Dashboard", font=("Segoe UI", 16, "bold"), bg=self.colors['primary'], fg="white").pack(fill="x")
        frame = tk.Frame(win, bg="#fff")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        if not self.entries:
            tk.Label(frame, text="No data to display", font=("Segoe UI", 16), bg="#fff", fg="#64748b").pack(expand=True)
            return
        healthy = sum(1 for e in self.entries if e["Status"] == "Healthy")
        needs_more = len(self.entries) - healthy
        fig = Figure(figsize=(7, 3), dpi=100, facecolor='#fff')
        ax = fig.add_subplot(111)
        ax.pie([healthy, needs_more], labels=["Healthy", "Needs Improvement"], autopct='%1.1f%%', colors=[self.colors['success'], self.colors['warning']], startangle=90)
        ax.set_title("Wellness Status Distribution", fontsize=14, fontweight='bold', pad=20)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(pady=10)
        total_time = sum(e["Screen-Free Time (minutes)"] for e in self.entries)
        avg_time = total_time / len(self.entries) if self.entries else 0
        stats_text = f"📈 Total Entries: {len(self.entries)} | 🎯 Healthy Days: {healthy} | ⏱️ Avg Screen-Free: {avg_time:.1f} min"
        tk.Label(frame, text=stats_text, font=("Segoe UI", 12, "bold"), bg="#fff", fg="#1e293b").pack()


    def open_calc_window(self):
        win = tk.Toplevel(self.root)
        win.title("Wellness Calculator")
        win.geometry("400x260")
        win.configure(bg=self.colors['light'])
        tk.Label(win, text="🧮 Wellness Calculator", font=("Segoe UI", 16, "bold"), bg=self.colors['warning'], fg="white").pack(fill="x")
        frame = tk.Frame(win, bg="#fff", padx=16, pady=16)
        frame.pack(fill="both", expand=True, padx=20, pady=18)
        result_var = tk.StringVar()
        tk.Label(frame, text="Screen-Free Time Statistics", font=("Segoe UI", 14, "bold"), bg="#fff", fg="#1e293b").pack(pady=(0, 12))
        tk.Label(frame, textvariable=result_var, font=("Segoe UI", 12), bg="#fff", fg="#64748b", justify="left").pack(pady=8)
        def calc():
            if not self.entries: result_var.set("📊 No data available"); return
            times = [e["Screen-Free Time (minutes)"] for e in self.entries]
            total, avg = sum(times), sum(times) / len(times)
            healthy_count = sum(1 for e in self.entries if e["Status"] == "Healthy")
            result_var.set(f"📈 Total: {total:.1f} min\n⚡ Average: {avg:.1f} min\n🎯 Healthy Days: {healthy_count}/{len(self.entries)}\n🔝 Best: {max(times):.1f} min\n📉 Lowest: {min(times):.1f} min")
        tk.Button(frame, text="🧮 Calculate", command=calc, font=("Segoe UI", 12, "bold"), bg=self.colors['warning'], fg="white", bd=0, padx=16, pady=8, cursor="hand2").pack(pady=12)
        calc()


    def update_summary(self):
        if hasattr(self, 'total_card'):
            self.total_card.config(text=str(len(self.entries)))
        if hasattr(self, 'healthy_card'):
            healthy = sum(1 for e in self.entries if e["Status"] == "Healthy")
            self.healthy_card.config(text=str(healthy))
        if hasattr(self, 'avg_card'):
            if self.entries:
                avg = sum(e["Screen-Free Time (minutes)"] for e in self.entries) / len(self.entries)
                self.avg_card.config(text=f"{avg:.1f} min")
            else:
                self.avg_card.config(text="0 min")
        if hasattr(self, 'recent_entries_frame'):
            for widget in self.recent_entries_frame.winfo_children():
                widget.destroy()
            if not self.entries:
                tk.Label(self.recent_entries_frame, text="No entries yet. Add your first wellness entry!", font=("Segoe UI", 12), bg=self.colors['light'], fg="#64748b").pack(pady=20)
            else:
                for entry in reversed(self.entries[-5:]):
                    self.create_entry_card(self.recent_entries_frame, entry)


    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.root.configure(bg="#1e293b" if self.dark_mode else self.colors['light'])


def main():
    root = tk.Tk()
    MentalWellnessLogger(root)
    root.mainloop()


if __name__ == "__main__":
    main()
