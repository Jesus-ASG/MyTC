class Structure:
    def __init__(self, fpath, fdata):
        self.fpath = fpath
        self.fdata = fdata

    def __str__(self):
        return f'path: {self.fpath}\ndata: restricted'
