import Labber

class Tagger():
    def __init__(self, path:list, info:dict, overwrite = 0):

        self.path_list = path
        self.info_dict = info
        self.overwrite = overwrite
        self.key = ('sample','env','proj','user','tag')
        self.path_trans()

    def get_Tag(self, log):
        info_dict = {}
        project = log.getProject().split('/')
        sample, environment, projectname = '','',''
        if len(project) > 1 :
            sample = project[0]
            environment = project[1]
            if len(project) > 2 :
                projectname = project[2]
        info_dict["sample"] = sample
        info_dict["env"] = environment
        info_dict["proj"] = projectname
        info_dict["user"] = log.getUser()
        info_dict["tag"] = log.getTags()

        return info_dict
    
    def extract_project(self, dict):
        seq = []
        for str in ('sample', 'env', 'proj'):
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
        if self.overwrite:
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

if __name__ == "__main__":
    path = ['C:/Users/edwin/Labber/Data/2022/10/Data_1008/Chalmers_TD_pwrdep_0dBm.hdf5']
    info = {
        'sample': 'transmon',
        'env': 'TL',
        'proj': 'slow_light',
        'user': 'tester',
        'tag': 'testing'
    }
    test =Tagger(path,info,1)
    test.tagging()

    file = test.path_list[0]
    log = Labber.LogFile(file)
    tag = test.get_Tag(log)
    print(tag)