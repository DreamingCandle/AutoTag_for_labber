import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import Labber
database_path = r"C:\Users\edwin\SynologyDrive\DESKTOP-V6JLHQU\C\Users\cluster\Labber\Data\Database.hdf5"

class Tagger():
    def __init__(self, path:list, info:dict, overwrite = 0):

        self.path_list = path
        self.info_dict = info
        self.overwrite = overwrite
        self.key = ('sample','proj','user','tag')
        self.path_trans()

    def get_Tag(self, log):
        info_dict = {}
        project = log.getProject().split('/')
        sample, projectname = '',''
        sample = project[0]
        if len(project) > 1 :
            projectname = project[1]
        info_dict["sample"] = sample
        info_dict["proj"] = projectname
        info_dict["user"] = log.getUser()
        info_dict["tag"] = log.getTags()
        return info_dict
    
    def extract_project(self, dict):
        seq = []
        for str in ('sample', 'proj'):
            seq.append(dict[str])
        try:
            seq.remove('')
        except:
            pass
        projname = '/'.join(seq)
        
        return projname
    
    def path_trans(self):
        for i,path in enumerate(self.path_list):
            seq = path.split('/')
            path = '\\'.join(seq)
            self.path_list[i] = path

    def tagging(self):
        if self.overwrite ==1 :
            proj = self.extract_project(self.info_dict)
            for i, path in enumerate(self.path_list):
                log = Labber.LogFile(path)
                log.setProject(proj)
                log.setTags(self.info_dict['tag'])
                log.setUser(self.info_dict['user'])
        else:
            for i, path in enumerate(self.path_list):
                log = Labber.LogFile(path)
                logTag = self.get_Tag(log)
                for str in self.key:
                    if len(logTag[str])==0:
                        logTag[str] = self.info_dict[str]
                proj = self.extract_project(logTag)
                log.setProject(proj)
                log.setTags(logTag['tag'])
                log.setUser(logTag['user'])

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
        self.resizable(1,0)
        self.pw1.paneconfig(self.file, minsize = 200, height = 320)
        self.pw1.paneconfig(self.interface, minsize = 150)

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
        if len(info['sample']) == 0 and len(info['proj']) != 0 and check == 1:
            self.information['text'] = 'Info: Sample name cannot leave blank.'
        else:
            self.tagger = Tagger(path, info, check).tagging()
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

        #select database
        self.sample = []
        self.user = []
        self.database = self.Database_labels(database_path)

        #create weidgets
        self.sample_label = tk.Label(self, text = 'Sample name: ')
        self.proj_label = tk.Label(self, text = 'Project name: ')
        self.user_label = tk.Label(self, text = 'User name: ')
        self.tag_label = tk.Label(self, text = 'Tags: ')

        self.sample_CBox = ttk.Combobox(self)#
        self.proj_Entry = tk.Entry(self)
        self.user_CBox = ttk.Combobox(self)#
        self.tag_CBox = ttk.Combobox(self)

        #config
        self.sample_label.config(width = 13, anchor = 'w')
        self.proj_label.config(width = 13, anchor = 'w')
        self.user_label.config(width = 13, anchor = 'w')
        self.tag_label.config(width = 13, anchor = 'w')

        self.sample_CBox.config(
            values = self.sample,
            width= 18

        )#
        self.proj_Entry.config(
            width= 20
        )
        self.user_CBox.config(
            values = self.user,
            width= 18
        )#
        self.tag_CBox.config(
            values = [
                "",
                "one_tone",
                "owo_tone/sweep_flux",
                "owo_tone/sweep_pwr",
                "two_tone",
                "two_tone/sweep_flux",
                "two_tone/sweep_pwr",
                "Rabi",
                "T1",
                "T2E",
                "T2R",
                "RB",
                "others"
            ],
            width= 18,
            state= 'readonly'
        )

        #layout
        self.sample_label.grid(row = 0, column = 0, sticky= 'w', padx = 5, pady = 3)
        self.proj_label.grid(row = 1, column = 0, sticky= 'w', padx = 5, pady = 3)
        self.user_label.grid(row = 2, column = 0, sticky= 'w', padx = 5, pady = 3)
        self.tag_label.grid(row = 3, column = 0, sticky= 'w', padx = 5, pady = 3)

        self.sample_CBox.grid(row = 0, column = 1)
        self.proj_Entry.grid(row = 1, column = 1)
        self.user_CBox.grid(row = 2, column = 1)
        self.tag_CBox.grid(row = 3, column = 1)

    def get_info(self):
        info_dict = {}
        info_dict['sample'] = self.sample_CBox.get()
        info_dict['proj'] = self.proj_Entry.get()
        info_dict['user'] = self.user_CBox.get()
        info_dict['tag'] = [self.tag_CBox.get()]
        if len(self.tag_CBox.get()) == 0:
            info_dict['tag'] = []
        return info_dict
    
    def Database_labels(self,path):
        import h5py
        if path == '':
            return None
        f = h5py.File(path,'r')
        Labels = f['Labels'][:]
        for i,tag in enumerate(Labels):
            tag = tag.decode("utf-8").split('/')
            if tag[0] == 'Project':
                self.sample.append(tag[1])
            elif tag[0] == 'User':
                self.user.append(tag[1])

            



if __name__ == "__main__":
    app = App()
    app.mainloop()