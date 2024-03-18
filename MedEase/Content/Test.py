import tkinter as tk
from tkinter import messagebox

def show_tooltip(text):
    tooltip_label.config(text=text)
    tooltip_label.place(x=window.winfo_pointerx() + 10, y=window.winfo_pointery() + 10)

def hide_tooltip(event=None):
    tooltip_label.place_forget()

def open_file():
    messagebox.showinfo("Info", "Open clicked")

def save_file():
    messagebox.showinfo("Info", "Save clicked")

# Create the main window
window = tk.Tk()
window.title("Tooltip Example")

# Create a menu
menu = tk.Menu(window)
window.config(menu=menu)

# Create a "File" menu
file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)

# Add "Open" menu item with tooltip
open_text = "Open a file"
open_command = lambda: open_file()
file_menu.add_command(label="Open", command=open_command, 
                      accelerator="Ctrl+O", 
                      activeforeground="blue", 
                      activebackground="lightgrey", 
                      state="active")
file_menu.entryconfig("Open", 
                      activeforeground="blue", 
                      activebackground="lightgrey", 
                      state="active")

# Add "Save" menu item with tooltip
save_text = "Save the current file"
save_command = lambda: save_file()
file_menu.add_command(label="Save", command=save_command)
file_menu.entryconfig("Save", 
                      activeforeground="blue", 
                      activebackground="lightgrey", 
                      state="active")

# Create a label for the tooltip
tooltip_label = tk.Label(window, bg="lightyellow", relief="solid", borderwidth=1, wraplength=150)
tooltip_label.bind("<Enter>", lambda event: [print('uhvuhgv'), hide_tooltip()])
tooltip_label.bind("<Leave>", lambda event: [print('uhvuhgv'), hide_tooltip()])

# Bind mouse hover events to show tooltips
file_menu.entryconfig("Open", 
                      activeforeground="blue", 
                      activebackground="lightgrey", 
                      state="active",
                      command=lambda: show_tooltip(open_text))
file_menu.entryconfig("Save", 
                      activeforeground="blue", 
                      activebackground="lightgrey", 
                      state="active",
                      command=lambda: show_tooltip(save_text))

# Run the application
window.mainloop()
