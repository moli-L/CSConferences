import json

class Conf(object):
    def __init__(self):
        with open("csconferences/conf.json", 'r') as f:
            self.conf_json = json.loads(f.read())

    def readValue(self, key):
        return self.conf_json[key.upper()]

    def writeValue(self, key, value):
        self.conf_json[key.upper()] = value
        with open("csconferences/conf.json", "w") as f:
            f.write(json.dumps(self.conf_json))

conf = Conf()
print(conf.readValue('index'))