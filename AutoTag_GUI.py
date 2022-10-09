import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import AutoTag_py

class App(tk.Tk):
    def __init__(self):
        super().__init__() #Inheritance tk.TK()

        #Create paneWindows
        self.pw1 = tk.PanedWindow(self,orient='vertical')
        self.file = file_fram(self.pw1)
        self.pw1.add(self.file)
        self.interface = interface_fram(self.pw1)
        self.pw1.add(self.interface)
        self.pw1.pack(fill = 'both', expand= 1, pady = 5, padx = 3)

        #Create widgets
        self.overwrite_checkbox = tk.Checkbutton(self, text = 'Confirm Overwrite')
        self.process_btn = tk.Button(self, text = 'Process')
        self.cancel_btn = tk.Button(self, text = 'Cancel')
        self.information = tk.Label(self,text = 'Info: ')

        #Create vars
        self.overwrite_check = tk.IntVar()

        #Configure
        self.title("Auto Tag")
        self.geometry('400x600+1000+80')
        self.resizable(0,0)
        self.pw1.paneconfig(self.file, minsize = 200, height = 320)
        self.pw1.paneconfig(self.interface, minsize = 170)

        self.overwrite_checkbox.config(variable = self.overwrite_check, onvalue= 1, offvalue= 0)
        self.process_btn.config(command = self.confirm)
        self.cancel_btn.config(command = self.destroy)
        self.information.config()

        #layout
        self.information.pack(side = 'top', anchor='w', padx = 10)
        self.overwrite_checkbox.pack(side = 'left',padx = 10 , pady = 10)
        self.cancel_btn.pack(side = 'right', padx = 10)
        self.process_btn.pack(side = 'right')

    def confirm(self):
        self.information['text'] = 'Info: '
        path = self.file.get_selected()
        info = self.interface.get_info()
        check = self.overwrite_check.get()
        self.tagger = AutoTag_py.Tagger(path, info, check).tagging()
        self.information['text'] = f'Info: Total process {len(path)} files.'


class file_fram(tk.LabelFrame):
    def __init__(self,container):
        super().__init__(container)
        self.config(text = 'Selected files', relief= 'flat', pady = 5)

        #create widgets
        self.listbox = tk.Listbox(self,selectmode="multiple")
        self.select_btn = tk.Button(self, text = 'select file')
        self.add_btn = tk.Button(self, text = 'Add')
        self.del_btn = tk.Button(self, text = 'Delet')
        self.select_check = tk.IntVar()
        self.select_checkbtn = tk.Checkbutton(self, text = 'select all')

        #config 
        self.select_btn.config(command = self.selectfile, width= 10)
        self.add_btn.config(command = self.addfile, width = 10)
        self.del_btn.config(command = self.delfile, width = 10)
        self.select_checkbtn.config(
            command = self.select_all,
            variable = self.select_check,
            onvalue = 1, offvalue = 0,
        )

        #layout
        self.listbox.pack(side = 'left', fill = 'both', expand = 1, padx = 3)
        self.select_btn.pack(side = 'top', padx = 3)
        self.add_btn.pack(side = 'top', padx = 3)
        self.del_btn.pack(side = 'top', padx = 3)
        self.select_checkbtn.pack(side = 'top', padx = 3, pady = 5)

        #path dict
        self.path_dict = {}

    def selectfile(self):
        self.listbox.delete(0,'end')
        self.filespath = fd.askopenfilenames(
            parent= self,
            title = 'AutoTags - Open files',
            filetypes=[("Labber log files (*.hdf5)","*.hdf5")]
        )
        self.files = list(self.filespath)

        for path in self.files:
            names = path.split('/')[-1]
            self.path_dict[names] = path
            self.listbox.insert('end',names)

    def addfile(self):
        self.filespath = fd.askopenfilenames(
            parent= self,
            title = 'AutoTags - Open files',
            filetypes=[("Labber log files (*.hdf5)","*.hdf5")]
        )
        self.files = list(self.filespath)

        for path in self.files:
            names = path.split('/')[-1]
            self.path_dict[names] = path
            self.listbox.insert('end',names)

    def delfile(self):
        for idx in reversed(self.listbox.curselection()):
            del self.path_dict[self.listbox.get(idx)]
            self.listbox.delete(idx)
    
    def select_all(self):
        #select and deselect
        if self.select_check.get():
            self.listbox.select_set(0,"end")
        else:
            self.listbox.select_clear(0,"end")

    def get_selected(self):
        path = []
        for idx in self.listbox.curselection():
            path.append(self.path_dict[self.listbox.get(idx)])
        return path


class interface_fram(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(pady = 10)

        #create weidgets
        self.sample_label = tk.Label(self, text = 'Sample name: ')
        self.env_label = tk.Label(self, text = 'Environment: ')
        self.proj_label = tk.Label(self, text = 'Project name: ')
        self.user_label = tk.Label(self, text = 'User name: ')
        self.tag_label = tk.Label(self, text = 'Tags: ')

        self.sample_Entry = tk.Entry(self)
        self.env_Entry = tk.Entry(self)
        self.proj_Entry = tk.Entry(self)
        self.user_Entry = tk.Entry(self)
        self.tag_CBox = ttk.Combobox(self)

        #config
        self.sample_label.config(width = 13, anchor = 'w')
        self.env_label.config(width = 13, anchor = 'w')
        self.proj_label.config(width = 13, anchor = 'w')
        self.user_label.config(width = 13, anchor = 'w')
        self.tag_label.config(width = 13, anchor = 'w')

        # self.sample_Entry.config()
        # self.env_Entry.config()
        # self.proj_Entry.config()
        # self.user_Entry.config()
        self.tag_CBox.config(
            values = [
                "",
                "one_tone",
                "two_tone",
                "Rabi",
                "T1",
                "T2E",
                "T2R",
                "RB",
            ],
            width= 18,
            state= 'readonly'
        )

        #layout
        self.sample_label.grid(row = 0, column = 0, sticky= 'w', padx = 5, pady = 3)
        self.env_label.grid(row = 1, column = 0, sticky= 'w', padx = 5, pady = 3)
        self.proj_label.grid(row = 2, column = 0, sticky= 'w', padx = 5, pady = 3)
        self.user_label.grid(row = 3, column = 0, sticky= 'w', padx = 5, pady = 3)
        self.tag_label.grid(row = 4, column = 0, sticky= 'w', padx = 5, pady = 3)

        self.sample_Entry.grid(row = 0, column = 1)
        self.env_Entry.grid(row = 1, column = 1)
        self.proj_Entry.grid(row = 2, column = 1)
        self.user_Entry.grid(row = 3, column = 1)
        self.tag_CBox.grid(row = 4, column = 1)

    def get_info(self):
        info_dict = {}
        info_dict['sample'] = self.sample_Entry.get()
        info_dict['env'] = self.env_Entry.get()
        info_dict['proj'] = self.proj_Entry.get()
        info_dict['user'] = self.user_Entry.get()
        info_dict['tag'] = [self.tag_CBox.get()]
        if len(self.tag_CBox.get()) == 0:
            info_dict['tag'] = []
        return info_dict
            



if __name__ == "__main__":
    app = App()
    app.mainloop()