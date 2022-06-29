from typing import Tuple, List, Dict, Union
from utils import compile, str_similarity, link_objs, run_exec
import os, sys
from utils import link_objs
from compile_error import CompileError
from link_error import *
from runtime_error import process_report
def compile_correct(path:str)->Dict:
    """
        Return:{
            success: bool,
            objs: List[str],
            messages: List[str],
        }
    """
    result = compile(path)
    if result["success"]:
        return {
            "success": True,
            "objs": result["objs"],
            "messages": ["Success"]
        }
    file_errors:List[CompileError] = []
    messages = []
    for key, value in result["errors"].items():
        # Rule 0: If cannot find file, then suggest check the upload file
        if value == "file_not_exist":
            return{
                "success": False,
                "objs": [],
                "messages": [f"使用规则0: 文件{key}不存在，建议检查文件路径是否正确"]
            }
        file_errors.append(CompileError(key, value))
    # Use rule-based approach to check compile error
    for file_error in file_errors:
        for i in range(len(file_error)):
            begincol, beginrow, endcol, endrow = file_error.get_error_position(i)
            msg = f"在第{beginrow}至第{endrow}行、第{begincol}至第{endcol}列出现错误{file_error.get_error_string(i)}。"
        # Rule 5: If err is type error and similar to keyword, then suggest using the most similar keyword
            if file_error.is_type_error(i) and file_error.is_similar_keyword(i):
                messages.append(msg+f"使用规则5: 认为是词法错误，且错误类型{file_error.get_error_string(i)}与标准库关键字{file_error.most_similar_keyword(i)}类似，建议使用{file_error.most_similar_keyword(i)}")
                continue
        # Rule 1: If err is type error and similar to primitive type, then suggest using the most similar type
            if file_error.is_type_error(i) and file_error.is_similar_primitive_type(i):
                messages.append(msg+f"使用规则1: 认为是类型错误，且错误类型{file_error.get_error_string(i)}与原生类型{file_error.most_similar_primitive_type(i)}类似，建议使用{file_error.most_similar_primitive_type(i)}")
                continue
        # Rule 2: If err is type error and similar to class type, then suggest using the most similar type
            if file_error.is_type_error(i) and file_error.is_similar_class_type(i):
                messages.append(msg+f"使用规则2: 认为是类型错误，且错误类型{file_error.get_error_string(i)}与标准库容器类型{file_error.most_similar_class_type(i)}类似，建议使用{file_error.most_similar_class_type(i)}")
                continue
        # Rule 3: If err is preprocessor error and at top of file and similar to include, then suggest using #include
            if file_error.is_preprocess_error(i):
                if file_error.is_at_top_of_file(i) and str_similarity(file_error.get_error_string(i), "include") > 0.8:
                    messages.append(msg+f"使用规则3: 认为是预处理错误、在文件顶部且与include相似, 建议修改为include")
        # Rule 4: If err is preprocessor error but not following Rule3
                else:
                    messages.append(msg+f"使用规则4: 认为是预处理错误，建议检查该预处理命令")
                continue
        # Rule 6: If err is type error and not similar to any type or keyword, then suggest check for any library
            if file_error.is_type_error(i) and not file_error.is_similar_primitive_type(i):
                messages.append(msg+f"使用规则6: 认为是类型错误，且错误类型{file_error.get_error_string(i)}与任何类型都不相似，建议检查该类型是否为库类型且出现拼写错误")
                continue
        # Rule 9: If err is CPP usual library token, and there's no std:: defined, then suggest using std::
            if file_error.is_cpp_usual_lib_token(i) and not file_error.is_using_std_define(i):
                messages.append(msg+f"使用规则9: 认为是常见的标准库token, 且没有std::, 建议加上std::")
                continue
        # Rule 7: If err is not_declared error and has similar to nearby variable name, then suggest using the most similar variable name
            if not file_error.error_is_function_call(i) and file_error.is_not_declared_error(i) and file_error.not_declared_error_fix(i):
                messages.append(msg+f"使用规则7: 认为是变量未声明错误，且错误变量{file_error.get_error_string(i)}与附近变量{file_error.not_declared_error_fix(i)}类似，建议使用{file_error.not_declared_error_fix(i)}")
                continue
        # Rule 8: If err is not_declared error and has similar to nearby function name, then suggest using the most similar function name
            if file_error.error_is_function_call(i) and file_error.is_not_declared_error(i) and file_error.not_declared_error_fix(i):
                messages.append(msg+f"使用规则8: 认为是函数未声明错误，且错误函数{file_error.get_error_string(i)}与附近函数{file_error.not_declared_error_fix(i)}类似，建议使用{file_error.not_declared_error_fix(i)}")
                continue
        # Rule 10: If err is discard qualifier error, then suggest reconsidering the const qualifier in function call
            if file_error.is_discard_qualifier_error(i):
                messages.append(msg+f"使用规则10: 认为是函数调用时传入参数{file_error.get_error_string(i)}的const错误,建议考虑是否应该使用const")
                continue
        # Rule 11: If err is function call parameter matching error, then suggect double check the function call parameter
            if file_error.is_function_call_para_error(i):
                messages.append(msg+f"使用规则11: 认为是函数调用参数错误, 建议检查函数调用参数类型是否正确")
                continue
        # Rule 16: If err is template error, then suggest check this template
            if file_error.is_template_error(i):
                messages.append(msg+f"使用规则16: 认为是模板错误, 建议检查模板是否正确")
                continue
    print(result)
    print(messages)
    return {
        "success": False,
        "objs": [],
        "messages": messages
    }
    
        
             
def link_correct(text_files:List[str], objs:List[str])->Tuple[bool, str, str]:
    """
    Return (Success, Exec, Message)
    """
    result = link_objs(objs)
    err = result["errors"]
    message = ""
    while(1):
        # Rule 12: If main function is not found both in text and in object file, then suggest adding main function
        if is_undefined_main(err) and len(find_which_file_contains_reference("main", text_files)) == 0:
            message = "使用规则12: 认为是main函数在文本和二进制文件中未定义, 建议添加main函数或检查main函数是否被打错"
            break
        # Rule 13: If main function is found in text file but not in object file, then suggest inspect compiling process
        elif is_undefined_main(err) and len(find_which_file_contains_reference("main", text_files))>0:
            message = "使用规则13: 认为是main函数在二进制文件中未定义, 但在文本中已定义, 建议检查编译过程"
            break
        if is_undefined_reference(err):
            refs = get_reference_string(err)
        # Rule 14: If refs function is not found object file, then suggest adding refs function
            file = find_which_file_contains_reference(refs.split("(")[0], text_files)
            message = f"使用规则14: 认为是函数{refs}在二进制文件中未定义但在{file}中被引用, 建议添加函数{refs}"
            break
        # Rule 15: If multiple definition error, then suggest double check the definition
        if is_multiple_definition(err):
            refs = get_multiple_definition_string(err)
            files = find_which_file_contains_reference(refs.split("(")[0], text_files)
            message = f"使用规则15: 认为是函数{refs}在二进制文件中有多个定义, 这些定义可能在{files}中, 建议检查函数{refs}的定义"
            break
        break
    return result["success"], result["exec"], message

def runtime_correct(path:str, user_report:Dict={})->str:
    """
    Return Suggestion
    """
    result = run_exec(path)
    segfault = False
    timeout = False
    if "AddressSanitizer" in result:
        segfault = True
    if "Timeout" in result:
        timeout = True
    report = user_report | {
        "segfault": 10 if segfault else 0,
        "timeout": 10 if timeout else 0
    }
    result:Dict[str, int] = process_report(report)
    # 取结果的前3条
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)[0]
    suggestion = {
        "report": "向助教报告并求助",
        "valgrind": "使用valgrind工具检查程序的内存泄露/非法访问",
        "lore": "检查循环条件和递归终止条件",
        "inout": "检查程序的输入输出"
    }
    message = f"使用模糊逻辑：建议{suggestion[result[0]]}"
    return message
    


def run_debug(path: str,user_report:Dict)->Dict:
    """
    Return:{
        "compile_message": str,
        "link_message": str,
        "runtime_message": str,
    }
    """
    result = compile_correct(path)
    if not result["success"]:
        return {
            "compile_message": result["messages"],
            "link_message": "",
            "runtime_message": ""
        }
    objs = result["objs"]
    files = [path + "/"+file for file in os.listdir(path) if file.endswith(".cpp") or file.endswith(".h")] if os.path.isdir(path) else [path]
    result = link_correct(files, objs)
    if not result[0]:
        return {
            "compile_message": "",
            "link_message": result[2],
            "runtime_message": ""
        }
    if os.path.isdir(path):
        exec_path = path + "/" + result[1]
    else:
        exec_path = "/".join(path.split("/")[:-1]) + "/" + result[1]
    return {
            "compile_message": "",
            "link_message": "",
            "runtime_message": runtime_correct(exec_path, user_report)
        }
    
    


if __name__ == "__main__":
    run_debug(sys.argv[1])
    