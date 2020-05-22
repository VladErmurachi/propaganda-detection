import tkinter as tk
import tkinter.filedialog
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.font as font
import pandas as pd
# NLP Packages
import re
from tkinter.ttk import Progressbar
import joblib
import matplotlib
from predict import Prediction, CustomText, Predictors
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Circle

jl = joblib.load('logreg_binary')  # Logistic regression for binary classification (propaganda/non-propaganda)
jl_multiClass = joblib.load('multiclass_logreg')  # Logistic regression for multi Class  (14 classes)
#jl_fragment = joblib.load('logReg_fragment_word')

window = Tk()
window.title("PAS v1.0")
# window.geometry("1200x800")
window.config(background='black')
myFont = font.Font(family='Times New Roman', size=10, weight='bold')
# TAB LAYOUT
tab_control = ttk.Notebook(window)
main_tab = ttk.Frame(tab_control)
statistics_tab = ttk.Frame(tab_control)
about_tab = ttk.Frame(tab_control)
scroll = Scrollbar(window)
scroll.pack(side=RIGHT, fill=Y)
# ADD TABS TO NOTEBOOK

tab_control.add(main_tab, text='PAS')
tab_control.add(statistics_tab, text="Statistics")
tab_control.add(about_tab, text='About')

label2 = Label(main_tab, text='Propaganda detection tool', padx=5, pady=5, font=("Times New Roman", 10))
label2.grid(column=0, row=0)

label3 = Label(about_tab, text='About', padx=5, pady=5, font=("Times New Roman", 10))
label3.grid(column=0, row=0)

label4 = Label(statistics_tab, text="Statistics", padx=5, pady=5, font=("Times New Roman", 10))
label4.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

about_label = Label(about_tab, text=" PAS v1.0\n\n Vlad Ermurachi", pady=5, padx=5)
about_label.grid(column=0, row=1)

statistics_label = Label(statistics_tab, text=" Statistics about data", pady=5, padx=5)
statistics_label.grid(column=0, row=1, sticky=W)

response_label = Label(main_tab, width=40)
response_label.grid(column=1, row=1, columnspan=1, sticky=W)  # 3, 5


def show_info(text):
    response_label.configure(text=text, font=("Times New Roman", 12, "bold"))


# Clear entry widget
def clear_entry_text():
    firstEntry.delete(0, END)


def clear_display_result():
    tab1_display.delete('1.0', END)


# Clear Text  with position 1.0
def clear_text_file():
    show_info("")
    displayed_file.delete('1.0', END)


def open_files():
    displayed_file.delete('1.0', END)
    try:
        file1 = tk.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"), ("All files", "*")))
        read_text = open(file1).read()
        displayed_file.insert(tk.END, read_text)
    except:
        show_info("")


propDict = {}
percent_of_propaganda = ""


def check(event=None):
    show_info("")
    # try:
    raw_text = displayed_file.get('1.0', tk.END)
    candidate = Prediction(raw_text, jl, jl_multiClass)
    global propDict
    propDict = candidate.predict_technique()
    global percent_of_propaganda
    percent_of_propaganda = candidate.percent_of_propaganda()
    if len(propDict) > 0:
        displayed_file.delete('1.0', END)
        displayed_file.insert(tk.END, raw_text)
        displayed_file.tags()
        print(propDict)
        for key in propDict:
            for value in propDict[key]:
                displayed_file.highlight_pattern(value, key)
                tag = key
                displayed_file.tag_configure(tag)
                displayed_file.tag_bind(tag, "<Enter>",
                                        lambda event, key=key: show_info(key))
                displayed_file.tag_bind(tag, "<Leave>",
                                        lambda event, key=key: show_info(""))

    else:
        show_info("No propaganda detected")
    return propDict
    # except:
    #   show_info("Something went wrong! Please try again...")


def plot_techniques():
    plot_window = Tk()
    plot_window.title("Statistics")

    df = pd.DataFrame(propDict.items(), columns=['Technique', 'Instance'])
    df['Length'] = df['Technique'].str.split("").str.len()
    labels = [str(t) for t in df["Technique"]]
    values = [x for x in df["Length"]]
    fig = matplotlib.figure.Figure(figsize=(10, 10))
    fig.suptitle(percent_of_propaganda)
    ax = fig.add_subplot(111)
    ax.pie(values, labels=labels, autopct='%1.1f%%', shadow=True)
    ax.legend(labels)
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=CENTER)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()
    plot_window.mainloop()
    return fig


l1 = Label(main_tab, text="Insert your text or load a file", font=("Times", 10))
l1.grid(row=1, column=3)

displayed_file = CustomText(main_tab, height=25, width=100, yscrollcommand=scroll.set)
displayed_file.grid(row=2, column=1, columnspan=5, padx=5, pady=3)
displayed_file.config(font=("Times New Roman", 11, "bold"))
scroll.config(command=displayed_file.yview)

# BUTTONS
load_button = Button(main_tab, text="Load File...", width=12, command=open_files, bg='#c5cae9',
                     font=("Times New Roman", 10))
load_button.grid(row=1, column=5, padx=10, pady=10, sticky=W)

statistics_button = Button(main_tab, text="Statistics", width=12, command=plot_techniques, bg="light blue",
                           font=("Times New Roman", 10))
statistics_button.grid(row=4, column=1, sticky=W)

reset_button = Button(main_tab, text="Reset", width=12, command=clear_text_file, bg="#b9f6ca", font=("Times", 10))
reset_button.grid(row=3, column=5, padx=10, pady=10, sticky=W)

check_button = Button(main_tab, text="Check", width=12, command=check, bg='#03A9F4', fg='#fff', font=("Times", 10))
check_button.grid(row=3, column=1, sticky=W)

exit_button = Button(main_tab, text="Exit", width=12, command=window.destroy, font=("Times", 10))
exit_button.grid(row=4, column=5, padx=10, pady=10, sticky=W)

window.mainloop()
