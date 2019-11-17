import json

class Conf(object):
    def __init__(self):
        with open("csconferences/conf.json", 'r') as f:
            self.conf_json = json.loads(f.read())

    def readValue(self, key):
        return self.conf_json[key.upper()]

    def writeValue(self, key, value):
        self.conf_json[key.upper()] = value
        self.save()

    def addErrorIndex(self, key, index):
        self.conf_json[key.upper()].append(index)
        self.save()
    
    def isErrIndexInList(self, key, index):
        return index in self.conf_json[key.upper()]
    
    def removeErrIndex(self, key, index):
        self.conf_json[key.upper()].remove(index)
        self.save()
    
    def emptyErrList(self, key):
        self.conf_json[key.upper()] = []
        self.save()

    def getErrorIndexList(self, key):
        return self.conf_json[key.upper()]
    
    def save(self):
        with open("csconferences/conf.json", "w") as f:
            f.write(json.dumps(self.conf_json))