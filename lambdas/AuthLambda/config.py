import importlib

yaml = importlib.import_module("lib.yaml")

"""
load config data from gitignored config.yml file
access by using conf[key] where conf is instance of config
"""

class config(object):
    data = {
        'AccessID': None,
        'AccessSecret': None,
        'awsDynamodbRegion': None
    }

    filename = 'data/config.yml'

    def __init__(self, open = True):
        if open == True:
            self.open()

    def __getitem__(self, item):
        return self.data[item]

    def update(self):
        try:
            self.open()
        except FileNotFoundError:
            print("ERR: CONFIG FILE NOT FOUND")

        for key in self.data:
            #print(self.data)
            current = self.data[key]

            if current == None:
                self.data[key] = input(key + ": ")
            else:
                param = input(key + " [%s]" % current + ": ")

                if param == "": self.data[key] = current
                else: self.data[key] = param

        with open(self.filename, 'w') as outfile:
            yaml.dump(self.data, outfile, default_flow_style=False)

    def open(self):
        fileData = open(self.filename).read()
        fileData = fileData.replace('\t', ' ' * 4)
        data = yaml.load(fileData)
        for key in data:
            if key in self.data:
                self.data[key] = data[key]

        print(self.data)

    def makeDefaults(self):
        print("KEY IN CONFIGS")

        for key in self.data:
            self.data[key] = input(key+": ")


        with open(self.filename, 'w') as outfile:
            yaml.dump(self.data, outfile, default_flow_style=False)

if __name__ == '__main__':
    conf = config(open=False)
    conf.update()
