from tkinter import *


root = Tk()

root.geometry("200x200")
root.title("Question 2")
root.configure(background="#3E4149")

parent = Frame(root)
# http://stackoverflow.com/questions/1529847/how-to-change-the-foreground-or-background-colour-of-a-tkinter-button-on-mac-os
buttn = Button(parent, highlightbackground='#3E4149', padx=10, pady=5, text="Submit Vote")
buttn.pack()
parent.pack(expand=1)  # same as expand=True

root.mainloop()