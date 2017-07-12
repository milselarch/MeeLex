import yaml

"""
load config data from gitignored config.yml file
access by using conf[key] where conf is instance of config
"""

class config(object):
    filename = 'config.yml'

    def __init__(self):
        try:
            self.open()
        except FileNotFoundError:
            self.makeDefaults()

    def __getitem__(self, item):
        return self.data[item]

    def open(self):
        fileData = open(self.filename).read()
        fileData = fileData.replace('\t', ' ' * 4)
        self.data = yaml.load(fileData)
        print(self.data)

    def makeDefaults(self):
        data = {
            'botToken': None
        }

        print("KEY IN CONFIGS")
        for key in data:
            data[key] = input(key+": ")

        with open(self.filename, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

if __name__ == '__main__':
    conf = config()
