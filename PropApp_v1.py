import tkinter as tk
import tkinter.filedialog
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.font as font
import pandas as pd
# NLP Packages
import re
import joblib

jl = joblib.load('logreg_binary')  # Logistic regression for binary classification (propaganda/non-propaganda)
jl_multiClass = joblib.load('multiclass_logreg')  # Logistic regression for multi Class  (14 classes)
# Structure and Layout
window = Tk()
window.title("PropApp v 1.0")
window.geometry("800x600")
window.config(background='black')
myFont = font.Font(family='Times', size=10, weight='bold')
# TAB LAYOUT
tab_control = ttk.Notebook(window)
main_tab = ttk.Frame(tab_control)
about_tab = ttk.Frame(tab_control)

# ADD TABS TO NOTEBOOK

tab_control.add(main_tab, text='PropApp')
tab_control.add(about_tab, text='About')

label2 = Label(main_tab, text='Propaganda detection tool', padx=5, pady=5, font=myFont)
label2.grid(column=0, row=0)

label3 = Label(about_tab, text='About', padx=5, pady=5)
label3.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

about_label = Label(about_tab, text=" PropApp v1.0\n\n Vlad Ermurachi", pady=5, padx=5)
about_label.grid(column=0, row=1)


# Clear entry widget
def clear_entry_text():
    firstEntry.delete(0, END)


def clear_display_result():
    tab1_display.delete('1.0', END)


# Clear Text  with position 1.0
def clear_text_file():
    displayed_file.delete('1.0', END)


# Clear Result of Functions
def clear_result():
    main_tab_display_text.delete('1.0', END)


# Open File to Read and Process
def open_files():
    try:
        file1 = tk.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"), ("All files", "*")))
        read_text = open(file1).read()
        displayed_file.insert(tk.END, read_text)

    except:
        displayed_file.insert(tk.END, "Insert your text or load a file")


def clean_text(post):
    replaceBySpace = re.compile("[/(){}\[\]|@,;]")
    badSymbols = re.compile("[^0-9a-z #+_]")
    post = replaceBySpace.sub(' ', post)
    post = badSymbols.sub('', post)
    return post


def list_to_df(propaganda_list):
    df = pd.DataFrame(propaganda_list, columns=["Text", "Technique"])
    df["Text"] = df["Text"].replace("'\n'", '')
    return df.to_string(index=False)


def percent_of_propaganda(a_list, text):
    propaganda = [i[0] for i in a_list]
    propaganda = "".join(propaganda)
    totalNumberOfWords = len(text)
    numberOfPropagandaWords = len(propaganda)
    percentOfPropaganda = numberOfPropagandaWords * 100 / totalNumberOfWords
    response = f"\n\nPercent of Propaganda = {str(percentOfPropaganda)[:5]}%"
    return response

def prop():
    main_tab_display_text.delete('1.0', END)
    try:
        propList = []
        raw_text = displayed_file.get('1.0', tk.END)
        vector = raw_text + '.'
        vector = re.split("[?.!]", vector)
        for i in range(0, len(vector) - 1):
            text = vector[i]
            cleanedText = clean_text(text)
            x = jl.predict([cleanedText])
            if x == "propaganda":
                y = jl_multiClass.predict([cleanedText])
                response = (text, y)
                propList.append(response)
        if len(propList) > 0:
            main_tab_display_text.insert(tk.END, list_to_df(propList))
            main_tab_display_text.insert(tk.END, percent_of_propaganda(propList, raw_text))
        else:
            main_tab_display_text.insert(tk.END, "No propaganda detected")
    except:
        wrong_mess = "Something went wrong! Please try again..."
        main_tab_display_text.insert(tk.END, wrong_mess)


# FILE READING  AND PROCESSING TAB
l1 = Label(main_tab, text="Insert your text or load a file")
l1.grid(row=1, column=1)

displayed_file = ScrolledText(main_tab, height=9)
displayed_file.grid(row=2, column=0, columnspan=5, padx=5, pady=3)

# BUTTONS FOR SECOND TAB/FILE READING TAB
b0 = Button(main_tab, text="Load File...", width=12, command=open_files, bg='#c5cae9', font=myFont)
b0.grid(row=1, column=2, padx=10, pady=10)

b1 = Button(main_tab, text="Reset", width=12, command=clear_text_file, bg="#b9f6ca", font=myFont)
b1.grid(row=3, column=2, padx=10, pady=10)

b2 = Button(main_tab, text="Check", width=12, command=prop, bg='#03A9F4', fg='#fff', font=myFont)
b2.grid(row=3, column=0)

b3 = Button(main_tab, text="Clear Result", width=12, command=clear_result, font=myFont)
b3.grid(row=4, column=2, padx=10, pady=10)

b4 = Button(main_tab, text="Exit", width=12, command=window.destroy, font=myFont)
b4.grid(row=8, column=2, padx=10, pady=10)

# Display Screen

# main_tab_display_text = Text(main_tab)
main_tab_display_text = ScrolledText(main_tab, height=10)
main_tab_display_text.grid(row=7, column=0, columnspan=5, padx=5, pady=5)

# Allows to edit
main_tab_display_text.config(state=NORMAL)

window.mainloop()
