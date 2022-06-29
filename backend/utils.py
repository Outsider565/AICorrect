import os
import sys
from typing import Dict, List
import subprocess
import json
import difflib

GCC_ARGS = ["-fdiagnostics-format=json", "-fsanitize=address", "-std=c++17"]


def compile_file(filepath) -> Dict:
    """
    Compiles path.cpp to path.o without link
    Return {
        success: bool,
        obj: str,
        errors: List[Dict]
    }
    """
    process = subprocess.run(["g++"]+GCC_ARGS+[filepath, "-c", "-o", filepath.replace(".cpp", "0")+".o"],
                             capture_output=True,
                             universal_newlines=True)
    err = json.loads(process.stderr)
    if len(err) == 0:
        return {
            "success": True,
            "obj": filepath.replace(".cpp", "0")+".o",
            "errors": []
        }
    else:
        return {
            "success": False,
            "obj": "",
            "errors": err
        }


def compile(path: str) -> Dict:
    """
    Call compile_file
    If path is a directory, compile every file ends with cpp
    Return{
        success: bool,
        objs: List[str],
        errors: Dict{
            file: List[Dict]
        }
    }
    """
    if not os.path.exists(path):
        return {
            "success": False,
            "objs": [],
            "errors": 
                {
                    path: "file_not_exist",
                }
            
        }
    if os.path.isdir(path):
        objs = []
        errors = {}
        for file in os.listdir(path):
            if file.endswith(".cpp"):
                result = compile_file(os.path.join(path, file))
                if result["success"]:
                    objs.append(result["obj"])
                else:
                    errors[file] = result["errors"]
        if len(errors) == 0:
            return {
                "success": True,
                "objs": objs,
                "errors": {}
            }
        else:
            return {
                "success": False,
                "objs": objs,
                "errors": errors
            }
    else:
        result = compile_file(path)
        if result["success"]:
            return {
                "success": True,
                "objs": [result["obj"]],
                "errors": {}
            }
        else:
            return {
                "success": False,
                "objs": [],
                "errors": {
                    path: result["errors"]
                }
            }


def find_word(word: str, file: str) -> Dict:
    """
    Find a word in file, return its cols and rows
    {
        exist: bool,
        cols: int,
        rows: int
    }
    """
    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if word in line:
                return {
                    "exist": True,
                    "cols": line.index(word),
                    "rows": i
                }
    return {"exist": False}


def read_file(file: str, begincol: int, beginrow: int, endcol: int, endrow: int) -> str:
    """
    Read a file from begincol, beginrow to endcol, endrow
    """
    with open(file, "r") as f:
        lines = f.readlines()
        lines = [line[begincol-1:endcol] for line in lines[beginrow-1:endrow]]
        return "".join(lines)


def str_similarity(str1: str, str2: str) -> float:
    """
    Calculate the similarity of two strings
    """
    return difflib.SequenceMatcher(None, str1, str2).ratio()


def link_objs(objs: List[str]):
    """
    Link objs, return{
        success: bool,
        exec: str,
        errors: str
    }
    """
    dir = os.path.dirname(objs[0])
    process = subprocess.run(["g++"]+GCC_ARGS+objs+["-o", dir+"/"+"a.out"],
                             capture_output=True,
                             universal_newlines=True)
    err = str(process.stderr)
    if len(err) == 0:
        return {
            "success": True,
            "exec": "a.out",
            "errors": ""
        }
    else:
        return {
            "success": False,
            "exec": "",
            "errors": err
        }


def run_exec(exec: str, input: str = "") -> str:
    """
    Run exec with input, return output
    """
    process = subprocess.run([exec],
                             input=input,
                             capture_output=True,
                             universal_newlines=True,
                             timeout=1)
                             
    return str(process.stderr)


if __name__ == "__main__":
    print(json.dumps(compile(sys.argv[1]), indent=4))
