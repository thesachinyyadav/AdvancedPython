import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd

entries = []

def addEntry():
    name = nameEntry.get().strip()
    activity = activityEntry.get().strip()
    meTime = meTimeEntry.get().strip()
    screenTime = screenTimeEntry.get().strip()

    if not name or not activity or not meTime or not screenTime:
        messagebox.showerror("Input Error", "All fields are required.")
        return
    
    if not screenTime.isdigit() or int(screenTime) <= 0:
        messagebox.showerror("Input Error", "Screen-free time must be a positive number.")
        return

    status = "Healthy" if int(screenTime) >= 60 else "Needs More Me-Time"
    statusVar.set(status)

    entry = {
        "Name": name,
        "Activity": activity,
        "Me-Time": meTime,
        "Screen-Free Time": int(screenTime),
        "Status": status
    }
    entries.append(entry)
    updateTree()
    messagebox.showinfo("Success", "Entry added successfully.")

def deleteEntry():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Delete Error", "Select a record to delete.")
        return
    idx = int(tree.item(selected)['text'])
    entries.pop(idx)
    updateTree()
    messagebox.showinfo("Deleted", "Selected entry deleted.")

def clearAll():
    if messagebox.askyesno("Confirm", "Clear all records?"):
        entries.clear()
        updateTree()

def updateTree():
    for item in tree.get_children():
        tree.delete(item)
    for i, entry in enumerate(entries):
        tree.insert("", "end", text=str(i), values=(
            entry["Name"], entry["Activity"], entry["Me-Time"],
            entry["Screen-Free Time"], entry["Status"]
        ))

def saveToExcel():
    if not entries:
        messagebox.showerror("Save Error", "No data to save.")
        return
    df = pd.DataFrame(entries)
    try:
        df.to_excel("Mental_Wellness_Log.xlsx", index=False)
        messagebox.showinfo("Saved", "Data exported to Mental_Wellness_Log.xlsx")
    except:
        messagebox.showerror("Save Error", "Failed to save file.")

root = tk.Tk()
root.title("Mental Wellness Entry Logger")
root.geometry("800x500")

titleLabel = tk.Label(root, text="Mental Wellness Entry Logger", font=("Arial", 18, "bold"))
titleLabel.pack(pady=10)

inputFrame = tk.Frame(root)
inputFrame.pack(pady=5)

tk.Label(inputFrame, text="Student Name:").grid(row=0, column=0, padx=5, pady=5)
nameEntry = tk.Entry(inputFrame)
nameEntry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(inputFrame, text="Wellness Activity:").grid(row=1, column=0, padx=5, pady=5)
activityEntry = tk.Entry(inputFrame)
activityEntry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(inputFrame, text="Me-Time Activity:").grid(row=2, column=0, padx=5, pady=5)
meTimeEntry = tk.Entry(inputFrame)
meTimeEntry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(inputFrame, text="Screen-Free Time (mins):").grid(row=3, column=0, padx=5, pady=5)
screenTimeEntry = tk.Entry(inputFrame)
screenTimeEntry.grid(row=3, column=1, padx=5, pady=5)

statusVar = tk.StringVar()
tk.Label(inputFrame, text="Wellness Status:").grid(row=4, column=0, padx=5, pady=5)
statusLabel = tk.Label(inputFrame, textvariable=statusVar, width=20, relief="sunken")
statusLabel.grid(row=4, column=1, padx=5, pady=5)

buttonFrame = tk.Frame(root)
buttonFrame.pack(pady=10)

tk.Button(buttonFrame, text="Add Entry", command=addEntry, width=15).grid(row=0, column=0, padx=10)
tk.Button(buttonFrame, text="Delete Selected Entry", command=deleteEntry, width=20).grid(row=0, column=1, padx=10)
tk.Button(buttonFrame, text="Clear All", command=clearAll, width=15).grid(row=0, column=2, padx=10)
tk.Button(buttonFrame, text="Save to Excel", command=saveToExcel, width=15).grid(row=0, column=3, padx=10)

treeFrame = tk.Frame(root)
treeFrame.pack(pady=10)

cols = ("Name", "Activity", "Me-Time", "Screen-Free Time", "Status")
tree = ttk.Treeview(treeFrame, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=140)
tree.pack()

root.mainloop()
