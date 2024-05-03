import json
import os
import pickle
from typing import Any, Optional


def load_json(filedir: str) -> dict:
    with open(filedir) as f:
        data = json.load(f)
    return data


def save_json(filepath: str, dct: dict,
              json_encoder: Optional[json.JSONEncoder] = None,
              indent: int = 4,
              ) -> None:
    create_dirs_for_filepath(filepath)
    with open(filepath, 'w') as outfile:
        json.dump(dct, outfile, indent=indent, cls=json_encoder)


def load_pickle(filepath: str,
                encoding: str = 'ASCII',
                ) -> Any:
    with open(filepath, 'rb') as obj:
        file = pickle.load(obj, encoding=encoding)
    return file


def save_pickle(filepath: str, file: object) -> None:
    create_dirs_for_filepath(filepath)
    with open(filepath, 'wb') as file_pi:
        pickle.dump(file, file_pi)

