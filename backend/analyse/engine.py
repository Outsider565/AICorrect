import os
import sys
from typing import Dict
import subprocess
import json


def gather_system_info() -> Dict:
    """
    Gathers system information and returns it as a dictionary.
    """
    return {
        "cwd": os.getcwd(),
        "os": sys.platform,
        "python": sys.version,
        "g++": os.popen("g++ --version").read(),
        "gcc": os.popen("gcc --version").read(),
        "cmake": os.popen("cmake --version").read(),
        "make": os.popen("make --version").read(),
    }


def compile_program(program_path: str, output_path: str="output") -> Dict:
    """
    Compiles a program and returns the g++ output
    """
    try:
        # read stdout and stderr from the process
        process = subprocess.run(["g++", "-fdiagnostics-format=json", "-fsanitize=address",
                                program_path, "-o", output_path],
                                capture_output=True,
                                universal_newlines=True)
        err = json.loads(process.stderr)
        return err
    except Exception as e:
        return {"error": str(e), "msg":process.stderr}


if __name__ == "__main__":
    print(json.dumps(compile_program(sys.argv[1]), indent=4))