import os.path

class FakeConfig:
    def __init__(self):
        self.root_dir = './example/'
        self.build_dir = os.path.join(self.root_dir, '../build/')
        self.encoding = 'utf-8'
