from typing import List
from utils import find_word

def is_undefined_reference(err):
    return "undefined reference" in err

def is_multiple_definition(err):
    return "multiple definition" in err

def is_undefined_main(err):
    return "undefined reference to `main'" in err

def find_which_file_contains_reference(reference: str, files: List[str]):
    f = []
    for file in files:
        if find_word(reference, file)["exist"]:
            f.append(file)
    return f


def get_reference_string(err):
    return err.split("undefined reference")[1].split("`")[1].split("'")[0]

def get_multiple_definition_string(err):
    return err.split("multiple definition")[1].split("`")[1].split("'")[0]