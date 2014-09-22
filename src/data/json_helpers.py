import json
from pathlib import Path


def load_json(path: Path, decoder=json.JSONDecoder()):
    """
    IOError is passed on for further handling.

    :param path:
    :param decoder:
    :return: :raise e: FileNotFoundError
    """
    file = None
    try:
        file = path.open("r")
        json_set = decoder.decode(file.read())
        file.close()
        return json_set
    except FileNotFoundError as e:
        if file is not None:
            file.close()
        raise e


def save_json(path: Path, obj, encoder=json.JSONEncoder()):
    """
    """
    if not path.exists():
        path.touch()
    file = open(str(path), "w")
    file.truncate()
    encoder.indent = 2
    file.write(encoder.encode(obj))
    file.close()
