from tkinter import *
import random

def simulateMetrics():
    pulse.set(random.randint(60, 100))
    bp.set(random.randint(90, 160))
    heart.set(random.randint(60, 120))
    exercise.set(random.randint(0, 60))
    status.set("Metrics Simulated")
    steps.set(random.randint(1000, 10000))
    assessMetrics()

def resetMetrics():
    pulse.set("")
    bp.set("")
    heart.set("")
    exercise.set("")
    status.set("")
    steps.set("")
    assessment.set("")

def assessMetrics():
    p = int(pulse.get())
    b = int(bp.get())
    h = int(heart.get())
    e = int(exercise.get())
    result = ""
    if p < 100 and 90 <= b <= 120 and h < 100 and e >= 30:
        result = "Normal Metrics"
    elif e < 30:
        result = "Increase Physical Activity"
    elif b > 120:
        result = "High Blood Pressure"
    else:
        result = "Monitor Regularly"
    assessment.set(result)

def exitApp():
    root.destroy()

root = Tk()
root.title("Smartwatch Health Monitoring System")
root.geometry("350x500")

pulse = StringVar()
bp = StringVar()
heart = StringVar()
exercise = StringVar()
status = StringVar()
steps = StringVar()
assessment = StringVar()

topFrame = Frame(root)
topFrame.pack(pady=10)

Label(topFrame, text="Health Metrics", font=('Arial', 12, 'bold')).pack()

metricsFrame = LabelFrame(root, text="Metrics", padx=10, pady=10)
metricsFrame.pack(padx=10, pady=5)

Label(metricsFrame, text="Pulse Rate").grid(row=0, column=0, sticky=W)
Entry(metricsFrame, textvariable=pulse, width=15).grid(row=0, column=1)

Label(metricsFrame, text="Blood Pressure").grid(row=1, column=0, sticky=W)
Entry(metricsFrame, textvariable=bp, width=15).grid(row=1, column=1)

Label(metricsFrame, text="Heart Beat").grid(row=2, column=0, sticky=W)
Entry(metricsFrame, textvariable=heart, width=15).grid(row=2, column=1)

Label(metricsFrame, text="Exercise Duration").grid(row=3, column=0, sticky=W)
Entry(metricsFrame, textvariable=exercise, width=15).grid(row=3, column=1)

actionFrame = Frame(root)
actionFrame.pack(pady=10)

Button(actionFrame, text="Simulate", command=simulateMetrics, width=10).grid(row=0, column=0, padx=5)
Button(actionFrame, text="Reset", command=resetMetrics, width=10).grid(row=0, column=1, padx=5)
Button(actionFrame, text="Exit", command=exitApp, width=10).grid(row=0, column=2, padx=5)

summaryFrame = LabelFrame(root, text="Health Summary", padx=10, pady=10)
summaryFrame.pack(padx=10, pady=5)

Label(summaryFrame, text="Status").grid(row=0, column=0, sticky=W)
Entry(summaryFrame, textvariable=status, width=20).grid(row=0, column=1)

Label(summaryFrame, text="Steps Logged").grid(row=1, column=0, sticky=W)
Entry(summaryFrame, textvariable=steps, width=20).grid(row=1, column=1)

Label(summaryFrame, text="Assessment").grid(row=2, column=0, sticky=W)
Entry(summaryFrame, textvariable=assessment, width=20).grid(row=2, column=1)

root.mainloop()
