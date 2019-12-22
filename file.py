import os
import os.path

class File:
    def __init__(self, base_dir=''):
        self.base_dir = base_dir
        if base_dir != '' and base_dir not in os.listdir():
            os.mkdir(base_dir)

    def listdir(self):
        return os.listdir(self.base_dir)

    def abspath(self, file):
        return self.base_dir + os.path.sep + file
        
    def open(self, file, mode='r', **kwargs):
        return open(self.base_dir + os.path.sep + file, mode=mode, **kwargs)
