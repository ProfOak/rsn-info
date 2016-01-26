import rarfile


class RSN:
    def __init__(self, filename):
        """
        Extract files from rsn files - wrapper for rarfile

        RSN files are just rar files.
        To use the 'rarfile' import you must have unrar on your system.
        """
        self.filename = filename
        self.rf = rarfile.RarFile(filename)
        self.size = len(self.rf.infolist())

    def list_filenames(self):
        """list names of files only"""
        return [song.filename for song in self.files()]

    def files(self):
        """yeild all of the files as RarInfo objects"""
        return self.rf.infolist()

    def read_file(self, f):
        """return the raw bits of a file from the rar archive"""
        return self.rf.read(f)

    def extractall(self):
        """extract all files from the rsn archive"""
        self.rf.extractall()

    def close(self):
        """closes file"""
        self.rf.close()
