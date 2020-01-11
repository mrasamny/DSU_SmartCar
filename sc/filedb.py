import os.path
from pathlib import Path

cfghome = os.path.expanduser("~")

class FileDB(object):
    """A file based database.
    A file based database, read and write arguements in the specific file.
    """
    def __init__(self, db=cfghome):
        """Init the db_file is a file to save the datas."""
        # Check if db_file is defined
        if db != None and os.path.exists(db):
            self.db = db+'/smartcar.cfg'
        else:
            self.db = 'smartcar.cfg'
            
        if not os.path.exists(self.db):
            Path(self.db).touch() 
        
    def get(self, name, default_value=None):
        """Get value by data's name. Default value is for the arguemants do not exist"""
        try:
            conf = open(self.db,'r')
            lines=conf.readlines()
            conf.close()
            file_len=len(lines)
            flag = False
            # Find the arguement and set the value
            for i in range(file_len):
                if lines[i][0] != '#':
                    if lines[i].split('=')[0].strip() == name:
                        value = lines[i].split('=')[1].replace(' ', '').strip()
                        flag = True
            if flag:
                return eval(value)
            else:
                return default_value
        except :
                return default_value

    @property
    def path(self, path):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
                            
    def set(self, name, value):
        """Set value by data's name. Or create one if the arguement does not exist"""

        # Read the file
        conf = open(self.db,'r')
        lines=conf.readlines()
        conf.close()
        file_len=len(lines)
        flag = False
        # Find the arguement and set the value
        for i in range(file_len):
            if lines[i][0] != '#':
                if lines[i].split('=')[0].strip() == name:
                    lines[i] = '%s = %s\n' % (name, value)
                    flag = True
        # If arguement does not exist, create one
        if not flag:
            lines.append('%s = %s\n' % (name, value))

        # Save the file
        conf = open(self.db,'w')
        conf.writelines(lines)
        conf.close()
