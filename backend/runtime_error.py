import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
# import matplotlib.pyplot as plt

# Use fuzzy logic to process user and system reports
# 用户报告为0-10分的分数
# 1. 程序经常崩溃吗？每次、偶尔、从不（设置本条的原因是OOP有一个实验是写大型游戏，因此崩溃是偶发性的，很难复现）
# 2. 程序CPU占用率高吗？高、中等、低 (因为每个实验和同学的电脑CPU都不同，很难量化CPU占用率)
# 3. 程序内存占用率高吗？高、中等、低 (因为每个实验和同学的电脑内存都不同，很难量化内存占用率)
# 4. 程序运行时间长吗？太长、正常、短
# 5. 程序运行结果正确吗？总是正确、经常正确、从不正确 (我们实验中不可能覆盖每个测例，只能让学生观察在典型测例和自定义测例下的情况)
# 系统报告为0或者10分的分数
# 1. 出现segfault吗？
# 2. 出现time out吗？

# 返回数个建议及每个建议的推荐值
# 1. 向助教报告并求助
# 2. 使用valgrind工具检查程序的内存泄露/非法访问
# 3. 检查循环条件和递归终止条件
# 4. 检查程序的输入输出
def process_report(cond: dict):
    # 输入
    crush = ctrl.Antecedent(np.arange(0, 11, 1), 'crush')
    crush['never'] = fuzz.trimf(crush.universe, [0, 0, 5])
    crush['often'] = fuzz.trimf(crush.universe, [0, 5, 10])
    crush['always'] = fuzz.trimf(crush.universe, [5, 10, 10])

    cpu = ctrl.Antecedent(np.arange(0, 11, 1), 'cpu')
    cpu['low'] = fuzz.trimf(cpu.universe, [0, 0, 5])
    cpu['medium'] = fuzz.trimf(cpu.universe, [0, 5, 10])
    cpu['high'] = fuzz.trimf(cpu.universe, [5, 10, 10])

    mem = ctrl.Antecedent(np.arange(0, 11, 1), 'mem')
    mem['low'] = fuzz.trimf(mem.universe, [0, 0, 5])
    mem['medium'] = fuzz.trimf(mem.universe, [0, 5, 10])
    mem['high'] = fuzz.trimf(mem.universe, [5, 10, 10])

    time = ctrl.Antecedent(np.arange(0, 11, 1), 'time')
    time['short'] = fuzz.trimf(time.universe, [0, 0, 5])
    time['normal'] = fuzz.trimf(time.universe, [0, 5, 10])
    time['long'] = fuzz.trimf(time.universe, [5, 10, 10])

    correct = ctrl.Antecedent(np.arange(0, 11, 1), 'correct')
    correct['never'] = fuzz.trimf(correct.universe, [0, 0, 5])
    correct['often'] = fuzz.trimf(correct.universe, [0, 5, 10])
    correct['always'] = fuzz.trimf(correct.universe, [5, 10, 10])

    segfault = ctrl.Antecedent(np.arange(0, 11, 1), 'segfault')
    segfault['never'] = fuzz.trimf(segfault.universe, [0, 0, 5])
    segfault['often'] = fuzz.trimf(segfault.universe, [0, 5, 10])
    segfault['always'] = fuzz.trimf(segfault.universe, [5, 10, 10])

    timeout = ctrl.Antecedent(np.arange(0, 11, 1), 'timeout')
    timeout['never'] = fuzz.trimf(timeout.universe, [0, 0, 5])
    timeout['often'] = fuzz.trimf(timeout.universe, [0, 5, 10])
    timeout['always'] = fuzz.trimf(timeout.universe, [5, 10, 10])
    
    # 输出
    report = ctrl.Consequent(np.arange(0, 11, 1), 'report')
    report["low"] = fuzz.trimf(report.universe, [0, 0, 5])
    report["medium"] = fuzz.trimf(report.universe, [0, 5, 10])
    report["high"] = fuzz.trimf(report.universe, [5, 10, 10])
    
    valgrind = ctrl.Consequent(np.arange(0, 11, 1), 'valgrind')
    valgrind["low"] = fuzz.trimf(valgrind.universe, [0, 0, 5])
    valgrind["medium"] = fuzz.trimf(valgrind.universe, [0, 5, 10])
    valgrind["high"] = fuzz.trimf(valgrind.universe, [5, 10, 10])

    lore = ctrl.Consequent(np.arange(0, 11, 1), 'lore') #Loop or Recursion
    lore["low"] = fuzz.trimf(lore.universe, [0, 0, 5])
    lore["medium"] = fuzz.trimf(lore.universe, [0, 5, 10])
    lore["high"] = fuzz.trimf(lore.universe, [5, 10, 10])

    inout = ctrl.Consequent(np.arange(0, 11, 1), 'inout') #Input or Output
    inout["low"] = fuzz.trimf(inout.universe, [0, 0, 5])
    inout["medium"] = fuzz.trimf(inout.universe, [0, 5, 10])
    inout["high"] = fuzz.trimf(inout.universe, [5, 10, 10])

    # 规则1：如果程序经常崩溃或内存占用率高或出现segfault，则使用valgrind的推荐值为高
    rule1 = ctrl.Rule(crush['always'] | segfault['always'] | mem['high'], valgrind['high'])
    # 规则2：如果程序偶尔崩溃且内存占用率中等, 则使用valgrind的推荐值为高
    rule2 = ctrl.Rule(crush['often'] & mem['medium'], valgrind['high'])
    # 规则3：如果程序偶尔崩溃或内存占用率中等 则使用valgrind的推荐值为中
    rule3 = ctrl.Rule(crush['often'] |  mem['medium'], valgrind['medium'])
    # 规则4：如果程序从不崩溃且内存占用率不为高，则使用valgrind的推荐值为低
    rule4 = ctrl.Rule(crush['never'] & segfault['never'] & ~mem['high'], valgrind['low'])
    # 规则5：如果程序timeout的频率中等或高，则检查循环和递归的推荐值为高
    rule5 = ctrl.Rule(timeout['often'] | timeout['always'], lore['high'])
    # 规则6：如果程序从不timeout，但CPU占用率高且运行时间长，则检查循环和递归的推荐值为高
    rule6 = ctrl.Rule(timeout['never'] & cpu['high'] & time['long'], lore['high'])
    # 规则7：如果程序从不timeout，CPU占用率低但运行时间长，则检查输入输出的推荐值为高(因为此时被iobound了)
    rule7 = ctrl.Rule(timeout['never'] & cpu['low'] & time['long'], inout['high'])
    # 规则8：如果程序从不timeout，但CPU占用率中等且运行时间中等，则检查循环和递归的推荐值为中
    rule8 = ctrl.Rule(timeout['never'] & cpu['medium'] & time['normal'], lore['medium'])
    # 规则9：如果程序从不timeout且运行时间短，则检查循环和递归的推荐值为低
    rule9 = ctrl.Rule(timeout['never'] & time['short'], inout['low'])
    # 规则10: 如果程序从不timeout,从不segfault,从不崩溃,但运行结果从不正确，则检查输入输出的推荐值为高(估计是输出错了)
    rule10 = ctrl.Rule(timeout['never'] & segfault['never'] & crush['never'] & correct['never'], inout['high'])
    # 规则11: 如果程序从不timeout,从不segfault,从不崩溃，则检查输入输出的推荐值为低
    rule11 = ctrl.Rule(timeout['never'] & segfault['never'] & crush['never'], inout['low'])
    # 规则12: 如果程序从不timeout,从不segfault,从不崩溃，但有偶发性的错误，则向助教报告并求助的推荐值为高
    rule12 = ctrl.Rule(timeout['never'] & segfault['never'] & crush['never'] & correct["often"], report["high"])
    # 规则13：如果程序会timeout或会segfault，则向助教报告并求助的推荐值为低
    rule13 = ctrl.Rule(timeout['often'] | segfault['often'], report["low"])
    
    # 以下为补充规则

    ## 根据单项补充规则
    rule15 = ctrl.Rule(crush['never'], report["low"])
    rule16 = ctrl.Rule(crush['often']|crush['always'], report["medium"])
    rule17 = ctrl.Rule(cpu['high'], report["medium"])
    rule18 = ctrl.Rule(cpu['medium']|cpu["low"], report["low"])
    rule19 = ctrl.Rule(mem['high'], report["medium"])
    rule20 = ctrl.Rule(mem['medium']|mem["low"], report["low"])
    rule21 = ctrl.Rule(time['long'], report["medium"])
    rule22 = ctrl.Rule(time['normal']|time['short'], report["low"])
    rule23 = ctrl.Rule(correct['always'], report["low"])
    rule24 = ctrl.Rule(correct['often'], report["medium"])
    rule25 = ctrl.Rule(correct['never'], report["high"])
    rule26 = ctrl.Rule(segfault['never'], report["low"])
    rule27 = ctrl.Rule(segfault['often'], report["medium"])
    rule28 = ctrl.Rule(segfault['always'], report["high"])
    rule29 = ctrl.Rule(timeout['never'], report["low"])
    rule30 = ctrl.Rule(timeout['often'], report["medium"])
    rule31 = ctrl.Rule(timeout['always'], report["high"])

    rule32 = ctrl.Rule(crush['never'], valgrind["low"])
    rule33 = ctrl.Rule(crush['often']|crush['always'], valgrind["high"])
    rule34 = ctrl.Rule(cpu["low"]|cpu["medium"]|cpu["high"], valgrind["low"])
    rule35 = ctrl.Rule(mem["low"], valgrind["low"])
    rule36 = ctrl.Rule(mem["medium"], valgrind["medium"])
    rule37 = ctrl.Rule(mem["high"], valgrind["high"])
    rule38 = ctrl.Rule(time["short"]|time["normal"]|time["long"], valgrind["low"])
    rule39 = ctrl.Rule(correct["never"]|correct['often']|correct['always'], valgrind["low"])
    rule40 = ctrl.Rule(segfault['never'], valgrind["low"])
    rule41 = ctrl.Rule(segfault['often']|segfault['always'], valgrind["high"])
    rule42 = ctrl.Rule(timeout['never']|timeout['often']|timeout['always'] , valgrind["low"])

    rule43 = ctrl.Rule(crush['never'], inout["low"])
    rule44 = ctrl.Rule(crush['often']|crush['always'], inout["high"])
    rule45 = ctrl.Rule(cpu["low"]|cpu["medium"]|cpu["high"], inout["low"])
    rule46 = ctrl.Rule(mem["low"]|mem['medium']|mem['high'], inout["low"])
    rule47 = ctrl.Rule(time["short"]|time["normal"]|time["long"], inout["low"])
    rule48 = ctrl.Rule(correct['often']|correct['always'], inout["high"])
    rule49 = ctrl.Rule(correct["never"], inout["low"])
    rule50 = ctrl.Rule(segfault['never']|segfault["often"], inout["low"])
    rule51 = ctrl.Rule(segfault['always'], inout["high"])
    rule52 = ctrl.Rule(timeout['never']|timeout['often']|timeout['always'], inout["low"])  

    rule53 = ctrl.Rule(crush['never']|crush['often']|crush['always'], lore["low"])
    rule54 = ctrl.Rule(cpu["low"]|cpu["medium"], lore["low"])
    rule55 = ctrl.Rule(cpu["high"], lore["high"])
    rule56 = ctrl.Rule(mem["low"]|mem['medium']|mem['high'], lore["low"])
    rule57 = ctrl.Rule(time["short"], lore["low"])
    rule58 = ctrl.Rule(time["normal"], lore["medium"])
    rule59 = ctrl.Rule(time["long"], lore["high"])
    rule60 = ctrl.Rule(correct["never"]|correct['often']|correct['always'], lore["low"])
    rule61 = ctrl.Rule(segfault['never']|segfault["often"]|segfault['always'], lore["low"])
    rule62 = ctrl.Rule(timeout['never'], lore["low"])
    rule63 = ctrl.Rule(timeout['often']|timeout['always'], lore["high"])




    # 创建控制器
    ctrl_sys = ctrl.ControlSystem(rules=[rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60, rule61, rule62, rule63])

    # 创建实例
    c = ctrl.ControlSystemSimulation(ctrl_sys)
    # 设置输入参数
    c.input['crush'] = cond["crush"]
    c.input['cpu'] = cond["cpu"]
    c.input['mem'] = cond["mem"]
    c.input['time'] = cond["time"]
    c.input['correct'] = cond["correct"]
    c.input['segfault'] = cond["segfault"]
    c.input['timeout'] = cond["timeout"]
    c.compute()
    # ctrl_sys.view()
    # plt.show()
    # 输出结果
    return {
        "report": c.output['report'],
        "inout": c.output['inout'],
        "lore": c.output['lore'],
        "valgrind": c.output['valgrind']
    }

    

if __name__ == "__main__":
    a = process_report({
        "crush": 1,
        "cpu": 1,
        "mem": 10,
        "time": 1,
        "correct": 10,
        "segfault": 0,
        "timeout": 0
    })
    print(a)