import os
import tkinter as tk
from tkinter import ttk,filedialog,messagebox

text_content = dict()


def create(content="",title="Untiitled"):
    text_area = tk.Text(notebook)
    text_area.insert("end",content)
    text_area.pack(fill="both", expand=True)
    notebook.add(text_area, text=title)
    notebook.select(text_area)
    text_content[str(text_area)] = hash(content)

def check_for_changes():
    current =get_text_widget()
    content = current.get("1.0","end-1c")
    name = notebook.tab(current)["text"]
    if hash(content) != text_content[str(current)]:
        if name[-1]!="*":
            notebook.tab("current",text=name+"*")
    elif name[-1] == "*":
        notebook.tab("current",text=name[:-1])


def get_text_widget():
    text_widget = root.nametowidget(notebook.select())
    return text_widget

def close_current_tab():
    current = get_text_widget()
    if current_tab_unsaved() and not confirm_close():
        return
    if len(notebook.tabs()) ==1:
        create()

    notebook.forget(current)
def current_tab_unsaved():
    text_widget = get_text_widget()
    content = text_widget.get("1.0", "end-1c")
    return hash(content) != text_content[str(text_widget)]

def confirm_close():
    return messagebox.askyesno(
        message="You have unsaved changes.Are you sure you want to close?",
        icon="question",
        title="Unsaved Changes"
    )


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename=os.path.basename(file_path)
        text_widget = get_text_widget()
        content = text_widget.get("1.0","end-1c")
        with open(file_path,"w")as file:
            file.write(content)
    except(AttributeError,FileNotFoundError):
        print("COULD NOT SAVE THE FILE")
        return
    notebook.tab("current",filename)
    text_content[str(text_widget)] = hash(content)


def open__file():
    file_path = filedialog.askopenfilename()
    try:
        filename = os.path.basename(file_path)
        with open(file_path,"r") as file:
            content = file.read()
    except(AttributeError,FileNotFoundError):
        print("could not open a file")
    create(content, filename)
def show_about():
    messagebox.showinfo(
        title = "ABOUT",
        message="THIS TELLLS YOU ABOUT"
    )
def confirm_quit():
    unsaved = False
    for tab in notebook.tabs():
        text_widget = root.nametowidget(tab)
        content = text_widget.get("1.0","end-1c")
        if hash(content) != text_content[str(text_widget)]:
            unsaved=True
            break
    if unsaved:
        confirm = messagebox.askyesno(
            message="You have unsaved changes.Are you sure you want to quit?",
            icon="question",
            title="Confirm Quit"
        )
        if not confirm:
            return
    root.destroy()




root = tk.Tk()
root.title("TEXT EDITOR")
root.option_add("*tearoff",False)
main = ttk.Frame(root)
main.pack(fill = "both",expand = True,padx=1,pady=(4,0))
menubar = tk.Menu()

root.config(menu=menubar)
file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)
menubar.add_cascade(menu=file_menu,label="FILE")
menubar.add_cascade(menu=help_menu,label="HELP")

file_menu.add_command(label="NEW",command = create,accelerator="Ctrl+N")
file_menu.add_command(label="OPEN",command = open__file,accelerator="Ctrl+O")
file_menu.add_command(label="SAVE",command =save_file,accelerator="Ctrl+S")
file_menu.add_command(label="CLOSE TAB",command =close_current_tab,accelerator="Ctrl+C")
file_menu.add_command(label="EXIT",command=confirm_quit)
help_menu.add_command(label="ABOUT",command =show_about)

notebook = ttk.Notebook(main)
notebook.pack(fill="both",expand = True)
root.bind("<KeyPress>",lambda event:check_for_changes())
root.bind("<Control-n>",lambda event:create())
root.bind("<Control-o>",lambda event:open__file())
root.bind("<Control-c>",lambda event:close_current_tab())
root.bind("<Control-s>",lambda event:save_file())
root.mainloop()
