import tkinter as tk
import tkinter.filedialog as fd


root = tk.Tk()
root.title('test list')

listbox = tk.Listbox(root)
listbox.pack(side = 'left', fill = 'both',expand='yes')

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side = 'left', fill = 'both')

files = fd.askopenfilenames(parent = root, title = 'AutoTags - Open files',filetypes=[("Labber log files (*.hdf5)","*.hdf5")])
files = list(files)

for names in files:
    listbox.insert('end',names.split('/')[-1])

listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command=listbox.yview)

btn = tk.Button(text = 'click me',width= 10,height= 5)
btn.pack()
root.mainloop()