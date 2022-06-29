import imp
from typing import Dict, List, Tuple
import json
from utils import read_file, str_similarity,find_word


CPPPrimitiveType = ["int", "float", "double", "char",
                    "bool", "void", "long", "short", "unsigned", "signed"]
CPPClassType = ["string", "vector", "map",
                "set", "unordered_map", "unordered_set"]
CPPKeyword = ['catch', 'sizeof', 'void', 'template', 'while', 'auto', 'typename', 'constexpr', 'volatile', 'dynamic_cast', 'false', 'if', 'reinterpret_cast', 'friend', 'thread_local', 'enum', 'class', 'namespace', 'continue', 'try', 'public', 'short', 'operator', 'typeid', 'switch', 'do', 'protected',
              'for', 'asm', 'static', 'new', 'decltype', 'true', 'union', 'goto', 'return', 'register', 'struct', 'extern', 'typedef', 'this', 'throw', 'break', 'virtual', 'default', 'noexcept', 'nullptr', 'private', 'static_cast', 'const_cast', 'delete', 'inline', 'using', 'else',  'alignof', 'const', 'case']

CPP_USUAL_LIB_TOKEN = ["cin","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream","ostream","iostream","cout","cerr","endl","getline","vector","map","set","unordered_map","unordered_set","string","fstream","ifstream","ofstream","fstream","istream"]

class CompileError:
    def __init__(self, path: str, errors: List[Dict]):
        self.path = path
        self.errors = errors

    def __str__(self):
        return json.dumps(self.errors, indent=4)

    def __sizeof__(self) -> int:
        return len(self.errors)

    def __len__(self) -> int:
        return len(self.errors)

    def get_error_position(self, idx) -> Tuple[int, int, int, int]:
        """
        Get begincol, beginrow, endcol, endrow
        """
        error = self.errors[idx]
        location = error["locations"][0]
        begincol = location["caret"]["column"]
        beginrow = location["caret"]["line"]
        if "finish" in location.keys():
            endcol = location["finish"]["column"]
            endrow = location["finish"]["line"]
        else:
            endcol = begincol
            endrow = beginrow
        return begincol, beginrow, endcol, endrow

    def get_error_message(self, idx) -> str:
        """
        Get error message
        """
        error = self.errors[idx]
        return error["message"]

    def get_error_string(self, idx) -> str:
        """
        Read error file with begincol, beginrow to endcol, endrow
        """
        begincol, beginrow, endcol, endrow = self.get_error_position(idx)
        return read_file(self.path, begincol, beginrow, endcol, endrow)

    def is_type_error(self, idx) -> bool:
        """
        Check if error is type error
        """
        error = self.errors[idx]
        return "does not name a type" in error["message"]

    def is_preprocess_error(self, idx) -> bool:
        """
        Check if error is preprocess error
        """
        error = self.errors[idx]
        return "invalid preprocessing directive" in error["message"]

    def is_at_top_of_file(self, idx) -> bool:
        """
        Check if error is at top of file
        """
        begincol, beginrow, endcol, endrow = self.get_error_position(idx)
        return endrow < 5

    def is_not_declared_error(self, idx) -> bool:
        """
        Check if error is not declared error
        """
        error = self.errors[idx]
        return "was not declared in this scope" in error["message"]

    def most_similar_primitive_type(self, idx) -> str:
        """
        Get most similar primitive type
        """
        s = self.get_error_string(idx)
        t = ""
        for p in CPPPrimitiveType:
            if str_similarity(s, p) > str_similarity(s, t):
                t = p
        return t


    def is_similar_class_type(self, idx) -> bool:
        """
        Check if error is similar class type
        """
        s = self.get_error_string(idx)
        t = self.most_similar_class_type(idx)
        return str_similarity(s, t) > 0.3
    
    def is_similar_primitive_type(self, idx) -> bool:
        """
        Check if error is similar primitive type
        """
        s = self.get_error_string(idx)
        t = self.most_similar_primitive_type(idx)
        return str_similarity(s, t) > 0.3

    def most_similar_class_type(self, idx) -> str:
        """
        Get most similar class type
        """
        s = self.get_error_string(idx)
        t = ""
        for c in CPPClassType:
            if str_similarity(s, c) > str_similarity(s, t):
                t = c
        return t

    def most_similar_keyword(self, idx) -> str:
        """
        Get most similar keyword
        """
        s = self.get_error_string(idx)
        t = ""
        for k in CPPKeyword:
            if str_similarity(s, k) > str_similarity(s, t):
                t = k
        return t

    def is_similar_keyword(self, idx) -> bool:
        """
        Check if error is similar keyword
        """
        s = self.get_error_string(idx)
        t = self.most_similar_keyword(idx)
        return str_similarity(s, t) > 0.8

    def is_not_declared_error(self, idx) -> bool:
        """
        Check if error is not declared error
        """
        error = self.errors[idx]
        return "was not declared in this scope" in error["message"]
    
    def not_declared_error_fix(self, idx)->str:
        """
        Get fix for not declared error
        """
        error = self.errors[idx]
        if "did you mean" in error["message"]:
            return error["message"].split("did you mean")[1].split("?")[0].replace("'", "").strip()
        return ""

    def error_is_function_call(self, idx) -> bool:
        """
        Check if error is function call
        """
        error = self.errors[idx]
        begincol, beginrow, endcol, endrow = self.get_error_position(idx)
        f= read_file(self.path, begincol, beginrow, endcol+1, endrow)
        return len(f)!=0 and f[-1] == "("
    
    def is_using_std_define(self, idx) -> bool:
        """
        Check if error is using std define
        """
        error = self.errors[idx]
        if "std" in error["message"]:
            return False
        return find_word("using namespace std", self.path) or find_word(f"using std::{self.get_error_string()}", self.path)

    def is_cpp_usual_lib_token(self, idx) -> bool:
        """
        Check if error is cpp usual lib token
        """
        s = self.get_error_string(idx)
        return s in CPP_USUAL_LIB_TOKEN

    def is_discard_qualifier_error(self, idx)->bool:
        """
        Check if error is discard qualifier error
        """
        error = self.errors[idx]
        return "discards qualifiers" in error["message"]
    
    def is_function_call_para_error(self, idx)->bool:
        """
        Check if error is function call para error
        """
        error = self.errors[idx]
        return "invalid conversion from" in error["message"]
    
    def is_template_error(self, idx)->bool:
        """
        Check if error is template error
        """
        error = self.errors[idx]
        return "<" in error["message"] and ">" in error["message"]
    
    def is_direct_cause(self, idx)->bool:
        """
        Check if error is direct cause
        """
        error = self.errors[idx]
        location = error["locations"][0]
        file = location["start"]["file"]
        print(file)
        print(self.path)
        if file == self.path:
            return True
        return False