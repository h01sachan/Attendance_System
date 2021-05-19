import tkinter as tk
from tkinter import ttk
import os,time
from datetime import date, datetime
from recoginition import *
from tkinter import messagebox as mb
from threading import Thread

def print_time():
    datetime_label.config(text="DATE: " + str(datetime.now().strftime("%d/%m/%Y")) + "        " + 
                "TIME: " + str(time.strftime("%H:%M:%S")))
    datetime_label.after(1000, print_time)

def attendence():
    # Thread(target=recognise).start()
    recognise()
    return
def save_image(event):
    name_entry.unbind("<Return>")
    # Thread(target=lambda: save_from_file(dir_path.get(),str(name.get()))).start()
    save_from_file(dir_path.get(),str(name.get()))
    name_entry.delete(0,tk.END)
    name_entry.grid_remove()
    name_label.grid_remove()
    path.delete(0,tk.END)
    path.grid_remove()
    path_label.grid_remove()

def new_faces(event):
    if os.path.exists(str(dir_path.get())):
        if os.path.isfile(str(dir_path.get())):
            path.unbind("<Return>")
            name_entry.focus()
            name_label.grid(row=4,column=0, columnspan=2)
            name_entry.grid(row=4, column=2,columnspan=4,padx=25, pady=4)
            name_entry.bind('<Return>',save_image)
        else:
            Thread(target=lambda: save_from_folder(str(dir_path.get()))).start()
    else:
        mb.showerror("ERROR", "FILE OR FOLDER DOES NOT EXISTS")
        path.delete(0,tk.END)
        path.grid_remove()
        path_label.grid_remove()

def save_face(emb):
    save_embedding(emb,str(name.get()))
    name_entry.unbind("<Return>")
    name_entry.delete(0,tk.END)
    name_entry.grid_remove()
    name_label.grid_remove()

def capture_face():
    q,emb = capture()
    if q:
        name_entry.focus()
        name_label.grid(row=4,column=0, columnspan=2)
        name_entry.grid(row=4, column=2,columnspan=4,padx=25, pady=4)
        name_entry.bind('<Return>',lambda event: save_face(emb))


def add_face():
    path.focus()
    path_label.grid(row=3, column=0, columnspan=2, padx=25,pady=4)
    path.grid(row=3,column=3,columnspan=4,padx=25, pady=4)
    path.bind('<Return>',new_faces)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("FACE RECOGNITION")

    root.configure(background='lavender blush')
    tk.Label(root, text="FACE RECOGNITION ATTENDENCE SYSTEM", 
                fg="magenta4", bg="plum1",
                font=("Courier", 20)
            ).grid(row=0, columnspan=6, padx=25, pady=5)
    
    dir_path = tk.StringVar(root)
    name = tk.StringVar(root)

    datetime_label = tk.Label(root, text="DATE: " + str(datetime.now().strftime("%d/%m/%Y")) + "        " + 
                "TIME: " + str(time.strftime("%H:%M:%S")),
                fg="maroon4",bg="pink"
            )
    take_attendence_button = tk.Button(root, text="Take attencence", bg="misty rose", fg="DeepPink2",command=attendence)
    capture_face_button = tk.Button(root, text='Capture and add face', bg="misty rose", fg="DeepPink2",command=capture_face)
    add_new_face_button = tk.Button(root, text='Add face(s) via file/folder', bg="misty rose", fg="DeepPink2",command=add_face)
    path_label = tk.Label(root,text="Enter path to file or folder: ", bg="misty rose", fg="DeepPink2")
    path = ttk.Entry(root, width=50, text='',textvariable=dir_path)
    name_label = tk.Label(root,text="Name of person: ", bg="misty rose", fg="DeepPink2")
    name_entry = ttk.Entry(root, width=20,text='',textvariable=name)

    datetime_label.grid(row=1, columnspan=6, padx=25, pady=4)
    take_attendence_button.grid(row=2, column=0, columnspan=2, padx=25, pady=4)
    add_new_face_button.grid(row=2, column=2, columnspan=2, padx=25, pady=4)
    capture_face_button.grid(row=2, column=4, columnspan=2, padx=25, pady=4)
    print_time()
    root.mainloop()