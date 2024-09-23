class Folder:
    def __init__(self):
        self.d = {}
        self.info = {}
        self.parent = None
    def all_subpaths(self):
        L = list([name, folder.info] for (name,folder) in self.d.items())
        for path, folder in self.d.items():
            L += [[path+"\\\\" + f[0], f[1]] for f in folder.all_subpaths()]
        return L
    def __str__(self):
        return f"({self.d}, {self.info})"
        

class DirTree:
    def __init__(self):
        self.d = {}
    def add_path(self, path):
        pathparts = path.split("\\\\")
        d = self.d
        parent_folder = None
        for p in pathparts:
            if p in d:
                parent_folder = d[p]
                d = parent_folder.d
            else:
                folder = Folder()
                folder.parent = parent_folder
                parent_folder = folder
                
                d[p] = folder
                d = folder.d
    def process_path(self, path, folderInfoEditor):
        
        pathparts = path.split("\\\\")
        folder = self.d[pathparts[0]]
        folderInfoEditor(folder.info)
        for part in pathparts[1:]:
            folder = folder.d[part]
            folderInfoEditor(folder.info)
            
    def all_subpaths(self):
        L = []
        for path, folder in self.d.items():
            L += [[path+"/" + f[0], f[1]] for f in folder.all_subpaths()]
        return L