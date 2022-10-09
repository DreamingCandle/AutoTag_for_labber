import Labber

'''
Setdict = {
    'tags' = [''],
    'user' = '',
    'project' = ''
    }
'''

dictionary = r'C:\Users\edwin\Labber\Data\2022\10\Data_1008'
fname = '\Chalmers_TD_pwrdep_0dBm.hdf5'
path = dictionary + fname
Setdict = {}


log = Labber.LogFile(path)
project = log.getProject().split('/')
sample, environment, projectname = '','',''
if len(project) > 1 :
    sample = project[0]
    environment = project[1]
    if len(project) > 2 :
        projectname = project[2]

print(f'sample = {sample}\nenvironment = {environment}\nprojectname = {projectname}')


Setdict["tags"] = log.getTags()
Setdict["user"] = log.getUser()
Setdict["sample"] = sample
Setdict["environment"] = environment


print('\nConfirm current setup:\n\n'
      f'User = { Setdict["user"] }\n'
      f'Sample = {Setdict["sample"]}\n'
      f'Environment = {Setdict["environment"]}\n'
      f'Tags = {Setdict["tags"]}'
      )




Setdict["project"] = Setdict["sample"] + "/" + Setdict["environment"]

'''
log.setTags(Setdict["tags"])
log.setUser(Setdict["user"])
log.setProject(Setdict["project"])
'''