import tkMessageBox
from Tkinter import *
import backend as DB


def view_all():
    listbox.delete(0, END)
    for movie in DB.get_movie(""):
        listbox.insert("end", ', '.join(movie))


def search_entry():
    listbox.delete(0,END)
    for movie in DB.get_movie(id_entry.get(),title_entry.get(),genre_entry.get()):
        listbox.insert("end", ', '.join(movie))


def add_entry():
    if id_entry.get()!= "" and title_entry.get() != "" and genre_entry.get()!= "":
        if DB.insert(id_entry.get(),title_entry.get(),genre_entry.get()):
            tkMessageBox.showerror("Error", "Duplicate Movie Id")
        else:
            view_all()
    else:
        tkMessageBox.showerror("Error", "One Or More Fields are Empty")


def update_selected():
    if listbox.curselection()!=():
        selected_list = str(listbox.get(listbox.curselection())).split(", ")
        title = selected_list[1] if title_entry.get()=="" else title_entry.get()
        genre = selected_list[2] if genre_entry.get()=="" else genre_entry.get()
        DB.update(selected_list[0],title,genre)
        view_all()
    else:
        tkMessageBox.showerror("Error","No Movie has Selected")



def delete_selected():
    if listbox.curselection() != ():
        selected_list = str(listbox.get(listbox.curselection())).split(", ")
        DB.delete(eval(selected_list[0]))
        view_all()
    else:
        tkMessageBox.showerror("Error", "No Movie has Selected")


DB.create_movies_table()
movie_window = Tk()
movie_window.title("MovieDB")


title_label = Label(movie_window, text="Title")
title_label.grid(row=0, column=0, padx=10)
id_label = Label(movie_window, text="ID")
id_label.grid(row=1, column=0, padx=10)
genre_label = Label(movie_window, text="Genre")
genre_label.grid(row=0, column=2, padx=10)

title_var = StringVar()
title_entry = Entry(movie_window, textvariable=title_var)
title_entry.grid(row=0, column=1, padx=10)

id_var = StringVar()
id_entry = Entry(movie_window, textvariable=id_var)
id_entry.grid(row=1, column=1, padx=10, pady=10)

genre_var = StringVar()
genre_entry = Entry(movie_window, textvariable=genre_var)
genre_entry.grid(row=0, column=3)

btn_frame = Frame(movie_window)
view_btn = Button(btn_frame, text='View all', command=view_all, width=12)
view_btn.grid(row=0, column=0)
search_bth = Button(btn_frame, text='Search entry', command=search_entry, width=12)
search_bth.grid(row=1, column=0)
add_btn = Button(btn_frame, text='Add entry', command=add_entry, width=12)
add_btn.grid(row=2, column=0)
update_btn = Button(btn_frame, text='Update selected', command=update_selected, width=12)
update_btn.grid(row=3, column=0)
delete_btn = Button(btn_frame, text='Delete selected', command=delete_selected, width=12)
delete_btn.grid(row=4, column=0)
close_btn = Button(btn_frame, text='Close', command=movie_window.destroy, width=12)
close_btn.grid(row=5, column=0)
btn_frame.grid(row=2, column=3)


frame = Frame(movie_window)
scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, yscrollcommand=scrollbar.set, width=35)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)
frame.grid(row=2, column=0, columnspan=2, pady=20)

movie_window.mainloop()
