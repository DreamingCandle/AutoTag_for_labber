import tkinter as tk #for Button, Checkbox, etc.
import tkinter.ttk as ttk #for progressbar
import tkinter.filedialog as fd


def selectfile():
    listbox.delete(0,'end')
    filespath = fd.askopenfilenames(
    parent = AutoTag,
    title = 'AutoTags - Open files',
    #filetypes=[("Labber log files (*.hdf5)","*.hdf5")]
    )
    files = list(filespath)

    for names in files:
        names = names.split('/')[-1]
        listbox.insert('end',names)

def select_all():
    #select and deselect
    if select_check.get():
        listbox.select_set(0,"end")
    else:
        listbox.select_clear(0,"end")


#Create screen
AutoTag = tk.Tk()
AutoTag.title("AutoTags")
AutoTag.geometry("400x600+1000+80")

#Create panewindow selected file
pw1 = tk.PanedWindow(AutoTag,orient='vertical')
pw1.pack(fill = 'both', expand ='yes')

file_frame = tk.LabelFrame(pw1,text = 'Selected files', relief= 'flat')
pw1.add(file_frame)

Type_frame = tk.Frame(pw1)
pw1.add(Type_frame)

#Create listbox stores selected file

listbox = tk.Listbox(file_frame,selectmode="multiple")
listbox.pack(side = 'left', fill = 'both',expand='yes')

#Selects files to listbox
btn = tk.Button(Type_frame,text = 'select file',command=selectfile).pack(side = 'top')###

select_check = tk.IntVar()
select_checkbtn = tk.Checkbutton(
    file_frame,
    text = 'select all',
    variable = select_check,
    onvalue = 1,
    offvalue = 0,
    command = select_all
)
select_checkbtn.pack()###

#Create checkbox for confirm overwrite

overwrite_check = tk.IntVar()
overwrite_checkbox = tk.Checkbutton(
    Type_frame,
    text = 'Overwrite',
    variable = overwrite_check,
    onvalue= 1,
    offvalue= 0
)

#Create Entry for sample name
sample_label = tk.Label(Type_frame,text = 'Sample name: ')
sample_label.pack()
sample_entry = tk.Entry(Type_frame)
sample_entry.pack()
sample = sample_entry.get()

#Create Entry for environment
env_label = tk.Label(Type_frame,text = 'Environment: ')
env_label.pack()
env_entry = tk.Entry(Type_frame)
env_entry.pack()
env = env_entry.get()

#Create Entry for projectname
proj_label = tk.Label(Type_frame,text = 'Project name: ')
proj_label.pack()
proj_entry = tk.Entry(Type_frame)
proj_entry.pack()
proj = proj_entry.get()

#Create Entry for user name
user_label = tk.Label(Type_frame,text = 'User: ')
user_label.pack()
user_entry = tk.Entry(Type_frame)
user_entry.pack()
user = user_entry.get()

#Create Selectbox for Tags

#Create process button
btn_process = tk.Button(AutoTag,text = 'Process') #main function
btn_process.pack()

#Create cancle button
btn_cancle = tk.Button(AutoTag,text = 'Cancle',command = AutoTag.destroy)
btn_cancle.pack()



AutoTag.mainloop()