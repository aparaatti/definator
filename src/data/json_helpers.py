import json
from pathlib import Path

def load_json(path, decoder=json.JSONDecoder()):
        """
        :param path: Path
        :param decoder:
        :return:
        """
        try:
            #terms = {str(x) for x in p.iterdir() if x.is_dir()}
            file = path.open("r")
            json_str = decoder.decode(file.read())
            file.close()
            return json_str
        except IOError as e:
            print('could not load from file\n' + e)
            
        return None


def save_json(path, obj, encoder=json.JSONEncoder()):
        file = open(path,   "w")
        file.truncate()
        for encoded_line in encoder.encode(obj):
            file.write(encoded_line)
        file.close()


class NotImplementedException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
